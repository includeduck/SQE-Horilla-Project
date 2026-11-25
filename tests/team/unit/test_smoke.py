import pytest

from leave.models import AvailableLeave, LeaveType


@pytest.mark.django_db
def test_database_builds_and_leave_models_work():
    lt = LeaveType.objects.create(name="Smoke", total_days=10)
    assert LeaveType.objects.filter(pk=lt.pk).exists()
    assert AvailableLeave.objects.count() == 0
