"""Critical module: LeaveRequest.clean (BR-01 balance boundary, BR-02 multi-condition
acceptance) and LeaveRequest.leaveoverlapping.

Line numbers refer to leave/models.py at the sqe-team baseline. MCC/MC-DC tables
for the compound decisions are in docs/team/reports/WHITEBOX_UNIT_TESTING.md; the
`mcc` / `mcdc` ids below match the rows there.
"""

from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError

from leave.models import AvailableLeave, LeaveRequest

from .conftest import D
from .mcc_tables import feasible_rows, row_id

pytestmark = pytest.mark.django_db

FULL, FIRST, SECOND = "full_day", "first_half", "second_half"


def lr(emp, lt, start=D, end=D, sb=FULL, eb=FULL, **kw):
    return LeaveRequest(
        employee_id=emp, leave_type_id=lt, start_date=start, end_date=end,
        start_date_breakdown=sb, end_date_breakdown=eb, description="unit", reject_reason="", **kw,
    )


def existing(emp, lt, start=D, end=D, sb=FULL, eb=FULL, status="approved"):
    """Persist a request WITHOUT LeaveRequest.save() side effects."""
    return LeaveRequest.objects.bulk_create([lr(emp, lt, start, end, sb, eb, status=status)])[0]


def set_balance(al, available=5, carry=0):
    AvailableLeave.objects.filter(pk=al.pk).update(available_days=available, carryforward_days=carry)


def msg(exc):
    return " ".join(exc.value.messages)


# --- Guard and assignment (lines 2049, 2057) ------------------------------------
def test_no_leave_type_returns_early(employee, acting_as):  # 2049 T
    acting_as(employee)
    req = lr(employee, None)
    assert req.clean() is None


def test_leave_type_not_assigned_rejected(employee, leave_type, acting_as):  # 2057 T
    acting_as(employee)
    with pytest.raises(ValidationError) as e:
        lr(employee, leave_type).clean()
    assert "not assigned" in msg(e)


# --- Date validation (2069) + C1 single-day breakdown (2072) -----------------------
def test_end_before_start_rejected(employee, leave_type, available_leave, acting_as):  # 2069 T
    acting_as(employee)
    with pytest.raises(ValidationError) as e:
        lr(employee, leave_type, start=D, end=D - timedelta(1)).clean()
    assert "End date should not be less" in msg(e)


@pytest.mark.parametrize(
    "mcc,start_end_same,sb,eb,rejected",
    [
        ("C1-1 A=T B=T", True, FIRST, SECOND, True),
        ("C1-2 A=T B=F", True, FIRST, FIRST, False),
        ("C1-3 A=F B=T", False, FIRST, SECOND, False),
        ("C1-4 A=F B=F", False, FULL, FULL, False),
    ],
)
def test_c1_single_day_breakdown_mismatch_mcc(employee, leave_type, available_leave, acting_as, mcc, start_end_same, sb, eb, rejected):
    # C1 = A (start == end) AND B (start breakdown != end breakdown). MC/DC pairs: A {1,3}, B {1,2}.
    acting_as(employee)
    end = D if start_end_same else D + timedelta(1)
    req = lr(employee, leave_type, start=D, end=end, sb=sb, eb=eb)
    if rejected:
        with pytest.raises(ValidationError, match="Mismatch in the breakdown"):
            req.clean()
    else:
        req.clean()


def test_missing_end_date_crashes_before_validation(employee, leave_type, available_leave, acting_as):
    # White-box finding: end_date is nullable on the model, but clean() compares
    # start_date > end_date (line 2069) before any None check, so a missing end
    # date raises TypeError instead of a ValidationError. This is also why the
    # False branch of line 2087 ("start_date and end_date") is unreachable.
    acting_as(employee)
    with pytest.raises(TypeError):
        lr(employee, leave_type, end=None).clean()


# --- C2 attachment requirement (2081) ---------------------------------------------
@pytest.mark.parametrize(
    "mcc,require,attachment,rejected",
    [
        ("C2-1 L=T R=T N=T", "yes", None, True),
        ("C2-2 L=T R=T N=F", "yes", "doc/proof.pdf", False),
        ("C2-3 L=T R=F N=T", "no", None, False),
        ("C2-4 L=T R=F N=F", "no", "doc/proof.pdf", False),
    ],
)
def test_c2_attachment_required_mcc(employee, leave_type, available_leave, acting_as, mcc, require, attachment, rejected):
    # C2 = L (leave_type) AND R (require_attachment == "yes") AND N (no attachment).
    # L is always True here: line 2049 already returned when leave_type is falsy
    # (rows with L=F are infeasible; see MCC table).
    acting_as(employee)
    leave_type.require_attachment = require
    req = lr(employee, leave_type, attachment=attachment)
    if rejected:
        with pytest.raises(ValidationError, match="attachment is required"):
            req.clean()
    else:
        req.clean()


# --- Overlap (2087-2092) + leaveoverlapping ---------------------------------------
def test_overlap_with_active_request_rejected(employee, leave_type, available_leave, acting_as):  # 2089 T
    acting_as(employee)
    existing(employee, leave_type, D, D + timedelta(1), status="requested")
    with pytest.raises(ValidationError, match="already has a leave request"):
        lr(employee, leave_type, start=D + timedelta(1), end=D + timedelta(2)).clean()


@pytest.mark.parametrize("status", ["cancelled", "rejected"])
def test_overlap_with_cancelled_or_rejected_request_allowed(employee, leave_type, available_leave, acting_as, status):  # 2089 F
    acting_as(employee)
    existing(employee, leave_type, D, D, status=status)
    lr(employee, leave_type).clean()


def test_overlap_boundary_adjacent_day_is_not_overlap(employee, leave_type, available_leave, acting_as):
    # BVA on the overlap window: existing ends on D, new starts D+1.
    acting_as(employee)
    existing(employee, leave_type, D - timedelta(1), D)
    lr(employee, leave_type, start=D + timedelta(1), end=D + timedelta(1)).clean()


# leaveoverlapping half-day exception (line 1969):
# H = c1 and c2 and c3 and c4 and c5 (conditions listed in MCC_MCDC_TABLES.md).
# When H is true the two half days are complementary and no overlap is reported.
# Complete MCC: every feasible row of the generated table is executed.
def _h_case(v):
    c1, c2, c3, c4, c5 = v
    if c2 and c3:
        e_sb, s_sb = (FIRST, SECOND) if c4 else (FIRST, FIRST)
    elif not c2 and not c3:
        e_sb, s_sb = FULL, FULL
    elif not c2:
        e_sb, s_sb = FULL, SECOND
    else:
        e_sb, s_sb = FIRST, FULL
    e_eb, s_eb = (FIRST, SECOND) if c5 else (SECOND, SECOND)
    return (0 if c1 else -1), e_sb, e_eb, s_sb, s_eb


@pytest.mark.parametrize("row", feasible_rows("H"), ids=row_id)
def test_leaveoverlapping_half_day_exception_mcc(employee, leave_type, row):
    offset, e_sb, e_eb, s_sb, s_eb = _h_case(row["v"])
    # Existing request spans D+offset..D, so every row overlaps by date; only H decides.
    existing(employee, leave_type, D + timedelta(offset), D, sb=e_sb, eb=e_eb)
    new = lr(employee, leave_type, start=D, end=D, sb=s_sb, eb=s_eb)
    assert new.leaveoverlapping().exists() is (not row["out"])


def test_leaveoverlapping_no_existing_requests(employee, leave_type):  # 1965 F
    assert not lr(employee, leave_type).leaveoverlapping().exists()


# --- C3 past-date restriction (2097, 2106) -----------------------------------------
@pytest.mark.parametrize(
    "mcc,restrict_on,past,rejected",
    [
        ("C3-1 R=T P=T", True, True, True),
        ("C3-2 R=T P=F", True, False, False),
        ("C3-3 R=F P=T", False, True, False),
        ("C3-4 R=F P=F", False, False, False),
    ],
)
def test_c3_past_date_restriction_mcc(employee, leave_type, available_leave, company, acting_as, mcc, restrict_on, past, rejected):
    from leave.models import EmployeePastLeaveRestrict

    acting_as(employee)
    if restrict_on:
        EmployeePastLeaveRestrict.objects.create(enabled=True, company_id=company)
    start = date.today() - timedelta(1) if past else date.today() + timedelta(30)
    req = lr(employee, leave_type, start=start, end=start)
    if rejected:
        with pytest.raises(ValidationError, match="past dates"):
            req.clean()
    else:
        req.clean()


def test_past_date_boundary_today_is_allowed(employee, leave_type, available_leave, company, acting_as):
    from leave.models import EmployeePastLeaveRestrict

    acting_as(employee)
    EmployeePastLeaveRestrict.objects.create(enabled=True, company_id=company)
    lr(employee, leave_type, start=date.today(), end=date.today()).clean()  # start < today is False


def test_superuser_skips_past_date_restriction(admin_employee, leave_type, company, acting_as):  # 2097 F
    from leave.models import EmployeePastLeaveRestrict

    AvailableLeave.objects.create(employee_id=admin_employee, leave_type_id=leave_type, available_days=5)
    EmployeePastLeaveRestrict.objects.create(enabled=True, company_id=company)
    acting_as(admin_employee)
    past = date.today() - timedelta(1)
    lr(admin_employee, leave_type, start=past, end=past).clean()


# --- BR-01 balance boundary (2128, 2151-2158) -------------------------------------
def test_zero_effective_days_rejected(employee, leave_type, available_leave, acting_as):  # 2128 T
    from base.models import Holidays

    acting_as(employee)
    leave_type.exclude_holiday = "yes"
    Holidays.objects.create(name="Unit holiday", start_date=D, end_date=D)
    with pytest.raises(ValidationError, match="requested days for this leave type is zero"):
        lr(employee, leave_type).clean()


@pytest.mark.parametrize(
    "bva,days,rejected",
    [("below (4 < 5)", 4, False), ("at (5 = 5)", 5, False), ("above (6 > 5)", 6, True)],
)
def test_balance_boundary_bva(employee, leave_type, available_leave, acting_as, bva, days, rejected):
    # BR-01: effective days <= available (5) + capped carry-forward (0) + forecast (0).
    acting_as(employee)
    req = lr(employee, leave_type, start=D, end=D + timedelta(days - 1))
    if rejected:
        with pytest.raises(ValidationError, match="sufficient leave balance"):
            req.clean()
    else:
        req.clean()


def test_half_day_just_above_balance_rejected(employee, leave_type, available_leave, acting_as):
    # BVA in 0.5-day steps: 5.5 > 5.
    acting_as(employee)
    req = lr(employee, leave_type, start=D, end=D + timedelta(5), sb=FULL, eb=FIRST)
    with pytest.raises(ValidationError, match="sufficient leave balance"):
        req.clean()


@pytest.mark.parametrize(
    "path,cf_type,cf_max,carry,days,rejected",
    [
        ("2151 T: carry capped at max (5+2=7 ok)", "carryforward", 2, 4, 7, False),
        ("2151 T: cap enforced (8 > 5+2)", "carryforward", 2, 4, 8, True),
        ("2151 T: expire type also capped", "carryforward expire", 2, 4, 8, True),
        ("2151 T: carry below max used fully", "carryforward", 10, 1, 6, False),
        ("2153 T: no carryforward ignores stored carry", "no carryforward", 10, 4, 6, True),
        ("2153 F: unknown type keeps stored carry uncapped", "legacy", 0, 4, 9, False),
    ],
)
def test_carryforward_types(employee, leave_type, available_leave, acting_as, path, cf_type, cf_max, carry, days, rejected):
    from leave.models import LeaveType

    acting_as(employee)
    LeaveType.objects.filter(pk=leave_type.pk).update(carryforward_type=cf_type, carryforward_max=cf_max)
    set_balance(available_leave, available=5, carry=carry)
    leave_type.refresh_from_db()
    req = lr(employee, leave_type, start=D, end=D + timedelta(days - 1))
    if rejected:
        with pytest.raises(ValidationError, match="sufficient leave balance"):
            req.clean()
    else:
        req.clean()


# --- Superuser return (2171) and restricted-leave loop (2175-2203) ------------------
def test_superuser_skips_restricted_dates(admin_employee, leave_type, department, acting_as):  # 2171 T
    from leave.models import RestrictLeave

    AvailableLeave.objects.create(employee_id=admin_employee, leave_type_id=leave_type, available_days=5)
    r = RestrictLeave.objects.create(title="Freeze", start_date=D, end_date=D, include_all=True)
    r.department.add(department)
    acting_as(admin_employee)
    lr(admin_employee, leave_type).clean()


def make_restriction(*, include_all=False, excluded=(), specific=(), start=D, end=D, departments=(), jobs=()):
    from leave.models import RestrictLeave

    r = RestrictLeave.objects.create(title="Freeze", start_date=start, end_date=end, include_all=include_all)
    r.exclued_leave_types.set(excluded)
    r.spesific_leave_types.set(specific)
    r.department.set(departments)
    r.job_position.set(jobs)
    return r


def test_no_restrictions_configured(employee, leave_type, available_leave, acting_as):  # 2175 loop not entered
    acting_as(employee)
    lr(employee, leave_type).clean()


# C4: which leave types a restriction applies to (2182 / 2184 / 2186 chain)
@pytest.mark.parametrize(
    "path,include_all,excluded_self,excluded_other,specific_self,applies",
    [
        ("2182 T: include_all, nothing excluded", True, False, False, False, True),
        ("2184 T: other type excluded, ours not", False, False, True, False, True),
        ("2184 F (2nd cond) -> 2186 F: ours excluded", True, True, False, False, False),
        ("2186 T: ours specifically listed", False, False, False, True, True),
        ("2186 F: nothing matches", False, False, False, False, False),
    ],
)
def test_c4_restriction_applicability(employee, leave_type, available_leave, department, company, acting_as, path, include_all, excluded_self, excluded_other, specific_self, applies):
    from leave.models import LeaveType

    acting_as(employee)
    other = LeaveType.objects.create(name="Other type", total_days=1, company_id=company)
    excluded = ([leave_type] if excluded_self else []) + ([other] if excluded_other else [])
    make_restriction(include_all=include_all, excluded=excluded, specific=[leave_type] if specific_self else [], departments=[department])
    req = lr(employee, leave_type)
    if applies:
        with pytest.raises(ValidationError, match="dates are restricted"):
            req.clean()
    else:
        req.clean()


def test_restriction_with_empty_date_range_is_skipped(employee, leave_type, available_leave, department, acting_as):  # 2193 T
    acting_as(employee)
    make_restriction(include_all=True, start=D, end=D - timedelta(1), departments=[department])
    lr(employee, leave_type).clean()


def test_restriction_on_other_dates_does_not_block(employee, leave_type, available_leave, department, acting_as):  # 2197 F
    acting_as(employee)
    make_restriction(include_all=True, start=D + timedelta(10), end=D + timedelta(12), departments=[department])
    lr(employee, leave_type).clean()


def test_restriction_boundary_first_restricted_day_blocks(employee, leave_type, available_leave, department, acting_as):
    # BVA on the restricted window: request ends on its first day.
    acting_as(employee)
    make_restriction(include_all=True, start=D + timedelta(1), end=D + timedelta(3), departments=[department])
    with pytest.raises(ValidationError, match="dates are restricted"):
        lr(employee, leave_type, start=D, end=D + timedelta(1)).clean()


# C5 (2198-2202): (Dp and InDept and NoJobs) or (Jb and InJobs).
# Complete MCC: every feasible row of the generated table (15 of 32) is executed;
# the MC/DC pairs are a subset of these rows (see MCC_MCDC_TABLES.md).
@pytest.mark.parametrize("row", feasible_rows("C5"), ids=row_id)
def test_c5_restriction_targets_department_or_job_mcc(acting_as, company, department, job, leave_type, row):
    from base.models import Department, JobPosition

    from .conftest import make_employee

    dp, in_dept, no_jobs, jb, in_jobs = row["v"]
    other_dept = Department.objects.create(department="Finance")
    other_job = JobPosition.objects.create(job_position="Accountant", department_id=other_dept)
    emp = make_employee(
        "Mcc", "mcc@unit.test", company=company,
        department=department if dp else None, job=job if jb else None,
    )
    AvailableLeave.objects.create(employee_id=emp, leave_type_id=leave_type, available_days=5)
    make_restriction(
        include_all=True,
        departments=[department if in_dept else other_dept],
        jobs=[] if no_jobs else [job if in_jobs else other_job],
    )
    acting_as(emp)
    req = lr(emp, leave_type)
    if row["out"]:
        with pytest.raises(ValidationError, match="dates are restricted"):
            req.clean()
    else:
        req.clean()


def test_employee_without_work_info_is_not_blocked(employee, leave_type, available_leave, department, acting_as):  # 2167/2168 else
    from employee.models import EmployeeWorkInformation

    acting_as(employee)
    EmployeeWorkInformation.objects.filter(employee_id=employee).delete()
    make_restriction(include_all=True, departments=[department])
    lr(employee, leave_type).clean()


def test_valid_request_passes_all_checks(employee, leave_type, available_leave, acting_as):
    acting_as(employee)
    assert lr(employee, leave_type, start=D, end=D + timedelta(2)).clean() is None
