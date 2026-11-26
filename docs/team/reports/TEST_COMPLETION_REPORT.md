# Test Completion Report

SE3002 SQE project, section SE-5B. System: Horilla HRMS 2.4.0, leave module (W1 leave allocation, W2 leave request). Status as of **26 November 2026**; to be finalised on 28 November once the waiting pull requests are merged and the open-defect decision (§6) is taken.

## 1. Summary

All 14 requirements (FR-01–FR-10, BR-01–BR-04) are covered by passing automated tests, each at two or more test levels. Testing found **33 defects** (10 high); **22 are fixed and verified** by regression tests in the required CI gate and **11 are open**, one of them high severity (#46, REC-01: a failed approval plus a retry credits the balance twice).

**Recommendation: RELEASE once PR #51 is merged** (HOLD until then). Two of the three release criteria are met outright; EC-2 depended on the open high-severity defect #46 in the highest-scored risk (PR-01, wrong balance changes). The fix is in PR #51: it failed before (2 recovery tests red) and passes after (5/5), with the unit, coverage and mutation gates unchanged.

## 2. Release criteria: actual vs target

| Criterion | Target | Actual | Met? |
|---|---|---|---|
| **EC-1** Business-logic test strength (PR-01, PR-02) | 100% statement + branch coverage of the 15 scoped functions, mutation score ≥ 95%, 0 unexplained survivors | 100% statement + branch (2 infeasible branches justified); mutation **97.9%**, 465/475 killed, **0 unexplained** survivors (10 documented equivalents) | **Yes** |
| **EC-2** Cross-employee access and state safety (PR-03, PR-04, PR-01) | 100% of access-matrix and state-transition tests pass; **0 open high-severity** defects in PR-01/PR-03/PR-04 | Access matrix 6/6 pass; state-transition API cases all pass (two orders); use-case flows 20/20 pass; high-severity #46 **fixed in PR #51** (recovery tests 5/5 after, 2 failing before) | **Yes, once PR #51 is merged** (No on the current `sqe-team`) |
| **EC-3** Performance of the selected operation (PR-10) | p95 ≤ 500 ms and < 1% unexpected failures at 5 concurrent users | Worst run at 5 users: **p95 39.1 ms, 0.0%** failures (4 runs) | **Yes** |

Other exit criteria:

| Criterion | Target | Actual | Met? |
|---|---|---|---|
| EC-4 No server errors on invalid input (PR-05) | 0 HTTP 500 across generated invalid-input API cases | All generated invalid-input cases pass (3,433 API cases, both orders); the seven 500-on-malformed-input defects (#3, #21, #22, #23, #26, #27, #28) are fixed and verified | Yes (API level) |
| EC-5 Accessibility of the fixed screen (PR-11) | 0 critical/serious axe-core violations after the fix | My Leave Requests: 0 critical/serious (was 2/7); Lighthouse accessibility 71 → 99 | Yes |

## 3. What was tested and what was not

| Tested | Level / technique | Result |
|---|---|---|
| Day counting, balance boundary, overlap, restrictions, approve/reject arithmetic, allocation edit lock, ownership (15 functions) | Unit white-box: statement + branch, MCC/MC-DC, BVA, mutation (custom operators) | 159 unit tests pass; 100% scoped coverage; 97.9% mutation |
| All leave and allocation API operations of W1/W2 (34 operations) | API: EP + 3-point BVA from the OpenAPI generator, decision tables, state transitions, repeated requests, read-back | 3,433 cases pass in each of two orders |
| Employee and approver flows in the browser | 4 use cases, 20 Playwright flows (main, alternative, exception) | 20/20 pass (10 merged, 10 in PR #49) |
| Keyboard use, error-message usability, accessibility of key screens | Playwright task tests, axe-core, Lighthouse | Pass; one screen fixed |
| Role and ownership controls, passive scan, dependencies | Playwright access matrix, OWASP ZAP passive, pip-audit | 6/6 decisions as expected; 7 findings logged |
| Balance read under load; failure and recovery of approval | k6 (1 and 5 users), test double on the database | Limits met; REC-01 found |
| Static quality | SonarQube 26.10, ratchet quality gate in CI | No regression from the baseline |

**Not tested (and why):**

| Item | Reason | Residual effect |
|---|---|---|
| Other Horilla modules (payroll, attendance, recruitment, ...) | Out of scope (TEST_PLAN §1) | Unknown quality outside the leave module |
| Multi-level conditional approval chains (`LeaveRequestConditionApproval`) | Not used by the two workflows | `leave_multiple_approve` untested |
| Production configuration (PostgreSQL, gunicorn, `DEBUG=False`) | Local/CI use SQLite and the dev server | Transaction and locking behaviour may differ (relevant to #46) |
| Load above 5 concurrent users; other operations under load | Out of scope | Capacity limit unknown |
| Decorated API `put` methods under mutation | mutmut 3 does not mutate decorated functions | Covered 100% by unit tests, not mutation-tested |
| Active security testing (DAST active scan, penetration) | Brief requires defensive/passive testing only | Exploitability of findings not demonstrated |
| Mobile app and mobile layouts | Not part of the selected workflows | none for this scope |

## 4. Deviations from the plan

| Deviation | Reason | Effect |
|---|---|---|
| Testing started 23 Nov instead of 19 Nov | No work 19–22 Nov (week 1 report) | Compressed schedule; all levels still completed by 26 Nov |
| Area 3 work reallocated to Rayyan and Wasay | A member's reduced capacity (team agreement, 26 Nov) | Area 3 done by two people; recorded in TEST_PLAN §3 |
| Mutation in WSL, browser tests on Windows/CI | mutmut needs `fork()`; WSL Chromium lacks system libraries | Environment differences documented per report |
| Unit test database built without migrations | Horilla's default-group hook made setup take 10+ min | Unit tests run in ~1 min; hook disabled for unit tests only |
| Security tests run locally, not in CI | They need a live seeded server and ZAP | Re-run instructions in `SECURITY_ASSESSMENT.md` |
| Quality-gate runs take ~50 min and queue | API suite sharded 16 × 2 orders, free runner limit | Slower merges (week 2, C2-3) |

## 5. Open defects

| Defect | Severity | Risk | Decision |
|---|---|---|---|
| #46 REC-01 approval not atomic, retry double-credits | **High** | PR-01, PR-06 | **Fixed in PR #51** (all four API approve/reject endpoints and the web allocation approval made atomic); closes on merge |
| #38 SEC-01 allocation approval on GET (CSRF) | Medium | PR-03 | Fix in the next cycle; mitigated by SameSite=Lax cookies for cross-site sub-requests |
| #39 SEC-02 no Content-Security-Policy | Medium | PR-03 | Next cycle (report-only first) |
| #40 SEC-03 moment.js 2.29.1 | Medium | PR-09 | Next cycle (library upgrade) |
| #41 SEC-04 CDN scripts without SRI | Medium | PR-09 | Next cycle |
| #11 A1-D01 missing end date → TypeError | Medium | PR-05 | Fix ready (PR #35, fails-before/passes-after); merge when CI is green |
| #13 A1-D03 unknown carry-forward type uncapped | Low | PR-02 | Accept for release (needs invalid data) |
| #12 A1-D02 dead code | Low | maintainability | Deferred |
| #42 SEC-05 pdfkit advisory | Low | PR-09 | Deferred (outside the workflows; compensating XSS guard) |
| #43 SEC-06 svglib DoS advisory | Low | PR-09 | Next cycle (pin version) |
| #44 SEC-07 CSRF token in a query string | Low | PR-03 | Next cycle |

## 6. Residual risk per risk

| Risk | Initial score | Testing done | Open defects | Residual risk |
|---|---|---|---|---|
| PR-01 wrong balance changes | 25 | White-box, MC/DC, mutation, API read-back, use cases, recovery tests | #46 fixed in PR #51 | **Low** once PR #51 is merged (High until then) |
| PR-02 balance boundary | 20 | BVA at unit/API, forecast and cap tests, mutation | #13 (low) | Low |
| PR-03 cross-employee access | 20 | Access matrix, API ownership tests, use-case E2 flows | #38 (medium), #39, #44 | Medium (CSRF on the web approval link) |
| PR-04 invalid state transitions | 16 | State-transition tests (all allowed + disallowed), OD-01 fix | none | Low |
| PR-05 malformed input → 500 | 15 | Generated invalid inputs on every API input | #11 (fix in PR #35) | Low once #35 is merged |
| PR-06 duplicates | 12 | Repeated-request tests, OD-02 fix, recovery retry | none after PR #51 | Low |
| PR-07 day counting | 12 | Basis-path, holiday/company-leave tests, custom mutants | none | Low |
| PR-08 overlap | 12 | 20-row MCC of the half-day exception | none | Low |
| PR-09 dependencies | 9 | pip-audit, ZAP library check | #40, #41, #42, #43 | Medium (client-side libraries) |
| PR-10 performance | 6 | k6 1 and 5 users | none | Low |
| PR-11 accessibility | 6 | axe + Lighthouse, fix of one screen | moderate items on other screens | Low on the fixed screen; Medium elsewhere |
| PJ-01 schedule / PJ-02 capacity | 16 / 16 | Re-planning, CI automation | n/a | Realised but contained; all levels delivered |
| PJ-03 AI work not understood | 15 | AI-use record with viva TODOs per component | n/a | Depends on viva preparation |

## 7. Effort: estimate vs actual

Three-point estimate (TEST_PLAN §8): **102.8 ± 12.9 person-hours**. Actual hours are recorded by each member for their own areas (TEST_PLAN §8 "Actual" column, control action C2-7) and compared here when complete. Calendar indicator: the work was delivered in 6 working days (18, 23–26 Nov plus finalisation), against 10 planned days (18–28 Nov).

## 8. Recommendation

**RELEASE** the tested leave workflows **once PR #51 (fix for #46) is merged and the required gate is green on `sqe-team`**; until then, **HOLD**.

- Met: EC-1 (test strength), EC-3 (performance), EC-4, EC-5; EC-2 with PR #51.
- Merge PR #35 (#11, missing end date) in the same cycle.
- The open medium-severity security findings (#38–#41) do not block this release under the agreed criteria. #38 (state change on GET) should be first in the next cycle because it touches the same high-risk area (PR-03).
