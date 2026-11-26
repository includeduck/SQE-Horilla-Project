"""Separate foundation population, reusing isolated non-autouse HTTP fixtures."""
import importlib.util
from pathlib import Path
TEAM = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("contract_shared_fixtures", TEAM / "api/conftest.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
for name in ("area2_seed", "area2_http", "runtime_cases", "c_context", "leave_http"):
    globals()[name] = getattr(shared, name)
