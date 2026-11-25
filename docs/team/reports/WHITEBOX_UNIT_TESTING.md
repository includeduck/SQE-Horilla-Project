# White-box Unit Testing (Area 1)

Owner: Muhammad Wasay Tariq (24I-3071). Brief §2, Unit level: "100% statement and branch coverage of all server-side business logic; justify any uncovered code. Critical module: complete MCC, then MC/DC pairs from the MCC tables. Cover all four business rules."

## 1. How to run

```powershell
.\.venv\Scripts\python -m pip install -r tests\team\requirements-unit.txt
.\.venv\Scripts\python -m pytest -c tests\team\pytest-unit.ini tests\team\unit --cov=leave --cov=horilla_api.api_views.leave --cov-branch --cov-report=json:coverage.json --cov-report=xml:coverage.xml
.\.venv\Scripts\python tests\team\unit\coverage_scope.py coverage.json
.\.venv\Scripts\python tests\team\unit\mcc_tables.py > docs\team\reports\MCC_MCDC_TABLES.md
```

- Settings: [`tests/team/unit_settings.py`](../../../tests/team/unit_settings.py) uses an in-memory SQLite DB built from the models (`--nomigrations`), so it never touches the local `TestDB.sqlite3` or the Area 2 databases. A full run takes about 1 minute.
- Horilla's `post_migrate` hook that syncs default HR groups and export permissions is disconnected for unit tests only ([`conftest.py`](../../../tests/team/unit/conftest.py)): it made test-DB creation take 10+ minutes and the groups are not used by the units under test. Django's own permission creation still runs.
- All data is synthetic; API views are called with DRF's `APIRequestFactory` + `force_authenticate` (no passwords are used).

## 2. Scope: server-side business logic of W1 and W2

The 100% target applies to the functions that implement the four business rules of the two workflows, listed in [`coverage_scope.py`](../../../tests/team/unit/coverage_scope.py). The rest of `leave/models.py` (≈3,000 lines: templates, reports, scheduling, dashboards) is not part of W1/W2.

| Unit | File | Rule(s) | Statements | Branches |
|---|---|---|---|---|
| `calculate_requested_days` | `leave/methods.py` | BR-01 | 6/6 | 2/2 |
| `leave_requested_dates` | `leave/models.py` | BR-01 | 3/3 | 2/2 |
| `cal_effective_requested_days` | `leave/models.py` | BR-01 | 17/17 | 8/8 |
| `AvailableLeave.forcasted_leaves` | `leave/models.py` | BR-01 | 6/6 | 4/4 |
| `LeaveRequest.leaveoverlapping` | `leave/models.py` | BR-02 | 6/6 | 4/4 |
| **`LeaveRequest.clean`** (critical module) | `leave/models.py` | BR-01, BR-02 | 71/72* | 44/46* |
| `LeaveAllocationRequest.clean` | `leave/models.py` | BR-03 | 2/2 | 2/2 |
| `LeaveRequestApproveAPIView.leave_approve_calculation` | `horilla_api/api_views/leave/views.py` | BR-01, BR-03 | 10/10 | 2/2 |
| `LeaveRequestRejectAPIView.leave_calculation` | 〃 | BR-03 | 9/9 | 0/0 |
| `LeaveRequestRejectAPIView.put` | 〃 | BR-03 | 13/13 | 6/6 |
| `LeaveAllocationApproveAPIView.approve_calculations` | 〃 | BR-03 | 3/3 | 0/0 |
| `LeaveAllocationApproveAPIView.put` | 〃 | BR-03 | 7/7 | 2/2 |
| `LeaveAllocationRequestRejectAPIView.reject_calculation` | 〃 | BR-03 | 6/6 | 2/2 |
| `LeaveAllocationRequestRejectAPIView.put` | 〃 | BR-03 | 10/10 | 4/4 |
| `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` | 〃 | BR-04 | 10/10 | 4/4 |

\* The remaining line and 2 branches are infeasible and justified in §3. `coverage_scope.py` fails the run if anything else is uncovered. Evidence: [`evidence/unit-coverage-scope.txt`](../evidence/unit-coverage-scope.txt).

**Result: 100% statement and branch coverage of every feasible statement and branch in scope.** 126 tests pass; 1 test is an expected failure (`xfail(strict=True)`) for the known defect OD-01.

### Business-rule coverage

| Rule | Covered by |
|---|---|
| BR-01 boundary (requested days ≤ balance) | `test_day_counting.py`; `test_balance_boundary_bva` (4/5/6 days vs balance 5), `test_half_day_just_above_balance_rejected` (5.5), `test_carryforward_types` (cap at/above max), `test_zero_effective_days_rejected`, `test_leave_approve_calculation_split` (below/at/above available) |
| BR-02 decision (≥2 Boolean conditions) | `LeaveRequest.clean` checks: not-assigned, date order, C1 breakdown, C2 attachment, overlap + half-day exception H, C3 past date, C5 restriction |
| BR-03 change of state | Leave reject (incl. already-rejected and pending-cancellation refusals, OD-01 xfail), allocation approve (twice / after reject refused, no double credit), allocation reject (balance floor at 0), `LeaveAllocationRequest.clean` edit lock |
| BR-04 ownership / permission | `get_allocation_request`: owner, non-owner → `PermissionDenied` (regression for A2-D02), anonymous → 404, missing → validation error |

## 3. Uncovered code and justification

| Location | Not covered | Why it cannot be covered |
|---|---|---|
| `leave/models.py:2141 → 2142` | `unique_dates.remove(...)` | **Infeasible: dead code.** The condition looks for `f"{today.month}-{today.year}"` (e.g. `"3-2031"`) in a list built as `f"{year}-{MM}"` (e.g. `"2031-03"`). A string starting with a 1–2 digit month can never equal one starting with a 4-digit year, so the branch is never true. `unique_dates` is also never used afterwards. Harmless, but a maintainability finding. |
| `leave/models.py:2087 → 2097` | False branch of `if self.start_date and self.end_date` | **Infeasible:** it needs a missing `start_date` or `end_date`, but line 2069 (`start_date > end_date`) runs first and raises `TypeError` when `end_date` is `None` (`test_missing_end_date_crashes_before_validation`). `start_date` is non-nullable. |

## 4. White-box findings

1. **Missing end date crashes validation.** `LeaveRequest.end_date` is nullable, but `clean()` compares it before checking for `None`, so a request without an end date raises `TypeError` (HTTP 500 through a form/API path) instead of a validation message. Severity: medium. To log as a GitHub Issue.
2. **Dead code in `clean()`** (line 2141, see §3). Severity: low.
3. **Unknown carry-forward type is not capped.** If `carryforward_type` holds a value outside the three choices (possible via direct DB edits or a future choice), the `elif` chain at 2151/2153 falls through and the stored carry-forward is added **uncapped** (`test_carryforward_types`, "2153 F" row). Severity: low (robustness).
4. **Reject accepts a cancelled leave** (OD-01, BR-03 terminal state). Kept visible as `xfail(strict=True)`; when fixed, the test will XPASS and fail the run until the marker is removed.

## 5. MCC and MC/DC (critical module)

The full tables are generated by [`tests/team/unit/mcc_tables.py`](../../../tests/team/unit/mcc_tables.py) into [`MCC_MCDC_TABLES.md`](MCC_MCDC_TABLES.md). The generator applies each decision's real feasibility constraints and Python's short-circuit evaluation; the tests for C5 and H are parametrised from the same tables, so **every feasible MCC row is executed** and its expected outcome is checked against the real code.

| Decision | Conditions | MCC rows | Feasible | Executed | MC/DC pairs | Min MC/DC set |
|---|---|---|---|---|---|---|
| C1 `start==end and sb!=eb` (2072) | 2 | 4 | 4 | 4 | A 1/3, B 1/2 (unique-cause) | 3 |
| C2 `leave_type and require=='yes' and not attachment` (2081) | 3 | 8 | 4 | 4 | R 1/3, N 1/2; L: none (L=F infeasible, line 2049) | 3 |
| C3 `restrict and start<today` (2106) | 2 | 4 | 4 | 4 | R 1/3, P 1/2 | 3 |
| C5 `(Dp and InDept and NoJobs) or (Jb and InJobs)` (2198) | 5 | 32 | 15 | 15 | InDept, NoJobs, InJobs unique-cause; Dp, Jb masking | 6 |
| H half-day exception, 5-way `and` (1969) | 5 | 32 | 20 | 20 | all unique-cause | 6 |

Notes:
- **Infeasible MCC rows** come from coupled conditions, e.g. in C5 "restriction lists no job positions" and "restriction lists the employee's job" cannot both be true; in H, if both requests are full-day their breakdowns cannot differ.
- **Masking MC/DC** is used where unique-cause is impossible: for `Dp` the only rows that flip it also change `InDept` (a restriction cannot list a department the employee does not have), but `InDept` is not evaluated once `Dp` is false, so its value cannot mask `Dp`'s effect. This is the standard short-circuit form of MC/DC.
- **Why MC/DC adds to branch coverage:** coverage.py measures branches between lines only. Inline conditional expressions (`x if c else y`) and the individual operands of `and`/`or` are not counted, so 100% branch coverage alone does not show that each condition independently affects the outcome. The MCC/MC-DC tests do.
- C4 (2182–2186, which leave types a restriction applies to) is an `if/elif/elif` chain of separate decisions whose conditions share one underlying value (`exclued_types` empty vs non-empty); it is covered by branch tests (`test_c4_restriction_applicability`, 5 paths) rather than a single MCC table.

## 6. SonarQube coverage before and after

Rescanned on 2026-11-25 with `coverage.xml` from the unit run (`sonar.python.coverage.reportPaths`).

| Component | Before (baseline) | After unit tests | Comment |
|---|---|---|---|
| Whole project | 0.0% | 2.3% (line 2.2%, branch 6.7%) | Expected: only the leave workflows are in scope; 113,914 lines to cover. |
| `leave/models.py` | 0.0% | 42.2% (line 47.7%, branch 25.8%) | File is mostly out-of-scope helpers; every scoped function is 100% (§2). |
| `leave/methods.py` | 0.0% | 16.4% | Only `calculate_requested_days` is in scope (100%). |
| `horilla_api/api_views/leave/views.py` | 0.0% | 33.4% | Scoped approve/reject/allocation methods are 100%. |

SonarQube reports coverage per file, not per function, so the function-level gate (`coverage_scope.py`) is the evidence for the brief's 100% requirement, and the SonarQube figures show the change in the overall picture.

## 7. Test design techniques used

| Technique | Where |
|---|---|
| Basis-path testing (V(G)=6) | `calculate_requested_days`: 7 path tests ≥ V(G) |
| Boundary value analysis (3-point) | balance 4/5/6 vs 5; half-day 5.5; overlap adjacent day; past date yesterday/today; restricted window first day; forecast reset date −1/0/+1; allocation reject floor (above/equal/below) |
| Branch / decision coverage | every `if`/`elif` true and false outcome in scope |
| MCC + MC/DC | C1, C2, C3, C5, H (§5) |
| Test doubles | `cal_effective_requested_days` (holiday/company-leave lists mocked to isolate the arithmetic); `forcasted_leaves` (leave type mocked) |
