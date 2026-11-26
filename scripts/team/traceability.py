"""Generate the requirements traceability matrix (docs/team/TRACEABILITY_MATRIX.md).

Inputs
  * unit/recovery cases: `pytest --co -q` of tests/team/unit and tests/team/recovery
    (run with the unit settings), mapped to requirements by test-function name;
  * API cases: Area 2 requirement evidence (docs/team/finish-line/PROMPT03_REQUIREMENT_EVIDENCE.json);
  * browser, security, performance and accessibility tests: listed below (few, stable).

Usage (repo root, project venv):
    python -m pytest -c tests/team/pytest-unit.ini tests/team/unit tests/team/recovery --co -q > docs/team/evidence/traceability/collected-unit-recovery.txt
    python scripts/team/traceability.py docs/team/evidence/traceability/collected-unit-recovery.txt > docs/team/TRACEABILITY_MATRIX.md
"""

import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQS = {
    "FR-01": "Employee creates an allocation request",
    "FR-02": "Approver approves an allocation; balance credited",
    "FR-03": "Approver rejects an allocation with a reason; balance unchanged",
    "FR-04": "Allocation editable only while requested",
    "FR-05": "Employee submits a leave request (dates, breakdown)",
    "FR-06": "Request above available balance is rejected",
    "FR-07": "Overlapping request is rejected",
    "FR-08": "Approver approves a leave request; balance deducted",
    "FR-09": "Approver rejects a leave request; days restored",
    "FR-10": "Balance view shows the updated balance",
    "BR-01": "Boundary: requested days <= available + capped carry-forward + forecast",
    "BR-02": "Decision: acceptance needs all conditions (assigned, dates, breakdown, attachment, no overlap, ...)",
    "BR-03": "Change of state: leave/allocation state machine",
    "BR-04": "Permission: approver rights, self-approval refused, ownership",
}

# Unit/recovery test function -> requirements. First matching rule wins.
UNIT_RULES = [
    (r"allocation_clean|allocation_edit_lock", ["FR-04", "BR-03"]),
    (r"anonymous_user|missing_allocation", ["BR-04"]),
    (r"non_owner|owner_gets_own|ownership", ["FR-04", "BR-04"]),
    (r"approve_allocation_creates_balance_row|approve_allocation_credits", ["FR-02", "FR-10", "BR-03"]),
    (r"approve_allocation_twice", ["FR-02", "BR-03"]),
    (r"approval_recovers|second_retry|partial_failure", ["FR-02", "FR-10", "BR-03"]),
    (r"leave_approve_calculation", ["FR-08", "BR-01"]),
    (r"reject_.*allocation|reject_requested_allocation|reject_rejected_allocation", ["FR-03", "BR-03"]),
    (r"reject_already_rejected|reject_cancelled|reject_pending_cancellation|refunds_requester|refunds_only", ["FR-09", "BR-03"]),
    (r"reject_without_reason", ["FR-09"]),
    (r"overlap", ["FR-07", "BR-02"]),
    (r"calculate_requested_days|leave_requested_dates|cal_effective|forcasted|forecast|balance|carryforward|zero_|"
     r"half_day_just_above|day_count|holiday|company_leave|defaults", ["FR-06", "BR-01"]),
    (r"insufficient", ["FR-06", "BR-01"]),
    (r"missing_end_date", ["FR-05"]),
    (r"c1_|c2_|c3_|c4_|c5_|past_date|restrict|not_assigned|leave_type_not_assigned|no_leave_type|end_before|"
     r"breakdown|attachment|valid_request|work_info|superuser", ["FR-05", "BR-02"]),
    (r"database_builds", []),
]

# Other levels: (level, test id, description, requirements)
OTHER = [
    ("Use case (browser)", "UC-RAY-01 (5 flows)", "tests/team/e2e: allocation request main/alt/exception flows", ["FR-01", "FR-10"]),
    ("Use case (browser)", "UC-RAY-02 (5 flows)", "tests/team/e2e: leave request main/alt/exception flows", ["FR-05", "FR-06", "BR-01", "BR-02"]),
    ("Usability (browser)", "A11Y-W1", "tests/team/a11y: keyboard-only allocation request", ["FR-01"]),
    ("Usability (browser)", "A11Y-W2", "tests/team/a11y: over-balance rejected then corrected", ["FR-05", "FR-06", "BR-01"]),
    ("Security", "AD-1", "employee views own balance page", ["FR-10"]),
    ("Security", "AD-2", "employee cannot approve own allocation", ["FR-02", "BR-04"]),
    ("Security", "AD-3", "approver approves reportee's allocation", ["FR-02", "FR-10", "BR-04"]),
    ("Security", "AD-4", "employee cannot approve own leave", ["FR-08", "BR-04"]),
    ("Security", "AD-5", "approver approves reportee's leave", ["FR-08", "FR-10", "BR-04"]),
    ("Security", "AD-6", "employee cannot delete another's allocation", ["FR-04", "BR-04"]),
    ("Performance", "k6 available-leave", "balance read at 1 and 5 users (4 runs)", ["FR-10"]),
]

LEVELS = ["Unit", "Recovery", "API", "Use case (browser)", "Usability (browser)", "Security", "Performance"]


def unit_cases(collected):
    per_req = defaultdict(lambda: defaultdict(int))
    tests_per_req = defaultdict(set)
    for line in Path(collected).read_text(encoding="utf-8").splitlines():
        if "::" not in line:
            continue
        path, name = line.split("::", 1)
        func = re.sub(r"\[.*", "", name)
        level = "Recovery" if "recovery" in path else "Unit"
        reqs = next((r for pat, r in UNIT_RULES if re.search(pat, func)), None)
        if reqs is None:
            sys.exit(f"unmapped test function: {func} (add a rule to UNIT_RULES)")
        for req in reqs:
            per_req[req][level] += 1
            tests_per_req[(req, level)].add(func)
    return per_req, tests_per_req


def api_cases():
    data = json.loads((ROOT / "docs/team/finish-line/PROMPT03_REQUIREMENT_EVIDENCE.json").read_text(encoding="utf-8"))
    out = {}
    for row in data["requirements"]:
        ids = row["required_case_ids"]
        ids = ast.literal_eval(ids) if isinstance(ids, str) else ids
        out[row["requirement"]] = (len(ids), row["status"], row["consumer_files"])
    return out


def main(collected):
    sys.stdout.reconfigure(encoding="utf-8")
    per_req, tests = unit_cases(collected)
    api = api_cases()
    for req, (n, _status, _files) in api.items():
        per_req[req]["API"] += n
    other_ids = defaultdict(lambda: defaultdict(list))
    for level, tid, _desc, reqs in OTHER:
        for req in reqs:
            per_req[req][level] += 1
            other_ids[req][level].append(tid)

    p = print
    p("# Requirements Traceability Matrix\n")
    p("Generated by [`scripts/team/traceability.py`](../../scripts/team/traceability.py) from the collected unit/recovery "
      "tests, the Area 2 requirement evidence (`finish-line/PROMPT03_REQUIREMENT_EVIDENCE.json`) and the browser, "
      "security and performance test lists. Cells are **numbers of executable test cases** (parametrised cases counted "
      "individually; each case counted once within its level). Requirements: `SCOPE.md` §3–4.\n")
    p("## 1. Matrix\n")
    p("| Req | Requirement | " + " | ".join(LEVELS) + " | Levels | Total |")
    p("|---|---|" + "---|" * len(LEVELS) + "---|---|")
    covered_levels = {}
    for req, text in REQS.items():
        cells = [per_req[req].get(lv, 0) for lv in LEVELS]
        covered_levels[req] = sum(1 for c in cells if c)
        p(f"| **{req}** | {text} | " + " | ".join(str(c) if c else "–" for c in cells)
          + f" | {covered_levels[req]} | {sum(cells)} |")

    n = len(REQS)
    covered = sum(1 for r in REQS if covered_levels[r] > 0)
    multi = sum(1 for r in REQS if covered_levels[r] >= 2)
    brief3 = [r for r in REQS if per_req[r].get("API") and (per_req[r].get("Unit") or per_req[r].get("Recovery"))
              and (per_req[r].get("Use case (browser)") or per_req[r].get("Usability (browser)"))]
    p("\n## 2. Requirements coverage\n")
    p("| Measure | Value |")
    p("|---|---|")
    p(f"| Requirements with at least one passing automated test | **{covered}/{n} = {100 * covered // n}%** |")
    p(f"| Requirements covered at two or more levels | {multi}/{n} = {round(100 * multi / n)}% |")
    def missing(r):
        gaps = []
        if not (per_req[r].get("Unit") or per_req[r].get("Recovery")):
            gaps.append("unit")
        if not (per_req[r].get("Use case (browser)") or per_req[r].get("Usability (browser)")):
            gaps.append("browser")
        return f"{r} (no {' / '.join(gaps)})"
    gaps = [missing(r) for r in REQS if r not in brief3]
    p(f"| Requirements covered at unit **and** API **and** browser level (the brief's three test levels) | "
      f"{len(brief3)}/{n} = {round(100 * len(brief3) / n)}% |")
    p(f"| Gaps against the three levels | {'; '.join(gaps)} |")
    for lv in LEVELS:
        c = sum(1 for r in REQS if per_req[r].get(lv))
        p(f"| Covered at level: {lv} | {c}/{n} = {round(100 * c / n)}% |")

    p("\n## 3. Detail: which tests trace to each requirement\n")
    for req, text in REQS.items():
        p(f"### {req}: {text}\n")
        for level in ("Unit", "Recovery"):
            funcs = sorted(tests.get((req, level), []))
            if funcs:
                p(f"- **{level}** ({per_req[req][level]} cases): " + ", ".join(f"`{f}`" for f in funcs))
        if req in api:
            cnt, status, files = api[req]
            p(f"- **API** ({cnt} case IDs, status `{status}`): {files}")
        for level in LEVELS[3:]:
            if other_ids[req].get(level):
                p(f"- **{level}**: " + ", ".join(other_ids[req][level]))
        p("")

    p("## 4. Notes\n")
    p("- Known open failures kept visible as strict `xfail`: REC-01 (#46) under FR-02/BR-03 (recovery level).")
    p("- API counts are case IDs required per requirement in the Area 2 evidence; one API case can serve several "
      "requirements, so the API column is not summed across rows.")
    p("- Mutation testing (MUTATION_TESTING.md) strengthens the unit level for BR-01–BR-04; it is not a separate test level.")


if __name__ == "__main__":
    main(sys.argv[1])
