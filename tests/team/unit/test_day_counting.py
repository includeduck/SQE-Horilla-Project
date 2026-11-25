"""BR-01 day counting: calculate_requested_days, leave_requested_dates,
cal_effective_requested_days, AvailableLeave.forcasted_leaves.

White-box: every test names the path / branch outcome it covers.
"""

from datetime import date, timedelta
from unittest import mock

import pytest

from leave.methods import calculate_requested_days
from leave.models import cal_effective_requested_days, leave_requested_dates

from .conftest import D

FULL, FIRST, SECOND = "full_day", "first_half", "second_half"


# --- calculate_requested_days: V(G) = 6 (see SONARQUBE_BASELINE.md §6) -------
# D1 same day? | D2 start full? | D3 end full? (D2 && D3) | D4 start full? | D5 end full?
@pytest.mark.parametrize(
    "path,start,end,sb,eb,expected",
    [
        ("P1 D1=T D2=T D3=T", D, D, FULL, FULL, 1),
        ("P2 D1=T D2=F (short-circuit)", D, D, FIRST, FULL, 0.5),
        ("P3 D1=T D2=T D3=F", D, D, FULL, SECOND, 0.5),
        ("P4 D1=F D4=T D5=T", D, D + timedelta(2), FULL, FULL, 3),
        ("P5 D1=F D4=F D5=T", D, D + timedelta(2), SECOND, FULL, 2.5),
        ("P6 D1=F D4=T D5=F", D, D + timedelta(2), FULL, FIRST, 2.5),
        ("P7 D1=F D4=F D5=F", D, D + timedelta(1), SECOND, FIRST, 1),
    ],
)
def test_calculate_requested_days_paths(path, start, end, sb, eb, expected):
    assert calculate_requested_days(start, end, sb, eb) == expected


def test_calculate_requested_days_adjacent_full_days_has_zero_middle_days():
    # BVA on the multi-day branch: smallest span (end = start + 1).
    assert calculate_requested_days(D, D + timedelta(1), FULL, FULL) == 2


# --- leave_requested_dates ----------------------------------------------------
def test_leave_requested_dates_end_none_means_single_day():
    assert leave_requested_dates(D, None) == [D]


def test_leave_requested_dates_inclusive_range():
    assert leave_requested_dates(D, D + timedelta(2)) == [D, D + timedelta(1), D + timedelta(2)]


# --- cal_effective_requested_days ----------------------------------------------
# Decisions: E1 employee given? | E2 (exclude_company AND exclude_holiday) |
#            E3 exclude_holiday | E4 exclude_company
HOL = D + timedelta(1)
CO = D + timedelta(2)


def _lt(exclude_company, exclude_holiday):
    return mock.Mock(exclude_company_leave=exclude_company, exclude_holiday=exclude_holiday)


@pytest.fixture
def no_db_calendar():
    """Holidays on HOL, company leave on CO; isolates the arithmetic from the DB."""
    with mock.patch("leave.models.Holidays") as hol, mock.patch("leave.models.CompanyLeaves") as co, mock.patch(
        "leave.models.holiday_dates_list", return_value=[HOL]
    ), mock.patch("leave.models.company_leave_dates_list", return_value=[CO]):
        yield hol, co


@pytest.mark.parametrize(
    "exclude_company,exclude_holiday,expected,path",
    [
        ("yes", "yes", 3, "E2=T: union removes both"),
        ("no", "yes", 4, "E2=F E3=T E4=F: holiday only"),
        ("yes", "no", 4, "E2=F E3=F E4=T: company leave only"),
        ("no", "no", 5, "E2=F E3=F E4=F: nothing excluded"),
    ],
)
def test_cal_effective_requested_days_exclusions(no_db_calendar, exclude_company, exclude_holiday, expected, path):
    end = D + timedelta(4)
    assert cal_effective_requested_days(D, end, _lt(exclude_company, exclude_holiday), 5) == expected


def test_cal_effective_requested_days_overlapping_holiday_and_company_leave_counted_once(no_db_calendar):
    # Same date in both sets: union (E2=T) must subtract it once, not twice.
    with mock.patch("leave.models.company_leave_dates_list", return_value=[HOL]):
        assert cal_effective_requested_days(D, D + timedelta(4), _lt("yes", "yes"), 5) == 4


def test_cal_effective_requested_days_employee_filters_specific_holidays(no_db_calendar):
    hol, _ = no_db_calendar
    emp = object()
    cal_effective_requested_days(D, D, _lt("no", "no"), 1, employee=emp)  # E1=T
    hol.objects.filter.assert_called_once()
    cal_effective_requested_days(D, D, _lt("no", "no"), 1)  # E1=F
    hol.objects.all.assert_called()


# --- AvailableLeave.forcasted_leaves -------------------------------------------
# F1 date is str? | F2 next_reset is truthy | F3 next_reset <= date
def _available(next_reset, total=10):
    from leave.models import AvailableLeave

    al = AvailableLeave()
    lt = mock.Mock(total_days=total)
    lt.leave_type_next_reset_date.return_value = next_reset
    al._state.fields_cache["leave_type_id"] = lt
    return al


def test_forcasted_leaves_string_date_is_parsed():  # F1=T
    assert _available(D).forcasted_leaves(D.isoformat()) == 10


def test_forcasted_leaves_no_reset_scheduled():  # F2=F
    assert _available(None).forcasted_leaves(D) == 0


def test_forcasted_leaves_reset_exactly_on_date_counts():  # F3 boundary: equal
    assert _available(D).forcasted_leaves(D) == 10


def test_forcasted_leaves_reset_after_date_does_not_count():  # F3=F boundary: +1 day
    assert _available(D + timedelta(1)).forcasted_leaves(D) == 0


def test_forcasted_leaves_reset_before_date_counts():  # F3=T boundary: -1 day
    assert _available(D - timedelta(1)).forcasted_leaves(D) == 10
