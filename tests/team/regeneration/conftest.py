"""Reuse the exact Area 2 HTTP fixtures with explicitly selected experiment data."""

import importlib.util
import os
from pathlib import Path

import pytest

TEAM = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("area2_http_fixtures", TEAM / "api/conftest.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
area2_seed = shared.area2_seed
area2_http = shared.area2_http
c_context = shared.c_context
leave_http = shared.leave_http


@pytest.fixture
def runtime_cases(area2_seed, tmp_path):
    generator = shared.generator
    folder = Path(os.environ["AREA2_EXPERIMENT_DIR"])
    variant = os.environ.get("AREA2_EXPERIMENT_VARIANT", "baseline")
    assert variant in {"baseline", "variant"}
    document = generator.load_json(folder / (variant + ".openapi.json"))
    bindings = generator.load_json(TEAM / "generator/bindings.json")
    generator.verify_fresh(generator.load_json(folder / (variant + ".cases.json")), document, bindings)
    bindings.update(employee_id=area2_seed["employee"].pk, leave_type_id=area2_seed["leave_type"].pk)
    artifact = generator.generate(document, bindings)
    generator.verify_fresh(artifact, document, bindings)
    return artifact
