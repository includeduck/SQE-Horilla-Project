"""Each materialized wire class uses the existing real Requests/live-server stack."""
import pytest
from generator.wire_catalog import build
from wire_support import run_wire

CASES=build()["cases"]


@pytest.mark.parametrize("case",CASES,ids=lambda case:case["id"])
def test_runtime_wire_contract(leave_http,case):
    run_wire(leave_http,case)
