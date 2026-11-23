"""Source-backed pagination clamps, reference routing and role boundaries."""

import json
from pathlib import Path

import pytest

ARTIFACT = json.loads((Path(__file__).resolve().parents[1] / "generator/generated_cases.json").read_text(encoding="utf-8"))
PAGE_CASE_IDS = [case["id"] for case in ARTIFACT["cases"]
                 if case["operation"] == "self_allocation_list" and case["location"] == "query"
                 and case["class"].startswith("x-clamp-maximum-")]


@pytest.mark.parametrize("case_id", PAGE_CASE_IDS, ids=PAGE_CASE_IDS)
def test_generated_page_size_clamp(leave_http, case_id):
    from leave.models import LeaveAllocationRequest

    h = leave_http
    case = h.case(case_id)
    h.lineage(case_id)
    cap = case["provenance"]["schema"]["x-clamp-maximum"]
    # This is setup only: the operation under test is the real GET paginator.
    LeaveAllocationRequest.objects.bulk_create([
        LeaveAllocationRequest(employee_id=h.context["employee"], leave_type_id=h.context["leave_type"],
                               requested_days=1, description=f"Synthetic paging {index}")
        for index in range(cap + 1)
    ])
    before_ids = list(LeaveAllocationRequest.objects.order_by("id").values_list("id", flat=True))
    response = h.request("GET", case["route"], query=case["request"]["query"])
    assert response.status_code == 200, response.text[:500]
    body = response.json()
    assert body["count"] == cap + 1
    assert len(body["results"]) == case["expected"]["normalized_value"]
    assert body["next"] is not None
    assert all(row["employee_id"]["id"] == h.context["employee"].pk for row in body["results"])
    assert list(LeaveAllocationRequest.objects.order_by("id").values_list("id", flat=True)) == before_ids
    assert h.balance() == (0.0, 0.0)
    assert h.balance("approver") == (7.0, 0.0)


@pytest.mark.parametrize("token", [None, "synthetic-invalid-token"], ids=["missing-token", "invalid-token"])
def test_authentication_required_without_state_change(leave_http, token):
    h = leave_http
    h.lineage("AUTH-TOKEN-" + ("missing" if token is None else "invalid"))
    before = h.snapshot()
    headers = {} if token is None else {"Authorization": "Bearer " + token}
    response = h.session.post(h.base + "/api/v1/leave/user-allocation-request/", headers=headers, json=h.baseline("allocation"), timeout=30)
    assert response.status_code == 401, response.text[:500]
    assert response.json().get("detail")
    assert h.snapshot() == before


@pytest.mark.parametrize("operation,route", [
    ("allocation_detail", "/api/v1/leave/allocation-request/{pk}/"),
    ("leave_detail", "/api/v1/leave/request/{pk}/"),
    ("approve", "/api/v1/leave/approve/{pk}/"),
])
def test_missing_reference_for_authorized_approver(leave_http, operation, route):
    h = leave_http
    case = h.case(operation + ":path:pk:EP:missing-record")
    h.lineage(case["id"])
    before = h.snapshot()
    response = h.request("PUT" if operation == "approve" else "GET", route.format(pk=case["value"]), "approver", {} if operation == "approve" else None)
    assert response.status_code == 404, response.text[:500]
    assert response.json().get("error")
    assert h.snapshot() == before


def test_nonowner_generic_detail_denied(leave_http):
    h = leave_http
    h.lineage("AUTH-NONOWNER-GENERIC-DETAIL")
    pk = h.create_allocation()
    before = h.snapshot()
    response = h.request("GET", f"/api/v1/leave/allocation-request/{pk}/", "outsider")
    assert response.status_code == 403
    assert response.json().get("error")
    assert h.snapshot() == before
