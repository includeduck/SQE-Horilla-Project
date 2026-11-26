"""Controlled failure-and-recovery test for a state-changing operation.

Brief §5: "use a test double to simulate a dependency becoming unavailable before
a write completes. Verify the persisted state after the failure, restore the
dependency, retry, and assert the expected final state without duplicate records."

Operation: PUT /api/leave/allocation-approve/<id>/ (W1 approval). It performs two
writes: (1) credit the balance (AvailableLeave.save), (2) mark the request
approved (LeaveAllocationRequest.save). The dependency is the database: a test
double makes the chosen write raise OperationalError, the error a dropped or
locked database connection gives.

Run (Windows or Linux, in-memory DB, about 10 s):
    python -m pytest -c tests/team/pytest-unit.ini tests/team/recovery -v
"""

from unittest import mock

import pytest
from django.db import OperationalError
from rest_framework.test import APIClient

from leave.models import AvailableLeave, LeaveAllocationRequest
from unit.conftest import (  # noqa: F401  (pytest fixtures)
    admin_employee, available_leave, company, department, employee, job, leave_type,
)

pytestmark = pytest.mark.django_db
DAYS = 3


@pytest.fixture
def allocation(employee, leave_type, available_leave):
    return LeaveAllocationRequest.objects.create(
        employee_id=employee, leave_type_id=leave_type, requested_days=DAYS,
        description="recovery test", reject_reason="", status="requested",
    )


@pytest.fixture
def approver(admin_employee):
    client = APIClient(raise_request_exception=False)  # a failing write must come back as a 500, like in production
    client.force_authenticate(user=admin_employee.employee_user_id)
    return client


def approve(client, pk):
    return client.put(f"/api/leave/allocation-approve/{pk}/", {}, format="json")


def persisted(allocation, employee, leave_type):
    allocation.refresh_from_db()
    rows = AvailableLeave.objects.filter(employee_id=employee, leave_type_id=leave_type)
    return allocation.status, rows.count(), rows.first().available_days


def database_down_on(model):
    """Test double: the database becomes unavailable when `model` is written."""
    real_save = model.save

    def failing_save(self, *args, **kwargs):
        raise OperationalError("database is unavailable (simulated)")

    return mock.patch.object(model, "save", failing_save), real_save


@pytest.mark.parametrize(
    "failing_write,model",
    [
        ("1st write: balance credit", AvailableLeave),
        pytest.param(
            "2nd write: request status", LeaveAllocationRequest,
            marks=pytest.mark.xfail(strict=True, reason="REC-01 (#46): approval is not atomic; a failure after the "
                                    "balance credit leaves it committed and the retry credits again"),
        ),
    ],
)
def test_approval_recovers_without_duplicate_credit(approver, allocation, employee, leave_type, available_leave, failing_write, model):
    start_balance = available_leave.available_days  # 5

    # 1. Dependency becomes unavailable during the approval.
    patch, _ = database_down_on(model)
    with patch:
        failed = approve(approver, allocation.pk)
    assert failed.status_code == 500

    # 2. Persisted state after the failure: nothing may be half-applied.
    status, rows, balance = persisted(allocation, employee, leave_type)
    assert (status, rows) == ("requested", 1), "no duplicate balance row, request still pending"
    assert balance == start_balance, (
        f"after a failed approval the balance must be unchanged ({start_balance}), "
        f"but it is {balance}: the credit was committed without the status change"
    )

    # 3. Dependency restored; the client retries the same request.
    retried = approve(approver, allocation.pk)
    assert retried.status_code == 200

    # 4. Final state: approved once, credited exactly once, still one balance row.
    status, rows, balance = persisted(allocation, employee, leave_type)
    assert (status, rows, balance) == ("approved", 1, start_balance + DAYS)


def test_second_retry_after_success_is_refused(approver, allocation, employee, leave_type, available_leave):
    # Idempotency check: a duplicate retry after success must not credit again.
    assert approve(approver, allocation.pk).status_code == 200
    assert approve(approver, allocation.pk).status_code == 400
    assert persisted(allocation, employee, leave_type) == ("approved", 1, available_leave.available_days + DAYS)


def test_observed_partial_failure_then_retry_credits_twice(approver, allocation, employee, leave_type, available_leave):
    """Characterisation of the current (defective) behaviour, kept as evidence.

    When the database fails between the two writes, the balance credit is
    already committed (Horilla does not wrap the approval in a transaction and
    ATOMIC_REQUESTS is not enabled). The request is still 'requested', so the
    retry passes the status check and credits the balance a second time.
    """
    start = available_leave.available_days
    patch, _ = database_down_on(LeaveAllocationRequest)
    with patch:
        assert approve(approver, allocation.pk).status_code == 500
    assert persisted(allocation, employee, leave_type) == ("requested", 1, start + DAYS)
    assert approve(approver, allocation.pk).status_code == 200
    assert persisted(allocation, employee, leave_type) == ("approved", 1, start + 2 * DAYS)  # credited twice
