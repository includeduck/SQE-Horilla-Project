"""Scoped, non-autouse Area 2 fixtures. No production server or database access."""

import importlib.util
import os
import runpy
from pathlib import Path

import pytest
import requests
from django.conf import settings
from django.core.cache import cache
from django.db import connection

TEAM = Path(__file__).resolve().parents[1]
REPO = TEAM.parents[1]
spec = importlib.util.spec_from_file_location("area2_generate", TEAM / "generator/generate.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


@pytest.fixture
def area2_seed(transactional_db):
    """pytest-django flushes the disposable database between parametrized cases."""
    # SETTINGS_MODULE metadata may be None under the live-server overrides.
    # Verify the selected module, our positive sentinel and actual DB path.
    assert os.environ.get("DJANGO_SETTINGS_MODULE") == "area2_settings"
    assert getattr(settings, "AREA2_ISOLATED_TESTS", False) is True
    assert connection.settings_dict["ENGINE"] == "django.db.backends.sqlite3"
    assert Path(connection.settings_dict["NAME"]).resolve().parent == settings.AREA2_TEMP_ROOT.resolve()
    cache.clear()
    context = runpy.run_path(str(REPO / "scripts/team/seed_team.py"))
    for role in ("employee", "approver"):
        context[role].refresh_from_db()
        assert not context[role + "_user"].is_superuser
    assert context["employee"].employee_work_info.reporting_manager_id_id == context["approver"].pk
    from leave.models import LeaveAllocationRequest, LeaveRequest

    assert not LeaveAllocationRequest.objects.exists()
    assert not LeaveRequest.objects.exists()
    context["avail"].refresh_from_db()
    assert context["avail"].available_days == 0
    assert context["avail"].carryforward_days == 0
    # Runtime verification of the inherited FileField defaults used by the spec.
    from horilla_api.api_serializers.leave.serializers import LeaveAllocationRequestCreateSerializer

    field = LeaveAllocationRequestCreateSerializer().fields["attachment"]
    assert field.max_length == 100
    assert field.allow_empty_file is False
    return context


@pytest.fixture
def area2_http():
    with requests.Session() as session:
        # Loopback test traffic must not go through the user's external proxy.
        session.trust_env = False
        yield session


@pytest.fixture
def runtime_cases(area2_seed, tmp_path, record_property):
    """Consume checked-in output, then generate/read a real fixture-bound artifact."""
    source = os.environ.get("AREA2_SOURCE_SHA") or os.environ.get("GITHUB_SHA", "local-unpublished")
    record_property("source_sha", source)
    record_property("checkout_sha", os.environ.get("GITHUB_SHA", source))
    folder = TEAM / "generator"
    document = generator.load_json(folder / "openapi.json")
    bindings = generator.load_json(folder / "bindings.json")
    generator.verify_fresh(generator.load_json(folder / "generated_cases.json"), document, bindings)
    bindings.update(employee_id=area2_seed["employee"].pk, leave_type_id=area2_seed["leave_type"].pk)
    # Other operation IDs are unused by this slice; do not pretend they are bound.
    generated = generator.generate(document, bindings)
    artifact_path = tmp_path / "runtime_cases.json"
    import json

    artifact_path.write_text(json.dumps(generated), encoding="utf-8")
    artifact = generator.load_json(artifact_path)
    generator.verify_fresh(artifact, document, bindings)
    return artifact


@pytest.fixture
def c_context(area2_seed):
    """Distinct normal users/balances expose cross-user refund corruption."""
    from employee.models import EmployeeWorkInformation
    from leave.models import AvailableLeave
    from rest_framework.settings import api_settings

    assert "JSONParser" in {parser.__name__ for parser in api_settings.DEFAULT_PARSER_CLASSES}

    context = area2_seed
    user = context["upsert_user"]("team_outsider", "TeamOutside#2026", "team_outsider@sqe.test")
    outsider = context["upsert_employee"](user, "Team", "Outsider", "team_outsider@sqe.test", "03000000004")
    work, _ = EmployeeWorkInformation.objects.get_or_create(employee_id=outsider)
    work.company_id = context["company"]
    work.reporting_manager_id = None
    work.save()
    context.update(outsider_user=user, outsider=outsider)
    for role, amount in (("approver", 7), ("outsider", 9)):
        available, _ = AvailableLeave.objects.get_or_create(employee_id=context[role], leave_type_id=context["leave_type"])
        AvailableLeave.objects.filter(pk=available.pk).update(available_days=amount, carryforward_days=0, total_leave_days=amount)
        assert not context[role + "_user"].is_superuser
    return context


@pytest.fixture
def leave_http(live_server, c_context, area2_http, runtime_cases, record_property):
    from http_support import LeaveHTTP

    harness = LeaveHTTP(live_server.url, area2_http, c_context, runtime_cases, record_property)
    assert harness.balance() == (0.0, 0.0)
    assert harness.balance("approver") == (7.0, 0.0)
    assert harness.balance("outsider") == (9.0, 0.0)
    return harness
