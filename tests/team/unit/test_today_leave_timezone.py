"""Regression test: the "today's leave" filter must use the local date (TIME_ZONE).

Defect: LeaveRequestFilter.filter_today_leave took "today" from now().date(),
which is the UTC date when USE_TZ = True. In the hours where the local date is
already ahead of UTC (18:30-24:00 UTC for Asia/Kolkata, 19:00-24:00 UTC for the
unit settings' Asia/Karachi), a leave on today's local date was not listed. The
Area 2 API cases WIRE:leave_list:query:today_leave:* failed in CI at 19:04 UTC
for this reason.
"""

from datetime import date, datetime, timezone as dt_timezone
from unittest import mock

import pytest
from django.utils import timezone

from leave.filters import LeaveRequestFilter
from leave.models import LeaveRequest

pytestmark = pytest.mark.django_db


def leave_on(employee, leave_type, day):
    return LeaveRequest.objects.bulk_create([LeaveRequest(
        employee_id=employee, leave_type_id=leave_type, start_date=day, end_date=day,
        requested_days=1, description="today filter", reject_reason="", status="approved",
    )])[0]


def today_leave_ids(at_utc):
    with mock.patch("leave.filters.now", return_value=at_utc):
        qs = LeaveRequestFilter({"today_leave": True}, queryset=LeaveRequest.objects.all()).qs
        return set(qs.values_list("pk", flat=True))


@pytest.mark.parametrize(
    "utc_time,local_today",
    [
        # Local date ahead of UTC: 20:00 UTC on 26 Nov is 01:00 on 27 Nov in Karachi.
        (datetime(2026, 11, 26, 20, 0, tzinfo=dt_timezone.utc), date(2026, 11, 27)),
        # Boundary: 18:59 UTC is 23:59 local, still 26 Nov.
        (datetime(2026, 11, 26, 18, 59, tzinfo=dt_timezone.utc), date(2026, 11, 26)),
        # Same date in both zones.
        (datetime(2026, 11, 27, 9, 52, tzinfo=dt_timezone.utc), date(2026, 11, 27)),
    ],
    ids=["local-ahead-of-utc", "last-local-minute", "same-date"],
)
def test_today_leave_uses_local_date(employee, leave_type, utc_time, local_today):
    assert timezone.localdate(utc_time) == local_today  # premise of the case
    today = leave_on(employee, leave_type, local_today)
    other_day = leave_on(employee, leave_type, date(2026, 11, 25) if local_today.day != 25 else date(2026, 11, 24))
    ids = today_leave_ids(utc_time)
    assert today.pk in ids, f"leave on the local date {local_today} must be listed at {utc_time:%H:%M} UTC"
    assert other_day.pk not in ids
