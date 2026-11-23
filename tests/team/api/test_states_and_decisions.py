"""BR-02/03/04 truth tables and transition cases, driven by a shared catalog."""

from datetime import date, timedelta

import pytest

from case_catalog import authorization_rows, decision_rows, state_rows


@pytest.mark.parametrize("row", [r for r in decision_rows() if r["feasible"]], ids=lambda row: row["id"])
def test_br02_condition_combinations(leave_http, row):
    from leave.models import AvailableLeave, LeaveRequest, LeaveType

    h = leave_http
    h.lineage(row["id"])
    h.grant(5)
    employee, leave_type = h.context["employee"], h.context["leave_type"]
    c = row["conditions"]
    body = h.baseline("leave")
    anchor = date.fromisoformat(body["start_date"])
    body["end_date"] = (anchor if c["ordered"] else anchor - timedelta(days=1)).isoformat()
    body["end_date_breakdown"] = "full_day" if c["matching"] else "first_half"
    # Overlap is the actual endpoint database predicate. A spanning record can
    # satisfy it even when the proposed input date order is itself invalid.
    if not c["no_overlap"]:
        LeaveRequest.objects.create(employee_id=employee, leave_type_id=leave_type,
                                    start_date=anchor - timedelta(days=1), end_date=anchor,
                                    start_date_breakdown="full_day", end_date_breakdown="full_day",
                                    description="Synthetic overlap setup", status="requested")
    LeaveType.objects.filter(pk=leave_type.pk).update(require_attachment="yes")
    if not c["assigned"]:
        AvailableLeave.objects.filter(employee_id=employee, leave_type_id=leave_type).delete()
    before = h.snapshot()
    files = {"attachment": ("proof.txt", b"synthetic", "text/plain")} if c["attachment"] else None
    response = h.request("POST", "/api/v1/leave/user-request/", body=body, files=files)
    assert response.status_code == row["expected_status"], response.text[:500]
    if row["expected_status"] == 201:
        record = h.leave_detail(response.json()["id"])
        assert record["status"] == "requested" and float(record["requested_days"]) == 1
        assert len(h.leaves()) == len(before["leaves"]) + 1
        assert h.balance() == before["employee"]
    else:
        assert response.json(), "Decision rejection must include error details"
        assert h.snapshot() == before


@pytest.mark.parametrize("row", authorization_rows(), ids=lambda row: row["id"])
def test_br04_approval_truth_table(leave_http, row):
    from django.contrib.auth.models import Permission
    from employee.models import EmployeeWorkInformation

    h = leave_http
    h.lineage(row["id"])
    h.grant(5)
    pk = h.create_leave()
    role = "employee" if row["owner"] else "approver"
    actor = h.context[role]
    user = h.context[role + "_user"]
    permission = Permission.objects.get(content_type__app_label="leave", codename="change_leaverequest")
    if row["permission"]:
        user.user_permissions.add(permission)
    else:
        user.user_permissions.remove(permission)
    EmployeeWorkInformation.objects.filter(employee_id=h.context["employee"]).update(reporting_manager_id=actor if row["manager"] else None)
    before = h.snapshot()
    response = h.request("PUT", f"/api/v1/leave/approve/{pk}/", role, {})
    assert response.status_code == row["expected_status"], response.text[:500]
    if response.status_code == 200:
        assert h.leave_detail(pk)["status"] == "approved"
        assert h.balance() == (2.0, 0.0)
        assert h.balance("approver") == (7.0, 0.0)
    else:
        assert response.json().get("error")
        assert h.snapshot() == before


def setup_state(h, row):
    state = row["state"]
    if row["kind"] == "allocation":
        pk = h.create_allocation()
        if state != "requested":
            response = h.request("PUT", f"/api/v1/leave/allocation-{'approve' if state == 'approved' else 'reject'}/{pk}/", "approver", {})
            assert response.status_code == 200
        assert h.allocation_detail(pk)["status"] == state
        return pk
    h.grant(5)
    pk = h.create_leave()
    if state in {"approved", "cancel_requested", "cancelled"}:
        h.approve_leave(pk)
    if state == "rejected":
        assert h.request("PUT", f"/api/v1/leave/reject/{pk}/", "approver", {}).status_code == 200
    if state in {"cancel_requested", "cancelled"}:
        assert h.request("PUT", f"/api/v1/leave/cancel/{pk}/", body={}).status_code == 200
    if state == "cancelled":
        assert h.request("PUT", f"/api/v1/leave/cancellation-approve/{pk}/", "approver", {}).status_code == 200
    assert h.leave_detail(pk)["status"] == state
    return pk


@pytest.mark.parametrize("row", state_rows(), ids=lambda row: row["id"])
def test_state_transition_catalog(leave_http, row):
    h = leave_http
    h.lineage(row["id"])
    pk = setup_state(h, row)
    before = h.snapshot()
    kind, action = row["kind"], row["action"]
    if action in {"update", "delete"}:
        collection = "user-allocation-request" if kind == "allocation" else "user-request"
        route = f"/api/v1/leave/{collection}/{pk}/"
        method = "PUT" if action == "update" else "DELETE"
        body = h.baseline(kind) if action == "update" else {}
        role = "employee"
    else:
        name = "allocation-approve" if action == "self-approve" else "allocation-" + action if kind == "allocation" else action
        route, method, body = f"/api/v1/leave/{name}/{pk}/", "PUT", {}
        role = "employee" if action in {"cancel", "self-approve"} else "approver"
    response = h.request(method, route, role, body)
    assert response.status_code == row["expected_status"], response.text[:500]
    if not row["allowed"]:
        assert response.json()
        assert h.snapshot() == before
        return
    records = h.allocations() if kind == "allocation" else h.leaves()
    if row["target"] == "deleted":
        assert pk not in {record["id"] for record in records}
    else:
        detail = h.allocation_detail(pk) if kind == "allocation" else h.leave_detail(pk)
        assert detail["status"] == row["target"]
    expected = before["employee"]
    if kind == "allocation" and action == "approve": expected = (5.0, 0.0)
    if kind == "allocation" and action == "reject" and row["state"] == "approved": expected = (0.0, 0.0)
    if kind == "leave" and action == "approve": expected = (2.0, 0.0)
    if kind == "leave" and action == "reject" and row["state"] == "approved": expected = (5.0, 0.0)
    if kind == "leave" and action == "cancellation-approve": expected = (5.0, 0.0)
    assert h.balance() == expected
    assert h.balance("approver") == before["approver"]
    assert h.balance("outsider") == before["outsider"]
