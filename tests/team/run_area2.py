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
                   "-p", "area2_order", "-v", "-s",
                   "-o", "junit_family=xunit1"]
    return [
        ("generator", [py, "-m", "unittest", "discover", "-s", str(generator), "-p", "test_*.py", "-v"]),
        ("freshness", [py, str(generator / "generate.py"), "--spec", str(generator / "openapi.json"),
                       "--bindings", str(generator / "bindings.json"), "--output", str(generator / "generated_cases.json"), "--check"]),
        ("schema", [py, "-c", "import json; from openapi_spec_validator import validate; validate(json.load(open('tests/team/generator/openapi.json', encoding='utf-8'))); print('OpenAPI validated')"]),
        ("django", [py, "manage.py", "check", "--settings=area2_settings"]),
        ("api-preflight", pytest_base + [str(TEAM / "api/test_workflows.py") + "::test_w1_to_w2_shared_balance", "--maxfail=1", "--junitxml=" + str(evidence / "api-preflight.xml")]),
        ("api-first", pytest_base + [str(TEAM / "api"), "--junitxml=" + str(evidence / "api-first.xml")]),
        ("api-reversed", pytest_base + [str(TEAM / "api"), "--area2-reverse", "--junitxml=" + str(evidence / "api-reversed.xml")]),
        ("complete-scope", [py, str(generator / "generate.py"), "--spec", str(generator / "openapi.json"),
                            "--bindings", str(generator / "bindings.json"), "--output", str(generator / "generated_cases.json"), "--check", "--require-complete"]),
    ]


def execute_stage(name, command, evidence, *, cwd=REPO, env=None):
    start = time.monotonic()
    # Each run has a new evidence directory; an old passing XML is never reused.
    process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                               errors="replace", bufsize=1)
    # Preserve partial output if a remote job is interrupted, and make real
    # migration/case progress visible instead of buffering an entire API pass.
    with process.stdout as output, (evidence / (name + ".txt")).open("w", encoding="utf-8") as log:
        for line in output:
            log.write(line)
            log.flush()
            print(line, end="", flush=True)
    code = process.wait()
    return {"name": name, "command": command, "exit_code": code,
            "status": "passed" if code == 0 else "failed",
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


def run_stages(commands, evidence, env):
    """Keep dependency failures blocking, but collect both independent API runs.

    Each API invocation starts a new process and disposable settings/database.
    A failed first collection must stay failed while reverse-order evidence is
    still collected. Scope verification is independent of product assertions.
    """
    results, failure, exit_code = [], None, 0
    for name, command in commands:
        independent_after_api = (failure in {"api-first", "api-reversed"}
                                 and name in {"api-reversed", "complete-scope"})
        if failure and not independent_after_api:
            results.append({"name": name, "command": command, "status": "blocked", "blocked_by": failure})
            continue
        stage = execute_stage(name, command, evidence, env=env)
        if name.startswith("api-") and stage["exit_code"] == 0:
            try:
                totals = xml_totals(evidence / (name + ".xml"))
                valid = totals and totals["cases"] > 0 and not any(
                    totals[key] for key in ("failures", "errors", "skipped"))
            except (ET.ParseError, OSError) as error:
                valid = False
                stage["result_error"] = str(error)
            if not valid:
                stage.update(exit_code=4, status="failed",
                             validation_error="Missing, malformed, empty, failed, errored or skipped API results")
        results.append(stage)
        if stage["exit_code"] and failure is None:
            failure, exit_code = name, stage["exit_code"]
    return results, failure, exit_code


def manifest_totals(path):
    try:
        return xml_totals(path)
    except (ET.ParseError, OSError) as error:
        return {"invalid": True, "error": str(error)}


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
    env["PYTHONUNBUFFERED"] = "1"
    results, failure, exit_code = run_stages(stage_commands(evidence), evidence, env)
    manifest = {
        "owner": "Syed Muhammad Rayyan Hassan", "roll": "24I-3000",
        "python": sys.version, "repository": str(REPO),
        "spec_sha256": artifact["spec_sha256"], "data_sha256": artifact["data_sha256"],
        "coverage_complete": artifact["coverage_complete"], "stages": results,
        "api_preflight": manifest_totals(evidence / "api-preflight.xml"),
        "api_first": manifest_totals(evidence / "api-first.xml"),
        "api_reversed": manifest_totals(evidence / "api-reversed.xml"),
        "exit_code": exit_code, "accepted": exit_code == 0 and artifact["coverage_complete"],
    }
    (evidence / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exit_code": exit_code, "blocked_by": failure, "accepted": manifest["accepted"]}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
