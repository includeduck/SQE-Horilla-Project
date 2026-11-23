"""Scoped, non-autouse Area 2 fixtures. No production server or database access."""

import importlib.util
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
    assert settings.SETTINGS_MODULE == "area2_settings", "Use the explicit Area 2 config"
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
def runtime_cases(area2_seed, tmp_path):
    """Consume checked-in output, then generate/read a real fixture-bound artifact."""
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
