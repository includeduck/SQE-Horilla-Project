"""Runtime binding/assertions shared by the existing Area 2 HTTP consumers.

Only fixture setup uses ORM writes. The operation being tested always traverses
Requests -> live server -> real view/serializer/database. No mocked responses.
"""
import copy
from datetime import date
from pathlib import Path
from urllib.parse import quote

from http_support import response_rows

MISSING = 2147483647


def grant_operation_permissions(h):
    from django.contrib.auth.models import Permission
    user = h.context["approver_user"]
    user.user_permissions.add(*Permission.objects.filter(
        content_type__app_label="leave",
        codename__in=[f"{action}_{model}" for action in ("view", "add", "change", "delete")
                      for model in ("availableleave", "leaverequest", "leaveallocationrequest")]))
    assert not user.is_superuser


def state():
    from leave.models import AvailableLeave, LeaveAllocationRequest, LeaveRequest
    fields = {
        "allocations": (LeaveAllocationRequest, ["id", "employee_id_id", "leave_type_id_id", "requested_days", "description", "status", "is_active", "attachment", "reject_reason"]),
        "leaves": (LeaveRequest, ["id", "employee_id_id", "leave_type_id_id", "requested_days", "description", "status", "is_active", "attachment", "reject_reason", "start_date", "end_date", "start_date_breakdown", "end_date_breakdown", "approved_available_days", "approved_carryforward_days"]),
        "assignments": (AvailableLeave, ["id", "employee_id_id", "leave_type_id_id", "available_days", "carryforward_days", "total_leave_days", "is_active"]),
    }
    return {name: list(model.objects.entire().order_by("id").values(*names))
            for name, (model, names) in fields.items()}


def model_for(operation):
    from leave.models import AvailableLeave, LeaveAllocationRequest, LeaveRequest
    if operation.startswith("assignment_") or operation == "own_balance":
        return AvailableLeave
    return LeaveAllocationRequest if "allocation" in operation else LeaveRequest


def prepare(h, case):
    """Bind actual ID, role, editable state and enough balance independently."""
    from leave.models import AvailableLeave
    grant_operation_permissions(h)
    operation = case["operation"]
    role = case.get("role", "employee")
    is_leave = operation in {"approve", "reject", "cancel", "cancellation_approve", "cancellation_reject"} or (
        "leave" in operation and operation not in {"leave_type_list", "employee_leave_type_list"})
    pk = None
    if is_leave:
        h.grant(5)
    if operation.startswith("assignment_"):
        pk = h.context["avail"].pk
        if operation == "assignment_create":
            # The test must exercise creation, not only an already-assigned no-op.
            AvailableLeave.objects.entire().filter(pk=pk).delete()
            pk = None
    elif operation == "employee_leave_type_list":
        pk = h.context["employee"].pk
    elif "{pk}" in case["route"]:
        pk = h.create_leave() if is_leave else h.create_allocation()
        if operation in {"cancel", "cancellation_approve", "cancellation_reject"}:
            h.approve_leave(pk)
        if operation in {"cancellation_approve", "cancellation_reject"}:
            assert h.request("PUT", f"/api/v1/leave/cancel/{pk}/", body={}).status_code == 200
    return {"pk": pk, "role": role, "operation": operation,
            "route": case["route"].replace("{pk}", str(pk)), "method": case["method"]}


def bound_body(h, case):
    body = copy.deepcopy(case.get("request", {}).get("body", {}))
    # Runtime generator binds employee/type IDs. Path IDs need fresh records and
    # are handled by prepare(). Array boundaries intentionally retain duplicates.
    return body


def send(h, ctx, body, *, query=None, headers=None, encoding="json", raw=None):
    files = None
    payload = copy.deepcopy(body)
    if isinstance(payload, dict):
        for name, value in list(payload.items()):
            if isinstance(value, dict) and set(value) == {"filename", "text", "content_type"}:
                payload.pop(name)
                files = {name: (value["filename"], value["text"].encode("utf-8"), value["content_type"])}
    kwargs = {"headers": dict(h.headers[ctx["role"]]), "timeout": 30}
    if headers:
        kwargs["headers"].update(headers)
    if query is not None:
        kwargs["params"] = query
    if raw is not None:
        kwargs["data"] = raw
    elif files is not None:
        kwargs.update(data=payload, files=files)
    elif encoding == "form":
        kwargs["data"] = payload
    elif encoding == "multipart":
        # A synthetic file-part keeps multipart selection real even when the
        # selected ordinary body has no upload; unknown field is explicitly named.
        kwargs.update(data=payload, files={"wire_transport": ("", b"", "application/octet-stream")})
    elif body is not None:
        kwargs["json"] = payload
    h.record_property("wire_binding", "real-multipart-file" if files else encoding)
    return h.session.request(ctx["method"], h.base + ctx["route"], **kwargs)


def balances(h):
    return {role: h.balance(role) for role in ("employee", "approver", "outsider")}


def readback(h, operation, pk):
    return h.allocation_detail(pk) if "allocation" in operation else h.leave_detail(pk)


def assert_result(h, case, ctx, response, before, before_balances, body, expected_status):
    """Exact wire status plus persisted identities, fields, state and balances."""
    from leave.models import AvailableLeave
    operation = ctx["operation"]
    assert response.status_code == expected_status, (case["id"], response.status_code, response.text[:1200])
    after = state()
    if expected_status >= 400:
        assert after == before, (case["id"], "rejected operation changed persisted state")
        assert balances(h) == before_balances
        assert response.content, "Controlled refusal must provide a response"
        return
    if ctx["method"] == "GET":
        assert after == before
        assert balances(h) == before_balances
        return
    family = "assignments" if operation.startswith("assignment_") else "allocations" if "allocation" in operation else "leaves"
    old = {row["id"]: row for row in before[family]}
    new = {row["id"]: row for row in after[family]}
    pk = ctx["pk"]
    expected_balances = dict(before_balances)
    if operation == "assignment_create":
        # Cartesian assignment has one unique employee/type in the generated
        # baseline even at the cardinality-above boundary (duplicate IDs).
        expected_pairs = {(int(e), int(t)) for e in body["employee_ids"] for t in body["leave_type_ids"]}
        pairs = {(row["employee_id_id"], row["leave_type_id_id"]) for row in after[family]}
        assert expected_pairs <= pairs
        assert len(new) == len(old) + len(expected_pairs - {(r["employee_id_id"], r["leave_type_id_id"]) for r in old.values()})
        own = AvailableLeave.objects.entire().get(employee_id=h.context["employee"], leave_type_id=h.context["leave_type"])
        assert float(own.available_days) == float(h.context["leave_type"].total_days)
        expected_balances["employee"] = (float(own.available_days), float(own.carryforward_days))
    elif ctx["method"] == "DELETE":
        assert set(new) == set(old) - {pk}
        if family == "assignments":
            expected_balances["employee"] = None
    elif ctx["method"] == "POST":
        created = set(new) - set(old)
        assert len(created) == 1
        assert set(old) <= set(new)
        pk = created.pop()
    else:
        assert set(new) == set(old), (case["id"], "update/action changed identities")
    if pk is not None and pk in new:
        row = new[pk]
        assert row["employee_id_id"] == h.context["employee"].pk
        assert row["leave_type_id_id"] == h.context["leave_type"].pk
        if operation == "assignment_update":
            available = float(body["available_days"])
            carry = float(body.get("carryforward_days", old[pk]["carryforward_days"]))
            assert row["available_days"] == available and row["carryforward_days"] == carry
            expected_balances["employee"] = (available, carry)
        elif family != "assignments":
            transitions = {"allocation_approve": "approved", "allocation_reject": "rejected",
                           "approve": "approved", "reject": "rejected", "cancel": "cancel_requested",
                           "cancellation_approve": "cancelled", "cancellation_reject": "approved"}
            assert row["status"] == transitions.get(operation, "requested")
            if operation == "allocation_approve":
                expected_balances["employee"] = (before_balances["employee"][0] + old[pk]["requested_days"], 0.0)
            if operation == "approve":
                expected_balances["employee"] = (before_balances["employee"][0] - old[pk]["requested_days"], 0.0)
            if operation == "cancellation_approve":
                expected_balances["employee"] = (before_balances["employee"][0] + old[pk]["requested_days"], 0.0)
            if isinstance(body, dict) and operation not in transitions:
                for name in ("description", "requested_days", "is_active", "start_date_breakdown", "end_date_breakdown"):
                    if name not in body or name not in row:
                        continue
                    value = body[name]
                    if name == "description":
                        value = str(value).strip()
                    elif name == "requested_days" and value is not None:
                        value = float(value)
                    elif name == "is_active":
                        value = value in (True, 1, "true", "True", "1", "on", "yes")
                    assert row[name] == value, (case["id"], name, row[name], value)
                for name in ("start_date", "end_date"):
                    if name in row and name in body:
                        expected = body[name] or body.get("start_date")
                        assert row[name].isoformat() == expected
                if family == "leaves":
                    start = date.fromisoformat(body["start_date"])
                    end = date.fromisoformat(body.get("end_date") or body["start_date"])
                    left, right = body.get("start_date_breakdown", "full_day"), body.get("end_date_breakdown", "full_day")
                    days = (1 if left == "full_day" else .5) if start == end else (end-start).days-1 + (1 if left == "full_day" else .5) + (1 if right == "full_day" else .5)
                    assert float(row["requested_days"]) == days
                descriptor = body.get("attachment")
                stored = model_for(operation).objects.entire().get(pk=pk)
                if isinstance(descriptor, dict) and set(descriptor) == {"filename", "text", "content_type"}:
                    assert stored.attachment and row["attachment"]
                    with stored.attachment.open("rb") as stream:
                        assert stream.read() == descriptor["text"].encode("utf-8")
                elif "attachment" in body and descriptor is None:
                    assert not stored.attachment
            if operation.startswith(("allocation_", "self_allocation_", "leave_", "self_leave_")) and operation not in transitions:
                detail = readback(h, operation, pk)
                assert detail["id"] == pk and detail["status"] == row["status"]
                if "is_active" in detail:
                    assert detail["is_active"] is row["is_active"]
    # Every other persisted request/assignment must remain identical. Only the
    # employee's assignment may change for balance effects.
    for other_family in before:
        for row in before[other_family]:
            if other_family == family and row["id"] == pk:
                continue
            if other_family == "assignments" and row["employee_id_id"] == h.context["employee"].pk:
                continue
            assert row in after[other_family], (case["id"], "unrelated row changed", other_family, row["id"])
    assert balances(h) == expected_balances, (case["id"], balances(h), expected_balances)


def generated_oracle(case, ctx):
    if case["location"] == "path":
        if case["class"] == "valid":
            return 201 if ctx["method"] == "PUT" and "update" in ctx["operation"] else 200
        if case["class"] == "missing-record":
            op = ctx["operation"]
            return 400 if op.startswith(("self_", "assignment_")) or op in {"cancel", "employee_leave_type_list"} else 404
        return 404
    if case["location"] == "query":
        return 200
    if case["expected"]["predicate"] == "reject":
        if case["field"] == ["end_date"] and (case["omitted"] or case["value"] in (None, "")):
            return 201
        return 400
    return 200 if ctx["operation"] == "self_allocation_create" else 201


def run_generated(h, case):
    ctx = prepare(h, case)
    body = bound_body(h, case)
    if case["field"] != ["attachment"] and isinstance(body, dict):
        body.pop("attachment", None)
    if case["location"] == "path" and case["class"] != "valid":
        token = "" if case["omitted"] else str(case["value"])
        ctx["route"] = case["route"].replace("{pk}", quote(token, safe=""))
    h.lineage(case["id"], body)
    h.record_property("schema_predicate", case["expected"]["predicate"])
    h.record_property("runtime_record_id", ctx["pk"])
    h.record_property("input_family", "INPUT:" + case["operation"] + ":" + case["location"] + ":" + ".".join(map(str, case["field"])))
    if case["location"] == "query":
        return run_pagination(h, case, ctx)
    before, before_balances = state(), balances(h)
    response = send(h, ctx, body)
    expected = generated_oracle(case, ctx)
    assert_result(h, case, ctx, response, before, before_balances, body, expected)


def run_pagination(h, case, ctx):
    from leave.models import LeaveAllocationRequest, LeaveRequest, AvailableLeave, LeaveType
    op = ctx["operation"]
    # Detail GET ignores page_size; assert identity and unchanged persisted data.
    if op == "assignment_detail":
        before, amounts = state(), balances(h)
        response = send(h, ctx, None, query=case["request"]["query"])
        assert response.status_code == 200
        assert response.json()["id"] == ctx["pk"]
        assert_result(h, case, ctx, response, before, amounts, None, 200)
        h.record_property("bound_oracle", "detail-handler-ignores-pagination-query")
        return
    value = case["value"]
    schema = case["provenance"]["schema"]
    cap, default = schema["x-clamp-maximum"], schema["default"]
    expected = min(value, cap) if type(value) is int and value > 0 else default
    employee, leave_type = h.context["employee"], h.context["leave_type"]
    if "allocation" in op:
        model = LeaveAllocationRequest
        model.objects.bulk_create([model(employee_id=employee, leave_type_id=leave_type, requested_days=1, description=f"Paging {i}") for i in range(cap+1)])
    elif op in {"leave_list", "self_leave_list"}:
        model = LeaveRequest
        # ORM population is lower-level setup; the observed operation is GET.
        model.objects.bulk_create([model(employee_id=employee, leave_type_id=leave_type,
            start_date="2031-01-01", end_date="2031-01-01", description=f"Paging {i}") for i in range(cap+1)])
    else:
        # Types and assignment references must be distinct, not duplicated FK pairs.
        types = [LeaveType.objects.create(name=f"Paging {i}", count=1) for i in range(cap+1)]
        if op in {"own_balance", "assignment_list", "employee_leave_type_list"}:
            AvailableLeave.objects.bulk_create([AvailableLeave(employee_id=employee, leave_type_id=t, available_days=1) for t in types])
    before, amounts = state(), balances(h)
    response = send(h, ctx, None, query=case["request"]["query"])
    assert response.status_code == 200, response.text[:1000]
    result = response.json()
    # Generic lists may also contain the independent approver/outsider fixtures;
    # retain exact list population separately through an unbounded size-100 GET.
    assert result["count"] >= cap+1
    assert len(result["results"]) == expected, (case["id"], len(result["results"]), expected)
    assert result["next"] is not None
    assert_result(h, case, ctx, response, before, amounts, None, 200)
