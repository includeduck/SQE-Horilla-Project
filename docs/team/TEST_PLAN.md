# Test Plan

SE3002 SQE project, section SE-5B. System under test: Horilla HRMS 2.4.0, leave module. Shared test-management document (brief §2). Version 1.1, 2026-11-26; kept up to date as the project runs (change log at the end).

## 1. Scope

**Test basis:** [`SCOPE.md`](SCOPE.md) (FR-01–FR-10, BR-01–BR-04, two roles, oracle decisions OD-01/OD-02) and [`AREA2_TEST_BASIS.md`](AREA2_TEST_BASIS.md).

| In scope | Out of scope (and why) |
|---|---|
| W1 leave allocation: request, approve, reject, edit lock | Other Horilla modules (payroll, recruitment, attendance, …): not part of the selected workflows |
| W2 leave request: create, overlap, balance check, approve, reject, cancel | Upstream Horilla tests: they earn no marks; team tests live in `tests/team/` |
| Shared record `AvailableLeave` (balance, carry-forward, forecast) | Leave reports, dashboards, scheduling jobs: no business rule of W1/W2 |
| REST API `/api/leave/…` and the browser UI for both workflows | Production infrastructure (Docker/PostgreSQL deployment): tests run on SQLite locally and in CI |
| Roles: Employee, Leave Approver / HR admin | Multi-level conditional approval chains: not used by the two workflows |
| Usability/accessibility, security, performance of the selected screens and operation | Load beyond 5 concurrent users |

## 2. Approach by risk level

Risks and scores: [`RISK_REGISTER.md`](RISK_REGISTER.md). The risk level sets the techniques and depth:

| Level | Risks | Test levels and techniques |
|---|---|---|
| High | PR-01 balance changes, PR-02 balance boundary, PR-03 cross-employee access, PR-04 state transitions, PR-05 malformed input | Unit white-box (100% stmt/branch, MCC → MC/DC), mutation (≥95%, custom business-rule operators), API EP + 3-point BVA with read-back, state-transition and decision-table tests, access matrix |
| Medium | PR-06 duplicates, PR-07 day counting, PR-08 overlap, PR-09 dependencies | EP/BVA, decision tables, repeated-request tests, dependency audit |
| Low | PR-10 performance, PR-11 accessibility | k6 load runs, Lighthouse + axe-core scans, one automated task test per workflow |

| Test level | Owner area | Location |
|---|---|---|
| Static analysis (SonarQube) | Area 1 | `docs/team/reports/SONARQUBE_BASELINE.md` |
| Unit / white-box, MCC, MC/DC | Area 1 | `tests/team/unit/` |
| Mutation | Area 1 | `tests/team/mutation/` |
| API and integration, OpenAPI + data generator | Area 2 | `tests/team/api/`, `tests/team/generator/` |
| Use cases + browser end to end | Area 2 / Area 3 | `tests/team/e2e/` |
| Usability and accessibility | Area 3 | `tests/team/e2e/`, reports |
| Security | Area 3 | `tests/team/security/` |
| Performance and recovery | Area 3 | `tests/team/perf/`, `tests/team/recovery/` |
| CI quality gate | Area 1 | `.github/workflows/quality-gate.yml` |

## 3. Roles

| Role | Person | Responsibility |
|---|---|---|
| Area 1 owner, CI owner | Muhammad Wasay Tariq (24I-3071) | Static analysis, white-box, mutation, CI gate |
| Area 2 owner | Syed Muhammad Rayyan Hassan (24I-3000) | API testing, OpenAPI spec, data generator |
| Area 3 owner | Zain bin Jabir (24I-3130), per `TEAM.md` | Use cases, usability, accessibility, security, performance |
| Area 3 execution (team agreement, 2026-11-26) | Rayyan Hassan and Wasay Tariq | Rayyan takes as much of Area 3 as he can; Wasay takes the rest |
| Test manager (shared) | All three | Plan, estimates, risk register, traceability, defects, progress and completion reports |
| Approver of merges | Repository owner (Wasay) | Merges only through the required `gate` check |

## 4. Environment

| Item | Value |
|---|---|
| Application | Horilla 2.4.0, branch `sqe-team`, baseline commit `6c15617b8` (`SETUP.md`) |
| Runtime | Python 3.12, Django 5.2.19, DRF 3.18.3 |
| Database | SQLite (local `TestDB.sqlite3` + snapshot reset; in-memory for unit tests; disposable files for API tests) |
| Local machines | Windows 11 (app, unit, Sonar server), WSL Ubuntu 26.04 (mutation) |
| CI | GitHub Actions `ubuntu-latest`, workflow `quality-gate.yml` |
| Tools | pytest, pytest-django, coverage.py, SonarQube 26.10 Community, mutmut 3.8.1, OpenAPI 3.0.3 + own generator, Playwright (Chromium), Lighthouse, axe-core, OWASP ZAP, pip-audit, k6 |

## 5. Test data

- **Synthetic only.** `scripts/team/seed_team.py` creates the company, `team_admin`, `team_approver`, `team_employee` and "Team Annual Leave" with a 0-day balance (W1 starting state).
- Unit tests build their own data per test (fixtures in `tests/team/unit/conftest.py`); a fixed future date (2031-03-03) keeps date logic deterministic.
- API inputs come from the OpenAPI-driven generator (`tests/team/generator/`), never typed by hand.
- Reset between runs: `scripts/team/reset.ps1` (snapshot restore) or the per-test databases.

## 6. Schedule

| Dates (2026) | Activity |
|---|---|
| 18 Nov | MIS selected and registered, local setup, scope draft, team repo |
| 19–25 Nov | Area 2: OpenAPI spec, generator, API suite, defects A2-* |
| 24–26 Nov | Area 1: SonarQube baseline, white-box unit tests, MCC/MC-DC, mutation, CI gate |
| 26–28 Nov | Area 3: use cases, accessibility, security, performance/recovery; test management documents |
| 28 Nov | Test completion report, release/hold decision, PDF and repository zip |
| 29 Nov | Submission |

Weekly progress reports: week 1 (16–22 Nov), week 2 (23–29 Nov).

## 7. Entry, exit, suspension and resumption criteria

| Type | Criteria |
|---|---|
| **Entry** | Baseline commit recorded and runs locally; seed and reset scripts work; `SCOPE.md` requirements and rules agreed; test tools installed |
| **Exit** | Exit criteria EC-1 to EC-5 in `RISK_REGISTER.md` §6 met, **or** every unmet criterion recorded with its residual risk in the completion report. Release criteria: EC-1, EC-2, EC-3 |
| **Suspension** | (1) The baseline does not start or the seed fails; (2) a blocker defect stops a whole workflow (e.g. login or balance read fails); (3) the CI gate itself is broken (fails on an unchanged `sqe-team`) |
| **Resumption** | The blocking cause is fixed and verified: app starts and seed passes; the blocker defect is fixed or a workaround is documented; the gate is green again on `sqe-team` |

## 8. Estimation (three-point)

Effort in person-hours. Expected **E = (O + 4M + P) / 6**, standard deviation **σ = (P − O) / 6**.

| Area | Optimistic O | Most likely M | Pessimistic P | Expected E | σ | Actual |
|---|---|---|---|---|---|---|
| Setup, scope, registration | 3 | 5 | 10 | 5.5 | 1.2 | not split by area |
| Static analysis + cyclomatic complexity | 2 | 4 | 8 | 4.3 | 1.0 | not split by area |
| White-box unit, MCC, MC/DC | 8 | 14 | 24 | 14.7 | 2.7 | not split by area |
| Mutation testing | 4 | 8 | 16 | 8.7 | 2.0 | not split by area |
| CI quality gate | 4 | 8 | 16 | 8.7 | 2.0 | not split by area |
| API testing + data generator | 10 | 18 | 30 | 18.7 | 3.3 | not split by area |
| Use cases + automation | 6 | 10 | 18 | 10.7 | 2.0 | not split by area |
| Usability and accessibility | 3 | 6 | 10 | 6.2 | 1.2 | not split by area |
| Security | 3 | 6 | 12 | 6.5 | 1.5 | not split by area |
| Performance and recovery | 3 | 6 | 10 | 6.2 | 1.2 | not split by area |
| Test management and report | 8 | 12 | 20 | 12.7 | 2.0 | not split by area |
| **Total** | **54** | **97** | **174** | **102.8** | **6.4** | **21–23** |

Total σ = √(Σσ²) = √41.6 ≈ 6.4 h, so the plan is 102.8 ± 12.9 h at about 95% confidence. **Actual effort** was reported by each member (not estimated by tools). Members tracked their hours per day, not per area, so the actual is given per member:

| Member | Before 26 Nov (18, 23–25 Nov) | 26 Nov | Actual total |
|---|---|---|---|
| Muhammad Wasay Tariq (24I-3071) | 6 h | 4–5 h | **10–11 h** |
| Syed Muhammad Rayyan Hassan (24I-3000) | 5 h | 6–7 h | **11–12 h** |
| **Team** | 11 h | 10–12 h | **21–23 h** |

The comparison with the estimate is in the completion report §7.

## 9. Deliverables

Test plan (this document), risk register, traceability matrix, test scripts and data in `tests/team/`, CI configuration, GitHub Issues with severity/priority/triage, root cause analyses and Pareto chart, weekly progress reports with GQM metrics, test completion report, AI-use record, final PDF and repository zip.

## 10. Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-18 | Scope and test basis in `SCOPE.md` |
| 1.1 | 2026-11-26 | Full plan written: approach by risk, roles incl. Area 3 reallocation, schedule, criteria, three-point estimates |
