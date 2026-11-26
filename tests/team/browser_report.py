"""Render genuine Playwright/pytest JUnit results without inferring missing passes."""

import argparse
import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED = [f"UC-RAY-{number:02d}-{flow}" for number in (1, 2) for flow in ("MAIN", "A1", "A2", "E1", "E2")]


def render(junit, output):
    root = ET.parse(junit).getroot()
    results = {}
    for case in root.iter("testcase"):
        prop = case.find("properties/property[@name='case_id']")
        match = re.search(r"\[(UC-RAY-\d\d-(?:MAIN|A1|A2|E1|E2))\]", case.get("name", ""))
        key = prop.get("value") if prop is not None else match.group(1) if match else case.get("name")
        if key in results:
            raise ValueError("Duplicate browser case identity: " + key)
        failure = next((case.find(tag) for tag in ("error", "failure", "skipped") if case.find(tag) is not None), None)
        results[key] = {"status": failure.tag if failure is not None else "passed",
                        "detail": (failure.text or failure.get("message", "")) if failure is not None else "Visible result and persisted postconditions passed",
                        "seconds": case.get("time", "unavailable")}
    rows = []
    for key in EXPECTED:
        result = results.get(key, {"status": "not executed", "detail": "No JUnit result; this is not a pass", "seconds": "-"})
        rows.append("<tr><td>" + html.escape(key) + "</td><td>" + html.escape(result["status"]) + "</td><td>" + html.escape(result["seconds"]) + "</td><td><pre>" + html.escape(result["detail"]) + "</pre></td></tr>")
    passed = sum(results.get(key, {}).get("status") == "passed" for key in EXPECTED)
    complete = passed == 10 and set(results) == set(EXPECTED)
    document = "<!doctype html><html lang='en'><meta charset='utf-8'><title>Rayyan Playwright report</title><style>body{font:16px system-ui;margin:32px;max-width:1200px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:10px;text-align:left;vertical-align:top}pre{white-space:pre-wrap;max-width:720px;font-size:12px}</style><h1>Rayyan personal Playwright flows</h1><p>Syed Muhammad Rayyan Hassan · 24I-3000</p><p>Verified passes: " + str(passed) + "/10. Missing, failed, errored or skipped results do not satisfy completion.</p><table><tr><th>Flow</th><th>Actual status</th><th>Seconds</th><th>Evidence / assertion</th></tr>" + "".join(rows) + "</table><p>Raw JUnit, logs, screenshots and traces accompany this report. These are browser flows, separate from API and tooling counts.</p></html>"
    document = document.replace("<table>", "<p>Overall: " + ("PASS" if complete else "HOLD") + ". Unexpected case IDs: " + html.escape(", ".join(sorted(set(results) - set(EXPECTED))) or "none") + "</p><table>", 1)
    Path(output).write_text(document, encoding="utf-8")
    return complete


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--junit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if render(args.junit, args.output) else 1)
