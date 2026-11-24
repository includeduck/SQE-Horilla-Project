"""Strict baseline/variant contract assertions; variant mismatches really fail."""

import copy

import pytest

from demonstrate_regeneration import SELECTED_IDS


@pytest.mark.parametrize("case_id", SELECTED_IDS, ids=SELECTED_IDS)
def test_regenerated_allocation_contract(leave_http, case_id):
    h = leave_http
    case = h.case(case_id)
    body = copy.deepcopy(case["request"]["body"])
    descriptor = body.pop("attachment")
    h.lineage(case_id, case["request"]["body"])
    before = h.snapshot()
    response = h.request("POST", case["route"], body=body,
                         files={"attachment": (descriptor["filename"], descriptor["text"].encode(), descriptor["content_type"])})
    expected = 200 if case["expected"]["predicate"] == "accept" else 400
    after = h.snapshot()
    # Inspect persisted state even when the subsequent strict contract assertion fails.
    for role in ("employee", "approver", "outsider"):
        assert after[role] == before[role]
    if response.status_code == 200:
        assert len(after["allocations"]) == len(before["allocations"]) + 1
        detail = h.allocation_detail(after["allocations"][0]["id"])
        assert detail["description"] == body["description"].strip()
        assert detail["employee_id"]["id"] == h.context["employee"].pk
    else:
        assert response.status_code == 400 and response.json().get(case["field"][-1])
        assert after == before
    h.record_property("actual_http_status", response.status_code)
    h.record_property("contract_http_status", expected)
    assert response.status_code == expected, f"Spec/server disagreement: {case_id}; actual {response.status_code}, contract {expected}"
