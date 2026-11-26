"""Controlled two-constraint experiment; never edits canonical spec/data."""

import argparse
import copy
import json
from pathlib import Path

from generate import ContractError, fingerprint, generate, load_json, verify_fresh

ROOT = Path(__file__).resolve().parent
PREFIX = "self_allocation_create:body:"
SELECTED_IDS = [PREFIX + field + ":BVA:" + constraint + "-" + point
                for field, constraint in (("description", "minLength"), ("attachment", "x-filename-maxLength"))
                for point in ("below", "at", "above")]


def build_experiment(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    baseline = load_json(ROOT / "openapi.json")
    bindings = load_json(ROOT / "bindings.json")
    original = load_json(ROOT / "generated_cases.json")
    verify_fresh(original, baseline, bindings)
    variant = copy.deepcopy(baseline)
    properties = variant["components"]["schemas"]["SelfAllocationCreate"]["properties"]
    changes = [
        {"field": "description", "constraint": "minLength", "before": properties["description"]["minLength"], "after": 3,
         "rationale": "Tighten the existing nonblank minimum in a spec-only experiment; production remains minimum one."},
        {"field": "attachment", "constraint": "x-filename-maxLength", "before": properties["attachment"]["x-filename-maxLength"], "after": 80,
         "rationale": "Tighten the existing runtime-verified filename budget in a spec-only experiment; production remains 100."},
    ]
    for change in changes:
        properties[change["field"]][change["constraint"]] = change["after"]
    regenerated = generate(variant, bindings)
    try:
        verify_fresh(original, variant, bindings)
    except ContractError as error:
        stale = {"rejected": True, "reason": str(error)}
    else:
        raise AssertionError("Changed spec must reject old generated output")
    before = {case["id"]: case for case in original["cases"]}
    after = {case["id"]: case for case in regenerated["cases"]}
    assert before.keys() == after.keys(), "Two limit edits preserve stable case identities"
    affected = [key for key in before if before[key] != after[key]]
    assert {before[key]["operation"] for key in affected} == {"self_allocation_create"}
    assert generate(baseline, bindings) == original, "Canonical baseline must remain unchanged"
    report = {
        "changes": changes, "baseline_spec_sha256": fingerprint(baseline),
        "variant_spec_sha256": fingerprint(variant), "baseline_data_sha256": original["data_sha256"],
        "variant_data_sha256": regenerated["data_sha256"], "bindings_sha256": fingerprint(bindings),
        "stale_output": stale, "affected_case_ids": affected,
        "unchanged_case_ids": [key for key in before if before[key] == after[key]],
        "selected_http_ids": SELECTED_IDS,
        "predicted_baseline": {"passed": 6, "failed": 0},
        "predicted_variant": {"passed": 4, "failed": 2,
                              "failed_ids": [PREFIX + "description:BVA:minLength-below", PREFIX + "attachment:BVA:x-filename-maxLength-above"]},
        "selected_comparison": [{"id": key, "before": before[key], "after": after[key]} for key in SELECTED_IDS],
        "interpretation": "The unchanged server accepts description length two and filename length 81; the tightened experimental contract rejects both. This demonstrates spec/server disagreement, not a production rule change.",
        "canonical_baseline_preserved": True,
    }
    for name, value in (("baseline.openapi.json", baseline), ("baseline.cases.json", original),
                        ("variant.openapi.json", variant), ("variant.cases.json", regenerated),
                        ("comparison.json", report)):
        (output / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = build_experiment(args.output)
    print(json.dumps({key: result[key] for key in ("changes", "baseline_spec_sha256", "variant_spec_sha256", "stale_output", "canonical_baseline_preserved")}))
