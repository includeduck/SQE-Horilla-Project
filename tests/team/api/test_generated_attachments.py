"""Generated file classes on both self-service create routes, over real HTTP."""

import copy
import json
from pathlib import Path

import pytest

ARTIFACT = json.loads((Path(__file__).resolve().parents[1] / "generator/generated_cases.json").read_text(encoding="utf-8"))
CASE_IDS = [case["id"] for case in ARTIFACT["cases"]
            if case["operation"] in {"self_allocation_create", "self_leave_create"}
            and case["field"] == ["attachment"]
            and not (case["operation"] == "self_allocation_create" and case["technique"] == "BVA")]


@pytest.mark.parametrize("case_id", CASE_IDS, ids=CASE_IDS)
def test_generated_attachment_input(leave_http, case_id):
    from leave.models import LeaveAllocationRequest, LeaveRequest

    h = leave_http
    h.grant(5)
    case = h.case(case_id)
    body = copy.deepcopy(case["request"]["body"])
    h.lineage(case_id, body)
    descriptor = body.get("attachment")
    files = None
    binary = isinstance(descriptor, dict) and set(descriptor) == {"filename", "text", "content_type"}
    if binary:
        body.pop("attachment")
        files = {"attachment": (descriptor["filename"], descriptor["text"].encode("utf-8"), descriptor["content_type"])}
    h.record_property("wire_binding", "multipart-file" if binary else "native-json-null-omission-or-invalid-file")
    before = h.snapshot()
    response = h.request("POST", case["route"], body=body, files=files)
    if case["expected"]["predicate"] == "reject":
        assert response.status_code == 400, response.text[:500]
        assert response.json().get("attachment"), response.text[:500]
        assert h.snapshot() == before
        return

    allocation = case["operation"] == "self_allocation_create"
    assert response.status_code == (200 if allocation else 201), response.text[:500]
    family = "allocations" if allocation else "leaves"
    after = h.snapshot()
    previous_ids = {row["id"] for row in before[family]}
    created = [row for row in after[family] if row["id"] not in previous_ids]
    assert len(created) == 1
    assert len(after[family]) == len(before[family]) + 1
    for key in set(before) - {family}:
        assert after[key] == before[key]
    pk = created[0]["id"]
    detail = h.allocation_detail(pk) if allocation else h.leave_detail(pk)
    assert detail["id"] == pk and detail["status"] == "requested"
    assert detail["description"] == body["description"]
    assert detail["leave_type_id"]["id"] == h.context["leave_type"].pk
    assert float(detail["requested_days"]) == (float(body["requested_days"]) if allocation else 3.0)
    model = LeaveAllocationRequest if allocation else LeaveRequest
    stored = model.objects.get(pk=pk)
    assert stored.employee_id_id == h.context["employee"].pk
    if allocation:
        assert stored.created_by_id == h.context["employee_user"].pk
    else:
        # LeaveRequest overrides HorillaModel.created_by with a nullable
        # Employee FK. The API serializer does not expose/set that optional
        # audit field; the mandatory owner is employee_id, asserted above.
        from employee.models import Employee
        assert model._meta.get_field("created_by").related_model is Employee
    if binary:
        assert detail["attachment"]
        with stored.attachment.open("rb") as source:
            assert source.read() == descriptor["text"].encode("utf-8")
    else:
        assert detail["attachment"] is None
        assert not stored.attachment
