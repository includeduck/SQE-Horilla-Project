"""Shared fixtures for Area 1 white-box unit tests.

All people and companies are synthetic. Passwords are never used for login:
API views are exercised with DRF's ``force_authenticate``.
"""

from datetime import date

import pytest
from django.db.models.signals import post_migrate

from base import signals as base_signals

# Horilla's post_migrate hook syncs thousands of export permissions and default
# HR groups. Unit tests do not use those groups, and the hook makes building
# the test database take 10+ minutes, so it is disconnected for unit tests only.
# Django's own permission/content-type creation still runs.
post_migrate.disconnect(base_signals.create_default_hrms_groups)

# A fixed, far-future Monday so "past date" and weekday logic is deterministic.
D = date(2031, 3, 3)


def make_employee(first, email, *, superuser=False, company=None, department=None, job=None):
    from employee.models import Employee, EmployeeWorkInformation
    from horilla_auth.models import HorillaUser

    username = email.split("@")[0]
    if superuser:
        user = HorillaUser.objects.create_superuser(username, email, "unused-pass-1")
    else:
        user = HorillaUser.objects.create_user(username=username, email=email, password="unused-pass-1")
    emp = Employee(
        employee_user_id=user,
        employee_first_name=first,
        employee_last_name="Test",
        email=email,
        phone="0300" + str(abs(hash(email)) % 10_000_000).zfill(7),
    )
    emp.save()
    work, _ = EmployeeWorkInformation.objects.get_or_create(employee_id=emp)
    work.company_id = company
    work.department_id = department
    work.job_position_id = job
    work.save()
    return Employee.objects.get(pk=emp.pk)  # fresh: drop stale cached work info


@pytest.fixture
def company(db):
    from base.models import Company

    return Company.objects.create(company="Unit Test Co", hq=True, country="PK", state="ICT", city="Isb", zip="44000")


@pytest.fixture
def department(db, company):
    from base.models import Department

    return Department.objects.create(department="Engineering")


@pytest.fixture
def job(db, department):
    from base.models import JobPosition

    return JobPosition.objects.create(job_position="Developer", department_id=department)


@pytest.fixture
def employee(db, company, department, job):
    return make_employee("Emp", "emp@unit.test", company=company, department=department, job=job)


@pytest.fixture
def other_employee(db, company):
    return make_employee("Other", "other@unit.test", company=company)


@pytest.fixture
def admin_employee(db, company):
    return make_employee("Admin", "admin@unit.test", superuser=True, company=company)


@pytest.fixture
def leave_type(db, company):
    from leave.models import LeaveType

    return LeaveType.objects.create(
        name="Unit Annual",
        payment="paid",
        limit_leave=True,
        total_days=10,
        carryforward_type="no carryforward",
        require_approval="yes",
        require_attachment="no",
        exclude_company_leave="no",
        exclude_holiday="no",
        company_id=company,
    )


@pytest.fixture
def available_leave(db, employee, leave_type):
    from leave.models import AvailableLeave

    al, _ = AvailableLeave.objects.get_or_create(employee_id=employee, leave_type_id=leave_type)
    AvailableLeave.objects.filter(pk=al.pk).update(available_days=5, carryforward_days=0, total_leave_days=5)
    al.refresh_from_db()
    return al


@pytest.fixture
def acting_as():
    """Set the thread-local request user that LeaveRequest.clean reads."""
    from django.test import RequestFactory

    from horilla import horilla_middlewares

    def _set(employee):
        request = RequestFactory().get("/")
        request.user = employee.employee_user_id
        request.session = {}
        horilla_middlewares._thread_locals.request = request

    yield _set
    horilla_middlewares._thread_locals.request = None
