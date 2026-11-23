"""Generated EP/BVA consumption for self-service create body dimensions.

Normal JSON parser binding omits the optional binary upload baseline. This is
an explicit scenario adaptation, not byte-for-byte multipart replay. File
boundary cases remain in the existing five-case B consumer.
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
    body = copy.deepcopy(case["request"]["body"])
    body.pop("attachment", None)
    h.lineage(case_id, body)
    h.record_property("wire_binding", "native-json-with-optional-upload-omitted")
    h.record_property("generated_schema_predicate", case["expected"]["predicate"])
    before = h.snapshot()
    expected = case["expected"]["predicate"]
    # Source-backed wire normalization in employee POST: a falsy end date is
    # replaced by start before serializer validation. Preserve that difference
    # from the raw DateField schema predicate and report it explicitly.
    normalizes_end = case["operation"] == "self_leave_create" and case["field"] == ["end_date"] and (case["omitted"] or case["value"] in (None, ""))
    if normalizes_end:
        expected = "accept"
        h.record_property("bound_oracle", "view-normalizes-empty-end-date-to-start")
    response = h.request("POST", case["route"], body=body)
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
    allocation = case["operation"] == "self_allocation_create"
    assert response.status_code == (200 if allocation else 201), response.text[:500]
    assert h.balance() == before["employee"]
    assert h.balance("approver") == before["approver"]
    assert h.balance("outsider") == before["outsider"]
    if allocation:
        old = {row["id"] for row in before["allocations"]}
        created = [row for row in h.allocations() if row["id"] not in old]
        assert len(created) == 1
        detail = h.allocation_detail(created[0]["id"])
        assert detail["employee_id"]["id"] == h.context["employee"].pk
        assert float(detail["requested_days"]) == float(body["requested_days"])
        assert len(h.leaves()) == len(before["leaves"])
    else:
        detail = h.leave_detail(response.json()["id"])
        assert len(h.leaves()) == len(before["leaves"]) + 1
        assert len(h.allocations()) == len(before["allocations"])
        assert detail["start_date"] == body["start_date"]
        assert detail["end_date"] == (body.get("end_date") or body["start_date"])
        assert float(detail["requested_days"]) == expected_days(body)
    assert detail["status"] == "requested"
    assert detail["description"] == body["description"].strip()
