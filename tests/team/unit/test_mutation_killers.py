"""Tests added after mutation analysis (docs/team/reports/MUTATION_TESTING.md).

Each test names the surviving mutant(s) S## from the first mutmut run that it
kills. Two groups:
  * weak assertions: rejection paths are now checked with the exact message and
    the exact field key, not a substring;
  * missing tests: query filters, defaults (`or 0`), the forecast term and the
    restriction loop's `continue`, which no earlier test could tell apart.
"""

from datetime import date, timedelta
from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from horilla_api.api_views.leave import views as api
from leave.models import AvailableLeave, LeaveType

from .conftest import D, make_employee
from .test_approval_and_allocation import _owner_request, allocation, call, leave_req
from .test_leave_request_clean import FIRST, FULL, existing, lr, make_restriction

pytestmark = pytest.mark.django_db


def rejects(req, *, messages=None, message_dict=None):
    with pytest.raises(ValidationError) as e:
        req.clean()
    if messages is not None:
        assert e.value.messages == messages
    if message_dict is not None:
        assert e.value.message_dict == message_dict


def set_balance(emp, lt, available=None, carry=None):
    fields = {k: v for k, v in (("available_days", available), ("carryforward_days", carry)) if v is not None}
    AvailableLeave.objects.filter(employee_id=emp, leave_type_id=lt).update(**fields)


# --- Exact messages and field keys (weak-assertion survivors) ----------------------
def test_exact_not_assigned_message_and_field(employee, leave_type, acting_as):  # S27-S30
    acting_as(employee)
    rejects(lr(employee, leave_type), message_dict={"leave_type_id": ["The selected leave type is not assigned to this employee."]})


def test_exact_end_before_start_message(employee, leave_type, available_leave, acting_as):  # S31
    acting_as(employee)
    rejects(lr(employee, leave_type, end=D - timedelta(1)), messages=["End date should not be less than start date."])


def test_exact_breakdown_mismatch_message(employee, leave_type, available_leave, acting_as):  # S32
    acting_as(employee)
    rejects(lr(employee, leave_type, sb=FIRST, eb=FULL), messages=["Mismatch in the breakdown of the start and end date."])


def test_exact_attachment_message_and_field(employee, leave_type, available_leave, acting_as):  # S33-S36
    acting_as(employee)
    leave_type.require_attachment = "yes"
    rejects(lr(employee, leave_type), message_dict={"attachment": ["An attachment is required for this leave request"]})


def test_exact_overlap_message(employee, leave_type, available_leave, acting_as):  # S39-S40
    acting_as(employee)
    existing(employee, leave_type, status="requested")
    rejects(lr(employee, leave_type), messages=["Employee already has a leave request for this date range."])


def test_exact_past_date_message(employee, leave_type, available_leave, company, acting_as):  # S43-S44
    from leave.models import EmployeePastLeaveRestrict

    acting_as(employee)
    EmployeePastLeaveRestrict.objects.create(enabled=True, company_id=company)
    past = date.today() - timedelta(1)
    rejects(lr(employee, leave_type, start=past, end=past), messages=["Requests cannot be made for past dates."])


def test_exact_zero_days_message(employee, leave_type, available_leave, acting_as):  # S51-S52
    from base.models import Holidays

    acting_as(employee)
    leave_type.exclude_holiday = "yes"
    Holidays.objects.create(name="Unit holiday", start_date=D, end_date=D)
    rejects(lr(employee, leave_type), messages=[
        "The requested days for this leave type is zero. Please check the selected dates, breakdown and "
        "the leave type's holiday/company leave exclusion settings."
    ])


def test_exact_insufficient_balance_message(employee, leave_type, available_leave, acting_as):  # S62-S63
    acting_as(employee)
    rejects(lr(employee, leave_type, end=D + timedelta(5)), messages=["Does not have sufficient leave balance for the requested dates."])


def test_exact_restricted_message(employee, leave_type, available_leave, department, acting_as):  # S67-S68
    acting_as(employee)
    make_restriction(include_all=True, departments=[department])
    rejects(lr(employee, leave_type), messages=[
        "You cannot request leave for this date range. The requested dates are restricted. Please contact admin."
    ])


@pytest.mark.parametrize("status", ["approved", "rejected"])
def test_exact_allocation_edit_lock_message(employee, leave_type, status):  # S20-S21
    with pytest.raises(ValidationError) as e:
        allocation(employee, leave_type, status=status).clean()
    assert e.value.messages == ["This form cannot be edited because the status is Requested / Rejected."]


def test_exact_ownership_errors(employee, other_employee, leave_type):  # S01-S09
    view = api.EmployeeLeaveAllocationUpdateDeleteAPIView()
    alloc = allocation(employee, leave_type)
    with pytest.raises(PermissionDenied) as denied:
        view.get_allocation_request(_owner_request(other_employee), alloc.pk)
    assert denied.value.detail == "Access Denied.."
    with pytest.raises(Http404) as nf:
        view.get_allocation_request(_owner_request(None), alloc.pk)
    assert nf.value.args == ("AnonymousUser",)  # DRF returns this as the 404 detail
    with pytest.raises(serializers.ValidationError) as missing:
        view.get_allocation_request(_owner_request(employee), 999_999)
    assert "does not exist" in str(missing.value.detail[0])


# --- Query filters (missing-test survivors) ----------------------------------------
@pytest.fixture
def second_type(company):
    return LeaveType.objects.create(name="Unit Sick", total_days=5, company_id=company)


def test_not_assigned_even_if_other_rows_exist(employee, other_employee, leave_type, second_type, acting_as):  # S25-S26
    # Employee has a *different* type; another employee has *this* type.
    AvailableLeave.objects.create(employee_id=employee, leave_type_id=second_type, available_days=5)
    AvailableLeave.objects.create(employee_id=other_employee, leave_type_id=leave_type, available_days=5)
    acting_as(employee)
    rejects(lr(employee, leave_type), message_dict={"leave_type_id": ["The selected leave type is not assigned to this employee."]})


def test_balance_lookup_uses_employee_and_type(employee, other_employee, leave_type, second_type, available_leave, acting_as):  # S45-S46
    AvailableLeave.objects.create(employee_id=employee, leave_type_id=second_type, available_days=0)
    AvailableLeave.objects.create(employee_id=other_employee, leave_type_id=leave_type, available_days=0)
    acting_as(employee)
    lr(employee, leave_type, end=D + timedelta(4)).clean()  # uses exactly its own 5-day row


def test_reject_leave_refunds_only_matching_row(employee, other_employee, leave_type, second_type, available_leave, admin_employee):  # S13-S15
    AvailableLeave.objects.create(employee_id=employee, leave_type_id=second_type, available_days=7, carryforward_days=7)
    AvailableLeave.objects.create(employee_id=other_employee, leave_type_id=leave_type, available_days=7, carryforward_days=7)
    set_balance(employee, leave_type, available=1, carry=2)
    req = leave_req(employee, leave_type, days=3, approved_available=2, approved_carry=1)
    assert call(api.LeaveRequestRejectAPIView, admin_employee, req.pk).status_code == 200
    assert AvailableLeave.objects.get(employee_id=employee, leave_type_id=leave_type).carryforward_days == 3  # 2 + 1, not = 1
    assert AvailableLeave.objects.get(employee_id=employee, leave_type_id=leave_type).available_days == 3
    assert AvailableLeave.objects.get(employee_id=employee, leave_type_id=second_type).available_days == 7
    assert AvailableLeave.objects.get(employee_id=other_employee, leave_type_id=leave_type).available_days == 7


def test_reject_approved_allocation_debits_only_matching_row(employee, other_employee, leave_type, second_type, admin_employee):  # S10-S11
    # Unrelated rows are created first, so a filter missing either field would pick one of them.
    AvailableLeave.objects.create(employee_id=other_employee, leave_type_id=leave_type, available_days=9)
    AvailableLeave.objects.create(employee_id=employee, leave_type_id=second_type, available_days=9)
    AvailableLeave.objects.create(employee_id=employee, leave_type_id=leave_type, available_days=5)
    alloc = allocation(employee, leave_type, days=3, status="approved")
    assert call(api.LeaveAllocationRequestRejectAPIView, admin_employee, alloc.pk).status_code == 200
    assert AvailableLeave.objects.get(employee_id=employee, leave_type_id=leave_type).available_days == 2
    assert AvailableLeave.objects.get(employee_id=other_employee, leave_type_id=leave_type).available_days == 9
    assert AvailableLeave.objects.get(employee_id=employee, leave_type_id=second_type).available_days == 9


def test_disabled_past_date_restriction_is_ignored(employee, leave_type, available_leave, company, acting_as):  # S41
    from leave.models import EmployeePastLeaveRestrict

    EmployeePastLeaveRestrict.objects.create(enabled=False, company_id=company)
    acting_as(employee)
    past = date.today() - timedelta(1)
    lr(employee, leave_type, start=past, end=past).clean()


def test_past_date_restriction_of_other_company_is_ignored(employee, leave_type, available_leave, acting_as):  # S42
    from base.models import Company
    from leave.models import EmployeePastLeaveRestrict

    other = Company.objects.create(company="Other Co", hq=False, country="PK", state="ICT", city="Isb", zip="44001")
    EmployeePastLeaveRestrict.objects.create(enabled=True, company_id=other)
    acting_as(employee)
    past = date.today() - timedelta(1)
    lr(employee, leave_type, start=past, end=past).clean()


def test_other_employees_request_is_not_an_overlap(employee, other_employee, leave_type):  # S70
    existing(other_employee, leave_type, D, D)
    assert not lr(employee, leave_type).leaveoverlapping().exists()


def test_existing_request_after_new_end_is_not_an_overlap(employee, leave_type):  # S71
    existing(employee, leave_type, D + timedelta(5), D + timedelta(6))
    assert not lr(employee, leave_type, start=D, end=D + timedelta(1)).leaveoverlapping().exists()


def test_saved_request_does_not_overlap_itself(employee, leave_type):  # S69
    saved = existing(employee, leave_type, D, D)
    assert not saved.leaveoverlapping().exists()


# --- Day counting inputs passed from clean() ---------------------------------------
def test_end_breakdown_is_passed_to_day_count(employee, leave_type, available_leave, acting_as):  # S47
    set_balance(employee, leave_type, available=1.5)
    acting_as(employee)
    rejects(lr(employee, leave_type, end=D + timedelta(1)), messages=["Does not have sufficient leave balance for the requested dates."])


def test_end_date_is_passed_to_effective_day_count(employee, leave_type, available_leave, acting_as):  # S48
    from base.models import Holidays

    leave_type.exclude_holiday = "yes"
    Holidays.objects.create(name="Second day holiday", start_date=D + timedelta(1), end_date=D + timedelta(1))
    set_balance(employee, leave_type, available=1)
    acting_as(employee)
    lr(employee, leave_type, end=D + timedelta(1)).clean()  # 2 days minus 1 holiday = 1


def test_specific_holiday_of_other_employee_is_not_excluded(employee, other_employee, leave_type, available_leave, acting_as):  # S49-S50
    from base.models import Holidays

    leave_type.exclude_holiday = "yes"
    h = Holidays.objects.create(name="Their holiday", start_date=D, end_date=D, is_specific=True)
    h.employees.add(other_employee)
    acting_as(employee)
    lr(employee, leave_type).clean()  # 1 day stays 1 day, not 0


def test_specific_holiday_of_this_employee_is_excluded(employee, leave_type):  # S16
    from base.models import Holidays
    from leave.models import cal_effective_requested_days

    leave_type.exclude_holiday = "yes"
    h = Holidays.objects.create(name="My holiday", start_date=D, end_date=D, is_specific=True)
    h.employees.add(employee)
    assert cal_effective_requested_days(D, D, leave_type, 1, employee=employee) == 0


def test_company_leave_dates_called_with_request_range(leave_type):  # S17-S19
    from leave.models import cal_effective_requested_days

    with mock.patch("leave.models.company_leave_dates_list", return_value=[]) as co:
        cal_effective_requested_days(D, D + timedelta(3), leave_type, 4)
    args = co.call_args.args
    assert args[1:] == (D, D + timedelta(3))


# --- Defaults and the forecast term (BR-01) ----------------------------------------
@pytest.mark.parametrize(
    "case,cf_type,cf_max,available,carry,days",
    [
        ("S57 available 0 is not treated as 1", "no carryforward", None, 0, 0, 1),
        ("S58 carry 0 is not treated as 1", "carryforward", 5, 2, 0, 3),
        ("S59 missing carry max caps carry at 0, not 1", "carryforward", None, 2, 3, 3),
    ],
)
def test_balance_defaults_do_not_add_a_day(employee, leave_type, available_leave, acting_as, case, cf_type, cf_max, available, carry, days):
    LeaveType.objects.filter(pk=leave_type.pk).update(carryforward_type=cf_type, carryforward_max=cf_max)
    leave_type.refresh_from_db()
    set_balance(employee, leave_type, available=available, carry=carry)
    acting_as(employee)
    rejects(lr(employee, leave_type, end=D + timedelta(days - 1)), messages=["Does not have sufficient leave balance for the requested dates."])


# --- Restriction loop: continue, not break (S65, S66) --------------------------------
def test_unrelated_restriction_does_not_stop_later_checks(employee, leave_type, available_leave, department, company, acting_as):  # S65
    other_type = LeaveType.objects.create(name="Unrelated", total_days=1, company_id=company)
    make_restriction(specific=[other_type], departments=[department])  # not restricted for our type
    make_restriction(include_all=True, departments=[department])  # restricted
    acting_as(employee)
    rejects(lr(employee, leave_type), messages=[
        "You cannot request leave for this date range. The requested dates are restricted. Please contact admin."
    ])


def test_empty_restriction_does_not_stop_later_checks(employee, leave_type, available_leave, department, acting_as):  # S66
    make_restriction(include_all=True, start=D, end=D - timedelta(1), departments=[department])  # no days
    make_restriction(include_all=True, departments=[department])
    acting_as(employee)
    rejects(lr(employee, leave_type), messages=[
        "You cannot request leave for this date range. The requested dates are restricted. Please contact admin."
    ])
