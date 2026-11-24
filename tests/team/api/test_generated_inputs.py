"""Generated EP/BVA consumption for self-service create/update body dimensions.

Normal JSON parser binding omits the optional binary upload baseline. This is
an explicit scenario adaptation, not byte-for-byte multipart replay. File
classes and boundaries use multipart in the B consumer and attachment suite.
"""

import copy
import json
from datetime import date
from pathlib import Path

import pytest

from case_catalog import selected_generated_cases

ARTIFACT = json.loads((Path(__file__).resolve().parents[1] / "generator/generated_cases.json").read_text(encoding="utf-8"))
CASE_IDS = [case["id"] for case in selected_generated_cases(ARTIFACT)]


def expected_days(body):
    start = date.fromisoformat(body["start_date"])
    end = date.fromisoformat(body.get("end_date") or body["start_date"])
    left = body.get("start_date_breakdown", "full_day")
    right = body.get("end_date_breakdown", "full_day")
    if start == end:
        return 1 if left == right == "full_day" else 0.5
    return (end - start).days - 1 + (1 if left == "full_day" else 0.5) + (1 if right == "full_day" else 0.5)


@pytest.mark.parametrize("case_id", CASE_IDS, ids=CASE_IDS)
def test_generated_self_create_input(leave_http, case_id):
    h = leave_http
    h.grant(5)
    case = h.case(case_id)
    allocation = case["operation"].startswith("self_allocation_")
    updating = case["method"] == "PUT"
    pk = None
    route = case["route"]
    if updating:
        pk = h.create_allocation() if allocation else h.create_leave()
        route = route.replace("{pk}", str(pk))
        h.record_property("runtime_record_id", pk)
    body = copy.deepcopy(case["request"]["body"])
    body.pop("attachment", None)
    h.lineage(case_id, body)
    h.record_property("wire_binding", "native-json-with-optional-upload-omitted")
    h.record_property("generated_schema_predicate", case["expected"]["predicate"])
    before = h.snapshot()
    if allocation and updating:
        from leave.models import LeaveAllocationRequest
        persisted_ids = set(LeaveAllocationRequest.objects.entire().filter(
            employee_id=h.context["employee"]).values_list("id", flat=True))
    expected = case["expected"]["predicate"]
    # Source-backed wire normalization in employee POST/PUT: a falsy end date is
    # replaced by start before serializer validation. Preserve that difference
    # from the raw DateField schema predicate and report it explicitly.
    normalizes_end = not allocation and case["field"] == ["end_date"] and (case["omitted"] or case["value"] in (None, ""))
    if normalizes_end:
        expected = "accept"
        h.record_property("bound_oracle", "view-normalizes-empty-end-date-to-start")
    response = h.request(case["method"], route, body=body)
    if expected == "reject":
        assert response.status_code == 400, response.text[:500]
        errors = response.json()
        field = case["field"][-1]
        if case["expected"]["oracle"] == "date-order":
            assert errors.get("end_date")
        else:
            assert errors.get(field), errors
        assert h.snapshot() == before
        return
    assert response.status_code == (200 if allocation and not updating else 201), response.text[:500]
    assert h.balance() == before["employee"]
    assert h.balance("approver") == before["approver"]
    assert h.balance("outsider") == before["outsider"]
    if allocation:
        old = {row["id"] for row in before["allocations"]}
        after = h.allocations()
        if updating:
            inactive = body.get("is_active") is False
            assert {row["id"] for row in after} == (old - {pk} if inactive else old)
            assert set(LeaveAllocationRequest.objects.entire().filter(
                employee_id=h.context["employee"]).values_list("id", flat=True)) == persisted_ids
            persisted = LeaveAllocationRequest.objects.entire().get(pk=pk)
            assert persisted.is_active is (not inactive)
            if inactive:
                inactive_response = h.request("GET", "/api/v1/leave/user-allocation-request/", query={"is_active": "false"})
                assert inactive_response.status_code == 200, inactive_response.text[:500]
                inactive_body = inactive_response.json()
                inactive_rows = inactive_body["results"] if isinstance(inactive_body, dict) else inactive_body
                assert {row["id"] for row in inactive_rows} == {pk}
                h.record_property("bound_oracle", "persisted-inactive-row-hidden-from-default-list-not-deleted")
        else:
            created = [row for row in after if row["id"] not in old]
            assert len(created) == 1
            pk = created[0]["id"]
        detail = h.allocation_detail(pk)
        if updating:
            assert detail["is_active"] is (body.get("is_active") is not False)
        assert detail["employee_id"]["id"] == h.context["employee"].pk
        previous = next((row for row in before["allocations"] if row["id"] == pk), {})
        amount = body.get("requested_days", previous.get("requested_days"))
        if amount is None:
            assert detail["requested_days"] is None
        else:
            assert float(detail["requested_days"]) == float(amount)
        assert h.leaves() == before["leaves"]
    else:
        detail = h.leave_detail(response.json()["id"])
        assert detail["id"] == (pk if updating else response.json()["id"])
        assert len(h.leaves()) == len(before["leaves"]) + (0 if updating else 1)
        assert h.allocations() == before["allocations"]
        assert detail["start_date"] == body["start_date"]
        assert detail["end_date"] == (body.get("end_date") or body["start_date"])
        assert float(detail["requested_days"]) == expected_days(body)
    assert detail["status"] == "requested"
    assert detail["description"] == body["description"].strip()
    assert detail["leave_type_id"]["id"] == body.get("leave_type_id", h.context["leave_type"].pk)
