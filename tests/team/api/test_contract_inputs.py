"""Remaining generated EP/BVA consumers; relational/reason oracles stay in Prompt 3."""
import json
from pathlib import Path

import pytest
from contract_support import run_generated

TEAM = Path(__file__).resolve().parents[1]
ARTIFACT = json.loads((TEAM / "generator/generated_cases.json").read_text(encoding="utf-8"))
LEGACY = set(json.loads((Path(__file__).with_name("legacy_generated_ids.json")).read_text(encoding="utf-8"))["ids"])


def deferred(case):
    return case["field"] == ["reason"] or case["expected"]["oracle"] == "date-order"


CASE_IDS = [case["id"] for case in ARTIFACT["cases"]
            if case["id"] not in LEGACY and not deferred(case)]


@pytest.mark.parametrize("case_id", CASE_IDS, ids=CASE_IDS)
def test_remaining_generated_contract(leave_http, case_id):
    run_generated(leave_http, leave_http.case(case_id))
