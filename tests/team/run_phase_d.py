"""Run the controlled strict HTTP regeneration experiment with exact failure accounting."""

import argparse
import importlib.util
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from run_area2 import execute_stage, xml_totals

TEAM = Path(__file__).resolve().parent
REPO = TEAM.parents[1]
sys.path.insert(0, str(TEAM / "generator"))
from demonstrate_regeneration import build_experiment


def failed_ids(path):
    root = ET.parse(path).getroot()
    return sorted(case.find("properties/property[@name='case_id']").get("value")
                  for case in root.iter("testcase") if case.find("failure") is not None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    evidence = Path(args.evidence).resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    comparison = build_experiment(evidence / "experiment")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(map(str, (TEAM, TEAM / "api", TEAM / "generator", REPO)))
    env["AREA2_EXPERIMENT_DIR"] = str(evidence / "experiment")
    env["PYTHONUNBUFFERED"] = "1"
    stages = []
    for variant in ("baseline", "variant"):
        env["AREA2_EXPERIMENT_VARIANT"] = variant
        command = [sys.executable, "-m", "pytest", "-c", str(TEAM / "pytest-area2.ini"),
                   str(TEAM / "regeneration"), "-v", "-s", "-o", "junit_family=xunit1",
                   "--junitxml=" + str(evidence / (variant + ".xml"))]
        stages.append(execute_stage(variant, command, evidence, env=env))
    baseline = xml_totals(evidence / "baseline.xml")
    variant = xml_totals(evidence / "variant.xml")
    actual_failed = failed_ids(evidence / "variant.xml") if variant else []
    expected_failed = sorted(comparison["predicted_variant"]["failed_ids"])
    demonstrated = (stages[0]["exit_code"] == 0 and baseline == {"cases": 6, "failures": 0, "errors": 0, "skipped": 0}
                    and stages[1]["exit_code"] == 1 and variant == {"cases": 6, "failures": 2, "errors": 0, "skipped": 0}
                    and actual_failed == expected_failed)
    manifest = {"stages": stages, "baseline": baseline, "variant": variant,
                "actual_failed_ids": actual_failed, "expected_failed_ids": expected_failed,
                "experiment_demonstrated": demonstrated, "application_scope_complete": False,
                "interpretation": "Two predicted spec-only incompatibilities must fail strict pytest assertions. Every additional failure/setup error/skip/missing result makes this demonstration fail."}
    (evidence / "experiment-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest))
    return 0 if demonstrated else 1


if __name__ == "__main__":
    raise SystemExit(main())
