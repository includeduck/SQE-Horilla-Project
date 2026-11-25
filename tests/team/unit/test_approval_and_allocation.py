"""BR-03 state changes and balance arithmetic in the leave API layer, BR-04 ownership.

Units: LeaveAllocationRequest.clean, LeaveRequestApproveAPIView.leave_approve_calculation,
LeaveRequestRejectAPIView.leave_calculation/put, LeaveAllocationApproveAPIView,
LeaveAllocationRequestRejectAPIView, EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request.
Views are called through DRF's APIRequestFactory as a superuser approver (the
decorator's own access rules are covered by the Area 3 access matrix).
"""

import pytest
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIRequestFactory, force_authenticate

from horilla_api.api_views.leave import views as api
from leave.models import AvailableLeave, LeaveAllocationRequest, LeaveRequest

from .conftest import D

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


def call(view_cls, user_emp, pk, data=None):
    request = factory.put(f"/x/{pk}/", data or {}, format="json")
    force_authenticate(request, user=user_emp.employee_user_id)
    return view_cls.as_view()(request, pk=pk)


def allocation(emp, lt, days=3, status="requested"):
    return LeaveAllocationRequest.objects.create(
        employee_id=emp, leave_type_id=lt, requested_days=days, description="unit", reject_reason="", status=status
    )


def leave_req(emp, lt, days=2, status="approved", approved_available=0, approved_carry=0):
    return LeaveRequest.objects.bulk_create([
        LeaveRequest(
            employee_id=emp, leave_type_id=lt, start_date=D, end_date=D, requested_days=days,
            description="unit", reject_reason="", status=status,
            approved_available_days=approved_available, approved_carryforward_days=approved_carry,
        )
    ])[0]


def balance(emp, lt):
    al = AvailableLeave.objects.get(employee_id=emp, leave_type_id=lt)
    return al.available_days, al.carryforward_days


# --- LeaveAllocationRequest.clean (BR-03: editable only while requested) ----------
def test_allocation_clean_allows_requested(employee, leave_type):  # 2489 F
    allocation(employee, leave_type).clean()


@pytest.mark.parametrize("status", ["approved", "rejected"])
def test_allocation_clean_blocks_after_decision(employee, leave_type, status):  # 2489 T
    with pytest.raises(ValidationError, match="cannot be edited"):
        allocation(employee, leave_type, status=status).clean()


# --- leave_approve_calculation (BR-01 deduction split) ----------------------------
@pytest.mark.parametrize(
    "bva,available,carry,days,exp_available,exp_carry,exp_from_avail,exp_from_carry",
    [
        ("below: 2 < 5 from available only", 5, 3, 2, 3, 3, 2, 0),
        ("at: 5 = 5 uses all available, no carry", 5, 3, 5, 0, 3, 5, 0),
        ("above: 6 > 5 spills 1 into carry-forward", 5, 3, 6, 0, 2, 5, 1),
    ],
)
def test_leave_approve_calculation_split(employee, leave_type, available_leave, bva, available, carry, days, exp_available, exp_carry, exp_from_avail, exp_from_carry):
    AvailableLeave.objects.filter(pk=available_leave.pk).update(available_days=available, carryforward_days=carry)
    available_leave.refresh_from_db()
    req = leave_req(employee, leave_type, days=days, status="requested")
    api.LeaveRequestApproveAPIView().leave_approve_calculation(req, available_leave)
    assert balance(employee, leave_type) == (exp_available, exp_carry)
    assert (req.approved_available_days, req.approved_carryforward_days) == (exp_from_avail, exp_from_carry)


# --- LeaveRequestRejectAPIView.put / leave_calculation (BR-03) ---------------------
def test_reject_approved_leave_refunds_requester(employee, leave_type, available_leave, admin_employee):
    # Regression for A2-D01 (#4): refund must go to the requester, not the approver.
    AvailableLeave.objects.filter(pk=available_leave.pk).update(available_days=1, carryforward_days=0)
    req = leave_req(employee, leave_type, days=4, approved_available=3, approved_carry=1)
    resp = call(api.LeaveRequestRejectAPIView, admin_employee, req.pk, {"reason": "  Busy period  "})
    assert resp.status_code == 200
    req.refresh_from_db()
    assert req.status == "rejected"
    assert req.reject_reason == "Busy period"
    assert (req.approved_available_days, req.approved_carryforward_days) == (0, 0)
    assert balance(employee, leave_type) == (4, 1)


def test_reject_without_reason_keeps_reason_empty(employee, leave_type, available_leave, admin_employee):  # 850 F
    req = leave_req(employee, leave_type, status="requested")
    assert call(api.LeaveRequestRejectAPIView, admin_employee, req.pk).status_code == 200
    req.refresh_from_db()
    assert req.status == "rejected" and req.reject_reason == ""


def test_reject_pending_cancellation_is_refused(employee, leave_type, available_leave, admin_employee):  # 844 T
    req = leave_req(employee, leave_type, status="cancel_requested")
    resp = call(api.LeaveRequestRejectAPIView, admin_employee, req.pk)
    assert resp.status_code == 400
    req.refresh_from_db()
    assert req.status == "cancel_requested"


def test_reject_already_rejected_is_refused(employee, leave_type, available_leave, admin_employee):  # 848 F
    req = leave_req(employee, leave_type, status="rejected")
    before = balance(employee, leave_type)
    resp = call(api.LeaveRequestRejectAPIView, admin_employee, req.pk)
    assert resp.status_code == 400
    assert balance(employee, leave_type) == before


@pytest.mark.xfail(strict=True, reason="Known defect OD-01: rejecting a cancelled leave is accepted (BR-03 terminal state)")
def test_reject_cancelled_leave_is_refused(employee, leave_type, available_leave, admin_employee):
    req = leave_req(employee, leave_type, status="cancelled")
    resp = call(api.LeaveRequestRejectAPIView, admin_employee, req.pk)
    assert resp.status_code == 400


# --- LeaveAllocationApproveAPIView (BR-03) ----------------------------------------
def test_approve_allocation_credits_balance(employee, leave_type, available_leave, admin_employee):  # 969 T
    alloc = allocation(employee, leave_type, days=3)
    assert call(api.LeaveAllocationApproveAPIView, admin_employee, alloc.pk).status_code == 200
    alloc.refresh_from_db()
    assert alloc.status == "approved"
    assert balance(employee, leave_type)[0] == 8


def test_approve_allocation_creates_balance_row_when_missing(employee, leave_type, admin_employee):
    # get_or_create branch: no AvailableLeave yet for this type.
    alloc = allocation(employee, leave_type, days=2)
    assert call(api.LeaveAllocationApproveAPIView, admin_employee, alloc.pk).status_code == 200
    assert balance(employee, leave_type)[0] == 2


@pytest.mark.parametrize("status", ["approved", "rejected"])
def test_approve_allocation_twice_or_after_reject_refused(employee, leave_type, available_leave, admin_employee, status):  # 969 F
    alloc = allocation(employee, leave_type, days=3, status=status)
    resp = call(api.LeaveAllocationApproveAPIView, admin_employee, alloc.pk)
    assert resp.status_code == 400
    assert balance(employee, leave_type)[0] == 5  # not credited twice


# --- LeaveAllocationRequestRejectAPIView (BR-03) ----------------------------------
def test_reject_requested_allocation_leaves_balance(employee, leave_type, available_leave, admin_employee):  # 987 F, 1011 F
    alloc = allocation(employee, leave_type, days=3)
    assert call(api.LeaveAllocationRequestRejectAPIView, admin_employee, alloc.pk).status_code == 200
    alloc.refresh_from_db()
    assert alloc.status == "rejected" and alloc.reject_reason == ""
    assert balance(employee, leave_type)[0] == 5


@pytest.mark.parametrize(
    "bva,available,days,expected",
    [("balance above allocation", 5, 3, 2), ("balance equals allocation", 3, 3, 0), ("balance below allocation floors at 0", 2, 3, 0)],
)
def test_reject_approved_allocation_takes_days_back(employee, leave_type, available_leave, admin_employee, bva, available, days, expected):  # 987 T, 1011 T
    AvailableLeave.objects.filter(pk=available_leave.pk).update(available_days=available)
    alloc = allocation(employee, leave_type, days=days, status="approved")
    assert call(api.LeaveAllocationRequestRejectAPIView, admin_employee, alloc.pk, {"reason": "Over-allocated"}).status_code == 200
    alloc.refresh_from_db()
    assert alloc.reject_reason == "Over-allocated"
    assert balance(employee, leave_type)[0] == expected


def test_reject_rejected_allocation_refused(employee, leave_type, available_leave, admin_employee):  # 1007 F
    alloc = allocation(employee, leave_type, status="rejected")
    assert call(api.LeaveAllocationRequestRejectAPIView, admin_employee, alloc.pk).status_code == 400


# --- get_allocation_request (BR-04 ownership) -------------------------------------
def _owner_request(emp):
    from django.contrib.auth.models import AnonymousUser

    request = factory.get("/x/")
    request.user = emp.employee_user_id if emp else AnonymousUser()
    return request


def test_owner_gets_own_allocation(employee, leave_type):  # 1165 T
    alloc = allocation(employee, leave_type)
    assert api.EmployeeLeaveAllocationUpdateDeleteAPIView().get_allocation_request(_owner_request(employee), alloc.pk) == alloc


def test_non_owner_denied(employee, other_employee, leave_type):  # 1165 F (A2-D02 fix)
    alloc = allocation(employee, leave_type)
    with pytest.raises(PermissionDenied):
        api.EmployeeLeaveAllocationUpdateDeleteAPIView().get_allocation_request(_owner_request(other_employee), alloc.pk)


def test_anonymous_user_gets_404(employee, leave_type):  # 1161 T
    from django.http import Http404

    alloc = allocation(employee, leave_type)
    with pytest.raises(Http404):
        api.EmployeeLeaveAllocationUpdateDeleteAPIView().get_allocation_request(_owner_request(None), alloc.pk)


def test_missing_allocation_is_validation_error(employee):  # DoesNotExist
    with pytest.raises(serializers.ValidationError):
        api.EmployeeLeaveAllocationUpdateDeleteAPIView().get_allocation_request(_owner_request(employee), 999_999)
