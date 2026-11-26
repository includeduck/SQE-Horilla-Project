# Weekly Progress Report: Week 2 (23–29 November 2026)

Shared test-management document. Status as of **26 November 2026** (end of the main execution days); final figures are in the [test completion report](TEST_COMPLETION_REPORT.md).

## 1. Progress against the plan

| Planned (TEST_PLAN §6) | Planned dates | Actual | Status | Evidence |
|---|---|---|---|---|
| Area 2: OpenAPI spec, generator, API suite | 19–25 Nov | 23–25 Nov | **Done**: 3,433 API cases pass in two orders | `API_COVERAGE_MATRIX.md`, PR #2, #8 |
| Area 1: SonarQube baseline, cyclomatic complexity | 24–26 Nov | 25 Nov | **Done** | `reports/SONARQUBE_BASELINE.md`, PR #9 |
| Area 1: white-box unit tests, MCC/MC-DC | 24–26 Nov | 25 Nov | **Done**: 159 tests, 100% scoped coverage | `reports/WHITEBOX_UNIT_TESTING.md`, PR #10 |
| Area 1: mutation testing | 24–26 Nov | 26 Nov | **Done**: 97.9% (100% of non-equivalent) | `reports/MUTATION_TESTING.md`, PR #32 |
| Area 1: CI quality gate | 24–26 Nov | 26 Nov | **Done**: required, owner bypass off; blocked PR #34; fix PR #35 | PR #33, `reports/CI_QUALITY_GATE.md` |
| Area 3: use cases + automation | 26–28 Nov | 24–26 Nov | **Done**: 4 use cases, 20 browser flows | `RAYYAN_USE_CASES.md`, `WASAY_USE_CASES.md`, PR #49 |
| Area 3: usability and accessibility | 26–28 Nov | 26 Nov | **Done**: fixed screen 71 → 99 | `reports/ACCESSIBILITY_TESTING.md`, PR #47 |
| Area 3: security | 26–28 Nov | 26 Nov | **Done**: 6 access decisions, ZAP, pip-audit | `reports/SECURITY_ASSESSMENT.md`, PR #37 |
| Area 3: performance and recovery | 26–28 Nov | 26 Nov | **Done**: p95 39 ms; REC-01 found | `reports/PERFORMANCE_TESTING.md`, PR #45 |
| Test plan, risk register | 26–28 Nov | 26 Nov | **Done** | PR #36 (merged) |
| Traceability, defect analysis | 26–28 Nov | 26 Nov | **Done** | PR #48 |
| Completion report, PDF, zip | 28 Nov | started 26 Nov | In progress | this report, completion report |

**Activity:** 101 team commits (Rayyan 70, Wasay 31), 15 pull requests (8 merged, 6 waiting for CI, 1 demo closed by design), 33 defects logged.

## 2. GQM metrics

Same goal and questions as week 1.

| Question | Metric | Week 1 | Week 2 (26 Nov) | Trend / reading |
|---|---|---|---|---|
| Q1 How defective is the scoped code? | **Defect density** (defects / KLOC, scoped ≈ 15.6 KLOC) | 0.0 | **2.1 /KLOC** (33 defects); high severity **0.64 /KLOC** (10) | Most defects sit in input validation and leave-rule logic (Pareto, `DEFECT_ANALYSIS.md` §3). A density of ~2/KLOC in one module that already has upstream tests shows the extra techniques (state-based, generated inputs, fault injection) found what the upstream suite missed |
| Q2 How much of the test basis is verified? | **Requirements coverage** (FR + BR with ≥ 1 passing test / 14) | 0% | **14/14 = 100%**; 14/14 at ≥ 2 levels; 5/14 at unit + API + browser, **11/14 once PR #49 merges** | Coverage is complete at requirement level; after PR #49 the three-level gaps are FR-01 (no unit test: its logic sits in the API serializer, tested at API level) and FR-04, FR-07 (no browser flow; covered at unit, API and, for FR-04, security level) |
| Q3 Do fixes hold? | **Reopen rate** (reopened / closed) | n/a | **0/22 = 0%** | Every fix shipped with a regression test that runs in the required gate, so no fix has regressed |
| (supporting) | Defect closure | n/a | 22/33 closed (**67%**); 11 open (1 high) | The open high defect (#46) decides the release criteria |

Defect discovery by day: 23 Nov: 4, 24 Nov: 3, 25 Nov: 18 (generated API inputs), 26 Nov: 8 (security, white-box, recovery).

## 3. Risks and issues this week

| Item | Effect | Link |
|---|---|---|
| A team member's capacity reduced; Area 3 work reallocated by team agreement (26 Nov) | Area 3 done by the other two members; more load in the last days | PJ-02 |
| **CI congestion:** each gate run starts ~35 jobs (API suite sharded 16 × 2 orders) and Area 2's separate workflows repeat the same tests on every PR; the free runner limit (~20 concurrent jobs) queues PRs for hours | Merges wait; feedback slows | PJ-05 |
| Stale SQLite WAL files corrupted the restored database ("database disk image is malformed") | One accessibility run invalid; found and fixed | PJ-04 |
| REC-01 (#46): approval is not atomic, a retry double-credits | High-severity product defect open at the end of the week | PR-01 |
| `AI_USE_RECORD.md` edited by every PR | Merge conflicts on each merge (one line each) | process |
| mutmut needs `fork()`; Chromium in WSL needs system libraries (no sudo) | Mutation runs in WSL, browser tests on Windows / CI | PJ-04 |

## 4. Control actions

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| C2-1 | Re-plan Area 3 between Rayyan and Wasay; record the split in the test plan (roles) | Rayyan, Wasay | 26 Nov | Done (TEST_PLAN §3) |
| C2-2 | Merge the waiting PRs in dependency order (#48 → #49, then #37, #45, #47, #35); resolve the `AI_USE_RECORD.md` conflict as each lands | Wasay | 27 Nov | In progress |
| C2-3 | Reduce CI load: run Area 2's separate `phase-d` / `area2-verification` workflows only on push or manually, since the quality gate already runs the same API and browser tests on every PR | Rayyan, Wasay | 27 Nov | Proposed |
| C2-4 | `reset.ps1` removes `-wal`/`-shm` files and checkpoints before saving a snapshot | Wasay | 26 Nov | Done (PR #47) |
| C2-5 | Decide on #46 before the completion report: fix (`transaction.atomic` + `select_for_update`) or release on HOLD | Team | 28 Nov | Done: fixed in PR #51 (fails before, passes after) |
| C2-6 | Renumber the AI-use record once all PRs are merged | Wasay | 28 Nov | Open |
| C2-7 | Each member fills the **actual effort** column in `TEST_PLAN.md` §8 | All | 28 Nov | Open |
