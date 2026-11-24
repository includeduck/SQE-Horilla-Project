"""Server-side business logic in scope for Area 1 white-box testing.

The brief requires 100% statement and branch coverage of the server-side
business logic of the two selected workflows (W1 leave allocation, W2 leave
request). These are the functions that implement BR-01..BR-04; the rest of the
3,000-line leave/models.py (rendering helpers, reports, scheduling, etc.) is not
part of the workflows.

Usage (after a pytest run with --cov-branch --cov-report=json:coverage.json):
    python tests/team/unit/coverage_scope.py coverage.json
Exits 1 if any scoped function is below 100% statements or branches, unless the
gap is listed in JUSTIFIED_GAPS with a reason.
"""

import json
import sys
from pathlib import PurePath

# (file, qualified function name, business rule(s))
SCOPE = [
    ("leave/methods.py", "calculate_requested_days", "BR-01"),
    ("leave/models.py", "leave_requested_dates", "BR-01"),
    ("leave/models.py", "cal_effective_requested_days", "BR-01"),
    ("leave/models.py", "AvailableLeave.forcasted_leaves", "BR-01"),
    ("leave/models.py", "LeaveRequest.leaveoverlapping", "BR-02"),
    ("leave/models.py", "LeaveRequest.clean", "BR-01, BR-02 (critical module)"),
    ("leave/models.py", "LeaveAllocationRequest.clean", "BR-03"),
    ("horilla_api/api_views/leave/views.py", "LeaveRequestApproveAPIView.leave_approve_calculation", "BR-01, BR-03"),
    ("horilla_api/api_views/leave/views.py", "LeaveRequestRejectAPIView.leave_calculation", "BR-03"),
    ("horilla_api/api_views/leave/views.py", "LeaveRequestRejectAPIView.put", "BR-03"),
    ("horilla_api/api_views/leave/views.py", "LeaveAllocationApproveAPIView.approve_calculations", "BR-03"),
    ("horilla_api/api_views/leave/views.py", "LeaveAllocationApproveAPIView.put", "BR-03"),
    ("horilla_api/api_views/leave/views.py", "LeaveAllocationRequestRejectAPIView.reject_calculation", "BR-03"),
    ("horilla_api/api_views/leave/views.py", "LeaveAllocationRequestRejectAPIView.put", "BR-03"),
    ("horilla_api/api_views/leave/views.py", "EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request", "BR-04"),
]

# Gaps that cannot be covered, with the justification required by the brief.
# key: (file, function) -> {"lines": [...], "branches": [[from, to], ...], "reason": str}
JUSTIFIED_GAPS: dict = {
    ("leave/models.py", "LeaveRequest.clean"): {
        "lines": [2142],
        "branches": [[2087, 2097], [2141, 2142]],
        "reason": (
            "2141->2142 infeasible: the condition tests the string f'{month}-{year}' "
            "(e.g. '3-2031') against a list built as f'{year}-{MM}' (e.g. '2031-03'); "
            "a 4-digit year can never equal a 1-2 digit month, so line 2142 is dead "
            "code (and unique_dates is never used afterwards). "
            "2087->2097 infeasible: the False branch needs start_date or end_date to be "
            "None, but line 2069 compares them first and raises TypeError "
            "(see test_missing_end_date_crashes_before_validation)."
        ),
    },
}


def _norm(path):
    return PurePath(path).as_posix()


def main(report_path):
    data = json.load(open(report_path, encoding="utf-8"))
    files = {_norm(k): v for k, v in data["files"].items()}
    failed = False
    print(f"{'Function':75s} {'Stmts':>11s} {'Branches':>11s}  Rule")
    for file, func, rule in SCOPE:
        fn = files.get(file, {}).get("functions", {}).get(func)
        if fn is None:
            print(f"{file}::{func:60s} NOT EXECUTED / NOT FOUND")
            failed = True
            continue
        s = fn["summary"]
        gap = JUSTIFIED_GAPS.get((file, func), {})
        missing_lines = sorted(set(fn["missing_lines"]) - set(gap.get("lines", [])))
        missing_br = [b for b in fn["missing_branches"] if b not in gap.get("branches", [])]
        stmts = f"{s['covered_lines']}/{s['num_statements']}"
        brs = f"{s['covered_branches']}/{s['num_branches']}"
        flag = "" if not (missing_lines or missing_br) else f"  MISSING lines={missing_lines} branches={missing_br}"
        if gap:
            flag += "  (justified gap)"
        print(f"{func:75s} {stmts:>11s} {brs:>11s}  {rule}{flag}")
        failed |= bool(missing_lines or missing_br)
    print("\nRESULT:", "FAIL" if failed else "PASS: 100% statement and branch coverage of scoped business logic")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "coverage.json"))
