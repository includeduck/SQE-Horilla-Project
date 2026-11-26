# Weekly Progress Report: Week 1 (16–22 November 2026)

Shared test-management document. Plan: [`TEST_PLAN.md`](../TEST_PLAN.md) §6. Risks: [`RISK_REGISTER.md`](../RISK_REGISTER.md).

## 1. Progress against the plan

| Planned this week (TEST_PLAN §6) | Status | Evidence |
|---|---|---|
| Select and register the MIS | **Done** 18 Nov: Horilla HRMS 2.4.0, leave module | `SCOPE.md` §1 |
| Local setup, baseline commit, seed and reset | **Done** 18 Nov | `SETUP.md`, `scripts/team/seed_team.py`, `scripts/team/reset.ps1`; baseline `6c15617b8` |
| Scope: two workflows, shared record, FR/BR, roles | **Done** (draft) 18 Nov | `SCOPE.md` §2–5 (FR-01–10, BR-01–04) |
| Team repository and roles | **Done** 18 Nov | public repo, `sqe-team` branch, `TEAM.md` |
| Start of Area 2 (API testing) | **Not started** (planned from 19 Nov) | no commits 19–22 Nov |

**Activity:** 1 working day (18 Nov), 4 team commits. No tests were executed this week.

## 2. GQM metrics

**Goal:** assess, each week, how far testing has progressed and how defective the scoped leave module is, so the team can decide on release.

| Question | Metric | Week 1 value |
|---|---|---|
| Q1 How defective is the scoped code? | **Defect density** = defects found / KLOC of scoped code (`leave/` + leave API views ≈ 15.6 KLOC) | 0 defects → **0.0 /KLOC** (no testing yet, so not meaningful) |
| Q2 How much of the test basis is verified? | **Requirements coverage** = requirements (FR + BR) with ≥ 1 passing automated test / 14 | **0/14 = 0%** |
| Q3 Do fixes hold? | **Reopen rate** = defects reopened / defects closed | n/a (no defects closed) |

**Reading:** the week delivered the foundation (system running, scope, basis) but no verification. Requirements coverage at 0% after one week is behind a schedule that assumed API testing from 19 Nov.

## 3. Risks and issues this week

| Item | Effect | Link |
|---|---|---|
| No test execution 19–22 Nov | Schedule slip of ~4 days against the plan | PJ-01 (schedule) |
| Fresh `migrate` takes 10+ minutes | Slow resets would slow every test cycle | PJ-04 (environment) |
| Scope still a draft | Tests could be built on rules the team later changes | test basis |

## 4. Control actions

| # | Action | Owner | Due | Outcome (recorded in week 2) |
|---|---|---|---|---|
| C1-1 | Start Area 2 immediately (OpenAPI spec, generator, API tests) to recover the slip | Rayyan | 23 Nov | Done: Area 2 started 23 Nov |
| C1-2 | Snapshot-based database reset (seconds instead of 10+ min) | Wasay | 18 Nov | Done: `reset.ps1` restores `tests/team/.baseline.sqlite3` |
| C1-3 | Each member reviews `SCOPE.md` before writing tests; disputed oracles recorded as decisions | All | 23 Nov | Done: OD-01/OD-02 recorded 23 Nov |
| C1-4 | Work through pull requests on a shared `sqe-team` branch | All | 23 Nov | Done; protected branch with required gate from 26 Nov |
