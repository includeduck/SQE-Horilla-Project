"""Fail-propagating Area 2 producer command for Wasay's CI integration.

Run from any directory: python tests/team/run_area2.py --evidence <directory>
No application subprocess is launched until generator/schema checks pass.
No missing dependency, skipped API case or incomplete scope becomes a pass.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

TEAM = Path(__file__).resolve().parent
REPO = TEAM.parents[1]


def stage_commands(evidence):
    py = sys.executable
    generator = TEAM / "generator"
    pytest_base = [py, "-m", "pytest", "-c", str(TEAM / "pytest-area2.ini"),
                   "-p", "area2_order", str(TEAM / "api"), "-v", "-s",
                   "-o", "junit_family=xunit1"]
    return [
        ("generator", [py, "-m", "unittest", "discover", "-s", str(generator), "-p", "test_*.py", "-v"]),
        ("freshness", [py, str(generator / "generate.py"), "--spec", str(generator / "openapi.json"),
                       "--bindings", str(generator / "bindings.json"), "--output", str(generator / "generated_cases.json"), "--check"]),
        ("schema", [py, "-c", "import json; from openapi_spec_validator import validate; validate(json.load(open('tests/team/generator/openapi.json', encoding='utf-8'))); print('OpenAPI validated')"]),
        ("django", [py, "manage.py", "check", "--settings=area2_settings"]),
        ("api-first", pytest_base + ["--junitxml=" + str(evidence / "api-first.xml")]),
        ("api-reversed", pytest_base + ["--area2-reverse", "--junitxml=" + str(evidence / "api-reversed.xml")]),
        ("complete-scope", [py, str(generator / "generate.py"), "--spec", str(generator / "openapi.json"),
                            "--bindings", str(generator / "bindings.json"), "--output", str(generator / "generated_cases.json"), "--check", "--require-complete"]),
    ]


def execute_stage(name, command, evidence, *, cwd=REPO, env=None):
    start = time.monotonic()
    # Each run has a new evidence directory; an old passing XML is never reused.
    result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    (evidence / (name + ".txt")).write_text(result.stdout, encoding="utf-8")
    print(result.stdout, end="")
    return {"name": name, "command": command, "exit_code": result.returncode,
            "status": "passed" if result.returncode == 0 else "failed",
            "elapsed_seconds": round(time.monotonic() - start, 3)}


def xml_totals(path):
    if not path.exists():
        return None
    root = ET.parse(path).getroot()
    cases = list(root.iter("testcase"))
    return {"cases": len(cases),
            "failures": sum(case.find("failure") is not None for case in cases),
            "errors": sum(case.find("error") is not None for case in cases),
            "skipped": sum(case.find("skipped") is not None for case in cases)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", required=True, help="New directory; refuses to overwrite an earlier run")
    args = parser.parse_args(argv)
    evidence = Path(args.evidence).resolve()
    # Test evidence should be retained separately per run, not overwritten.
    evidence.mkdir(parents=True, exist_ok=False)
    artifact = json.loads((TEAM / "generator/generated_cases.json").read_text(encoding="utf-8"))
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(TEAM), str(TEAM / "api"), str(REPO)])
    env["PYTHONIOENCODING"] = "utf-8"
    results = []
    failure = None
    exit_code = 0
    for name, command in stage_commands(evidence):
        if failure:
            results.append({"name": name, "command": command, "status": "blocked", "blocked_by": failure})
            continue
        stage = execute_stage(name, command, evidence, env=env)
        results.append(stage)
        if stage["exit_code"]:
            failure, exit_code = name, stage["exit_code"]
        # A skipped API case does not satisfy required coverage.
        if name.startswith("api-") and not failure:
            totals = xml_totals(evidence / (name + ".xml"))
            if not totals or totals["cases"] == 0 or totals["skipped"]:
                failure, exit_code = name + ":empty-or-skipped-results", 4
    manifest = {
        "owner": "Syed Muhammad Rayyan Hassan", "roll": "24I-3000",
        "python": sys.version, "repository": str(REPO),
        "spec_sha256": artifact["spec_sha256"], "data_sha256": artifact["data_sha256"],
        "coverage_complete": artifact["coverage_complete"], "stages": results,
        "api_first": xml_totals(evidence / "api-first.xml"),
        "api_reversed": xml_totals(evidence / "api-reversed.xml"),
        "exit_code": exit_code, "accepted": exit_code == 0 and artifact["coverage_complete"],
    }
    (evidence / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exit_code": exit_code, "blocked_by": failure, "accepted": manifest["accepted"]}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
