"""FR-01–FR-10 / BR-01,03,04: real HTTP shared-state and defect regressions.

Unexecuted until the full Horilla runtime is available. Assertions are strict;
no xfail/skip or expectation weakened to match a suspected product defect.
"""

import pytest


def test_w1_to_w2_shared_balance(leave_http):
    h = leave_http
    h.lineage("INTEGRATION-W1-W2-001")
    h.grant(5)
    pk = h.create_leave()
    assert float(h.leave_detail(pk)["requested_days"]) == 3
    assert h.balance() == (5.0, 0.0)
    h.approve_leave(pk)
    assert h.balance() == (2.0, 0.0)
    before = h.snapshot()
    second = h.shifted_leave(14)
    assert second["start_date"] > h.leave_detail(pk)["end_date"]
    response = h.request("POST", "/api/v1/leave/user-request/", body=second)
    assert response.status_code == 400, response.text[:500]
    assert "enough leave" in str(response.json()).lower()
    assert h.snapshot() == before
    assert len(h.leaves()) == 1


def test_refund_belongs_to_requester(leave_http):
    h = leave_http
    h.lineage("DEFECT-REFUND-REQUESTER-001")
    h.grant(5)
    pk = h.create_leave()
    h.approve_leave(pk)
    assert h.balance() == (2.0, 0.0)
    assert h.balance("approver") == (7.0, 0.0)
    response = h.request("PUT", f"/api/v1/leave/reject/{pk}/", "approver", {"reason": "Synthetic regression rejection"})
    assert response.status_code == 200, response.text[:500]
    assert h.leave_detail(pk)["status"] == "rejected"
    assert h.balance() == (5.0, 0.0), "Refund must restore the requester"
    assert h.balance("approver") == (7.0, 0.0), "Approver's own balance must not change"
    assert h.balance("outsider") == (9.0, 0.0)


@pytest.mark.parametrize("approve", [True, False], ids=["approve-cancellation", "reject-cancellation"])
def test_cancellation_decision_and_no_second_attempt(leave_http, approve):
    h = leave_http
    h.lineage("CANCEL-DECISION-" + str(approve))
    h.grant(5)
    pk = h.create_leave()
    h.approve_leave(pk)
    response = h.request("PUT", f"/api/v1/leave/cancel/{pk}/", body={"reason": "Synthetic cancellation"})
    assert response.status_code == 200
    assert h.leave_detail(pk)["status"] == "cancel_requested"
    assert h.balance() == (2.0, 0.0)
    endpoint = "cancellation-approve" if approve else "cancellation-reject"
    response = h.request("PUT", f"/api/v1/leave/{endpoint}/{pk}/", "approver", {})
    assert response.status_code == 200, response.text[:500]
    assert h.leave_detail(pk)["status"] == ("cancelled" if approve else "approved")
    assert h.balance() == ((5.0, 0.0) if approve else (2.0, 0.0))
    before = h.snapshot()
    assert h.request("PUT", f"/api/v1/leave/cancel/{pk}/", body={}).status_code == 400
    assert h.request("PUT", f"/api/v1/leave/{endpoint}/{pk}/", "approver", {}).status_code == 400
    assert h.snapshot() == before


def test_repeated_allocation_approval_does_not_credit_twice(leave_http):
    h = leave_http
    h.lineage("REPEAT-ALLOCATION-APPROVE-001")
    pk = h.grant(5)
    before = h.snapshot()
    response = h.request("PUT", f"/api/v1/leave/allocation-approve/{pk}/", "approver", {})
    assert response.status_code == 400
    assert h.snapshot() == before


def test_repeated_leave_approval_does_not_debit_twice(leave_http):
    h = leave_http
    h.lineage("REPEAT-LEAVE-APPROVE-001")
    h.grant(5)
    pk = h.create_leave()
    h.approve_leave(pk)
    before = h.snapshot()
    assert h.request("PUT", f"/api/v1/leave/approve/{pk}/", "approver", {}).status_code == 400
    assert h.snapshot() == before


def test_duplicate_leave_creation_rejected_without_record(leave_http):
    h = leave_http
    h.lineage("REPEAT-LEAVE-CREATE-001")
    h.grant(5)
    body = h.baseline("leave")
    h.create_leave(body)
    before = h.snapshot()
    response = h.request("POST", "/api/v1/leave/user-request/", body=body)
    assert response.status_code == 400
    assert "already a leave request" in str(response.json()).lower()
    assert h.snapshot() == before


def test_allocation_duplicate_creation_contract(leave_http):
    """Provisional duplicate oracle: reject identical pending submission with 400.

    The brief requires no duplicates; the current endpoint has no idempotency
    contract. This explicit proposal needs owner review before a product fix.
    Keep a genuine failure visible; do not introduce deduplication in this test.
    """
    h = leave_http
    h.lineage("GAP-ALLOCATION-DUPLICATE-001")
    body = h.baseline("allocation")
    h.create_allocation(body)
    before = h.snapshot()
    response = h.request("POST", "/api/v1/leave/user-allocation-request/", body=body)
    assert response.status_code == 400, "Proposed rejection oracle requires owner decision"
    assert h.snapshot() == before


@pytest.mark.parametrize("method", ["PUT", "DELETE"])
def test_nonowner_self_allocation_route_denied(leave_http, method):
    """Expected controlled 403, matching the generic endpoint ownership rule."""
    h = leave_http
    h.lineage("DEFECT-NONOWNER-ALLOCATION-" + method)
    pk = h.create_allocation()
    before = h.snapshot()
    body = h.baseline("allocation") if method == "PUT" else {}
    response = h.request(method, f"/api/v1/leave/user-allocation-request/{pk}/", "outsider", body)
    assert response.status_code == 403, response.text[:500]
    assert h.snapshot() == before


def test_carryforward_cap_used_in_balance_validation(leave_http):
    """FR-06/BR-01 model oracle: capped carry-forward must not be overdrawn."""
    h = leave_http
    h.lineage("DEFECT-CARRYFORWARD-CAP-001")
    from leave.models import AvailableLeave, LeaveType

    leave_type = h.context["leave_type"]
    LeaveType.objects.filter(pk=leave_type.pk).update(carryforward_type="carryforward", carryforward_max=1, reset=False)
    AvailableLeave.objects.filter(employee_id=h.context["employee"], leave_type_id=leave_type).update(available_days=0, carryforward_days=5, total_leave_days=5)
    before = h.snapshot()
    response = h.request("POST", "/api/v1/leave/user-request/", body=h.baseline("leave"))
    assert response.status_code == 400, "Three days exceed effective capped balance one"
    assert "enough leave" in str(response.json()).lower()
    assert h.snapshot() == before
