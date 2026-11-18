"""
Deterministic synthetic seed for the SQE team tests (Horilla leave module).

Run (repo root):  .venv\\Scripts\\python manage.py shell -c "exec(open('scripts/team/seed_team.py', encoding='utf-8').read())"
Idempotent: re-running updates the same records instead of duplicating them.

All people, emails and passwords below are SYNTHETIC TEST VALUES for a local
install only. Never reuse them anywhere else.

Accounts (username / password):
  team_admin     / TeamAdmin#2026     superuser (setup only; NOT used for rule tests, see SCOPE A1)
  team_approver  / TeamApprove#2026   Role "Leave Approver": leave approve/reject permissions,
                                       reporting manager of team_employee
  team_employee  / TeamEmploy#2026    Role "Employee": no leave-admin permissions
"""

from django.contrib.auth.models import Permission

from base.models import Company
from employee.models import Employee, EmployeeWorkInformation
from horilla_auth.models import HorillaUser
from leave.models import AvailableLeave, LeaveType

COMPANY_NAME = "SQE Test Co"
LEAVE_TYPE_NAME = "Team Annual Leave"

APPROVER_PERMS = [
    "view_leaverequest",
    "change_leaverequest",
    "view_leaveallocationrequest",
    "change_leaveallocationrequest",
    "view_availableleave",
    "add_availableleave",
    "view_leavetype",
]


def upsert_user(username, password, email, superuser=False):
    user = HorillaUser.objects.filter(username=username).first()
    if user is None:
        if superuser:
            user = HorillaUser.objects.create_superuser(username, email, password)
        else:
            user = HorillaUser.objects.create_user(username=username, email=email, password=password)
    user.email = email
    user.is_superuser = superuser
    user.is_staff = superuser
    user.is_active = True
    user.set_password(password)
    if hasattr(user, "is_new_employee"):
        user.is_new_employee = False
    user.save()
    return user


def upsert_employee(user, first, last, email, phone):
    emp = Employee.objects.filter(email=email).first()
    if emp is None:
        emp = Employee(
            employee_user_id=user,
            employee_first_name=first,
            employee_last_name=last,
            email=email,
            phone=phone,
        )
        emp.save()
    return emp


company, _ = Company.objects.get_or_create(
    company=COMPANY_NAME,
    defaults={"hq": True, "country": "Pakistan", "state": "Islamabad", "city": "Islamabad", "zip": "44000"},
)

admin_user = upsert_user("team_admin", "TeamAdmin#2026", "team_admin@sqe.test", superuser=True)
upsert_employee(admin_user, "Team", "Admin", "team_admin@sqe.test", "03000000001")

approver_user = upsert_user("team_approver", "TeamApprove#2026", "team_approver@sqe.test")
approver = upsert_employee(approver_user, "Team", "Approver", "team_approver@sqe.test", "03000000002")
approver_user.user_permissions.add(*Permission.objects.filter(codename__in=APPROVER_PERMS))

employee_user = upsert_user("team_employee", "TeamEmploy#2026", "team_employee@sqe.test")
employee = upsert_employee(employee_user, "Team", "Employee", "team_employee@sqe.test", "03000000003")

for emp, manager in ((approver, None), (employee, approver)):
    work, _ = EmployeeWorkInformation.objects.get_or_create(employee_id=emp)
    work.company_id = company
    work.reporting_manager_id = manager
    work.email = emp.email
    work.save()

leave_type, _ = LeaveType.objects.update_or_create(
    name=LEAVE_TYPE_NAME,
    defaults={
        "payment": "paid",
        "limit_leave": True,
        "total_days": 10,
        "carryforward_type": "no carryforward",
        "require_approval": "yes",
        "require_attachment": "no",
        "company_id": company,
    },
)

# Starting condition for W1: the type is assigned with a ZERO balance.
avail, _ = AvailableLeave.objects.get_or_create(employee_id=employee, leave_type_id=leave_type)
AvailableLeave.objects.filter(pk=avail.pk).update(available_days=0, carryforward_days=0, total_leave_days=0)

print(
    f"Team seed OK: company={company.pk} leave_type={leave_type.pk} "
    f"approver={approver.pk} employee={employee.pk} available_leave={avail.pk}"
)
