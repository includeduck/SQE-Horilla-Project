"""SonarQube part of the Area 1 CI quality gate.

Runs against a throwaway SonarQube server started as a GitHub Actions service
container (same version as the local baseline, 26.10 Community Build).

  python tests/team/ci/sonar_gate.py setup   # admin password, token, project, quality gate
  python tests/team/ci/sonar_gate.py check   # wait for analysis, enforce the gate

`setup` appends SONAR_TOKEN to $GITHUB_ENV (masked). `check` exits 1 when the
SonarQube quality gate status is not OK and writes a table to the job summary.
Thresholds come from docs/team/ci/gate-thresholds.json.
"""

import base64
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOST = os.environ.get("SONAR_HOST_URL", "http://localhost:9000").rstrip("/")
PROJECT = "sqe-horilla"
CONFIG = json.loads((ROOT / "docs/team/ci/gate-thresholds.json").read_text(encoding="utf-8"))["sonar"]


def call(method, path, auth, params=None):
    data = urllib.parse.urlencode(params or {}).encode()
    url = f"{HOST}{path}" + (f"?{data.decode()}" if method == "GET" and data else "")
    req = urllib.request.Request(url, data=None if method == "GET" else data, method=method)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode())
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read()
    return json.loads(body) if body else {}


def wait_up(timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{HOST}/api/system/status", timeout=10) as resp:
                if json.load(resp).get("status") == "UP":
                    return
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            pass
        time.sleep(5)
    sys.exit("SonarQube did not reach status UP")


def setup():
    wait_up()
    password = secrets.token_urlsafe(24) + "aA1!"
    call("POST", "/api/users/change_password", ("admin", "admin"),
         {"login": "admin", "previousPassword": "admin", "password": password})
    admin = ("admin", password)
    call("POST", "/api/projects/create", admin, {"project": PROJECT, "name": "SQE Horilla"})
    gate = CONFIG["gate_name"]
    call("POST", "/api/qualitygates/create", admin, {"name": gate})
    for c in CONFIG["conditions"]:
        call("POST", "/api/qualitygates/create_condition", admin,
             {"gateName": gate, "metric": c["metric"], "op": c["op"], "error": c["error"]})
    call("POST", "/api/qualitygates/select", admin, {"gateName": gate, "projectKey": PROJECT})
    token = call("POST", "/api/user_tokens/generate", admin,
                 {"name": "ci", "type": "PROJECT_ANALYSIS_TOKEN", "projectKey": PROJECT})["token"]
    print(f"::add-mask::{token}")
    with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as env:
        env.write(f"SONAR_TOKEN={token}\n")
    print(f"Quality gate '{gate}' created with {len(CONFIG['conditions'])} conditions and selected for {PROJECT}.")


def check():
    token = (os.environ["SONAR_TOKEN"], "")
    task = dict(line.split("=", 1) for line in (ROOT / ".scannerwork/report-task.txt").read_text().splitlines() if "=" in line)
    for _ in range(120):
        status = call("GET", "/api/ce/task", token, {"id": task["ceTaskId"]})["task"]["status"]
        if status in {"SUCCESS", "FAILED", "CANCELED"}:
            break
        time.sleep(5)
    if status != "SUCCESS":
        sys.exit(f"SonarQube background task ended with {status}")
    result = call("GET", "/api/qualitygates/project_status", token, {"projectKey": PROJECT})["projectStatus"]
    measures = {m["metric"]: m.get("value") for m in call(
        "GET", "/api/measures/component", token,
        {"component": PROJECT, "metricKeys": ",".join(c["metric"] for c in CONFIG["conditions"])})["component"]["measures"]}
    why = {c["metric"]: c["why"] for c in CONFIG["conditions"]}
    lines = [f"### SonarQube quality gate: {result['status']}", "",
             "| Metric | Actual | Fails if | Status | Why |", "|---|---|---|---|---|"]
    for c in result.get("conditions", []):
        op = ">" if c["comparator"] == "GT" else "<"
        lines.append(f"| {c['metricKey']} | {measures.get(c['metricKey'], c.get('actualValue'))} | {op} {c['errorThreshold']} | {c['status']} | {why.get(c['metricKey'], '')} |")
    report = "\n".join(lines)
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(report + "\n")
    Path("docs/team/evidence/ci").mkdir(parents=True, exist_ok=True)
    Path("docs/team/evidence/ci/sonar-gate.json").write_text(json.dumps({"projectStatus": result, "measures": measures}, indent=2))
    if result["status"] != "OK":
        sys.exit(1)


if __name__ == "__main__":
    {"setup": setup, "check": check}[sys.argv[1]]()
