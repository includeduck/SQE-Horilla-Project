# Risk Register

SE3002 SQE project, Horilla HRMS leave module (W1 leave allocation, W2 leave request). Shared test-management document (brief §2: "at least 8 product and 2 project risks, likelihood × impact (1–5) on a 5 × 5 matrix. Risk level decides technique and depth.").

Version 1.1, 2026-11-26. Scores were first set from the source review in `SCOPE.md` (18 Nov) and are re-scored here with the defects found since (issue numbers as evidence). Residual risk after testing is reported in the test completion report.

## 1. Scales

| Score | Likelihood (L) | Impact (I) |
|---|---|---|
| 1 | Rare: needs unusual data or a code change | Negligible: cosmetic |
| 2 | Unlikely: one narrow path | Minor: workaround exists, no data damage |
| 3 | Possible: realistic input or role | Moderate: wrong result a user notices and can correct |
| 4 | Likely: ordinary use, or already seen in similar code | Major: wrong balance/state, or a 500 error on a core action |
| 5 | Almost certain: already reproduced | Severe: lost/incorrect entitlement for another person, or access across employees |

**Risk level = L × I.** High: 15–25. Medium: 8–14. Low: 1–7.

## 2. Product risks

| ID | Risk (what could go wrong) | Rule / FR | L | I | Score | Level | Evidence (defects) | Technique and depth |
|---|---|---|---|---|---|---|---|---|
| PR-01 | Approve/reject/cancel changes the **wrong balance**, or credits/debits it twice | BR-01, BR-03, FR-02, FR-08, FR-09 | 5 | 5 | **25** | High | #4 refund went to the approver; #19 malformed reject deducted before the 400; #18 approval ignored carry cap | White-box 100% stmt/branch, MC/DC, mutation ≥95% incl. custom `balance_term_drop`; API read-back of balance after success and rejection; repeated-request tests |
| PR-02 | **Balance boundary** wrong: a request above available + capped carry-forward + forecast is accepted, or a valid one refused | BR-01, FR-06 | 5 | 4 | **20** | High | #6 / #18 carry cap ignored; #16 forecast refused at reset boundary; #14 zero/negative duration accepted | 3-point BVA (below/at/above) in unit and API tests, generator BVA on every numeric input, mutation (`or 0` defaults, forecast term) |
| PR-03 | An employee can **read, change or delete another employee's** allocation or leave request | BR-04 | 4 | 5 | **20** | High | #5 foreign-owned PUT/DELETE; #20 owner can transfer a request; #24 foreign employee on generic allocation create | Access matrix with Playwright (allowed and denied per role), API ownership tests, unit tests of `get_allocation_request`, ZAP passive scan |
| PR-04 | **Invalid state transition** accepted (e.g. reject a cancelled leave, approve twice) | BR-03, FR-04 | 4 | 4 | **16** | High | #30 reject accepted on cancelled leave (OD-01); allocation approve-twice tested | State-transition testing: every allowed transition and ≥1 disallowed per state (unit + API), mutation with custom `leave_state_swap` |
| PR-05 | **Malformed input** causes a server error (500) instead of a validation message | FR-01, FR-05 | 5 | 3 | **15** | High | #11 missing end date → TypeError; #21, #22, #23, #26, #28 malformed ids/bodies/filters → 500 | EP with one invalid value per test from the OpenAPI generator, API negative tests, unit test for #11 |
| PR-06 | **Duplicate records** from repeated or double-submitted requests | FR-01, FR-05, brief "no duplicates" | 4 | 3 | **12** | Medium | #29 identical pending allocation accepted twice (OD-02) | Repeated-request API tests, decision table for duplicate conditions, recovery test (retry without duplicates) |
| PR-07 | **Day counting** wrong for half days, holidays or company leave | BR-01 | 3 | 4 | **12** | Medium | #15 specific holiday of another employee excluded; #17 complementary half days refused | Basis-path testing of `calculate_requested_days` (V(G)=6), unit tests with mocked calendars, custom `day_breakdown_swap` mutants |
| PR-08 | **Overlapping leave** accepted, or valid complementary halves refused | BR-02, FR-07 | 3 | 4 | **12** | Medium | #17 complementary half days refused by API | MCC/MC-DC of the 5-condition half-day exception (20 feasible rows), overlap BVA (adjacent day) |
| PR-09 | **Vulnerable third-party dependency** in the deployed stack | n/a | 3 | 3 | **9** | Medium | to be measured by `pip-audit` | Dependency audit (pip-audit), SonarQube security issues ratchet in CI |
| PR-10 | **Slow response** for the balance/request API under several users | FR-10 | 2 | 3 | **6** | Low | none yet | k6 load: 1 VU and 5 VUs, twice each, p95 and failure-rate targets |
| PR-11 | **Accessibility barriers** on the leave forms (keyboard, labels, error messages) | FR-01, FR-05 | 3 | 2 | **6** | Low | none yet | Lighthouse + axe-core scans, Playwright keyboard navigation test, one screen fixed and re-scanned |

## 3. Project risks

| ID | Risk | L | I | Score | Level | Mitigation / contingency |
|---|---|---|---|---|---|---|
| PJ-01 | **Schedule:** the 29 Nov deadline leaves little slack for the remaining areas | 4 | 4 | **16** | High | Risk-based ordering (high risks first); weekly progress report with control actions; CI gate runs unattended |
| PJ-02 | **Team capacity:** reduced availability of one member; work reallocated by team agreement | 4 | 4 | **16** | High | Areas re-planned between the other two members (2026-11-26); remaining work tracked in the progress report |
| PJ-03 | **AI-generated work not understood** by its owner, so components fail the viva | 3 | 5 | **15** | High | AI-use record per output with "what we checked"; viva TODOs recorded per component; each owner reruns and explains their tests |
| PJ-04 | **Environment:** heavy setup (10+ min migrations, Windows limits such as mutmut needing `fork()`) | 4 | 3 | **12** | Medium | SQLite snapshot reset, in-memory unit DB, WSL for mutation, Linux CI runners |
| PJ-05 | **CI capacity:** free-tier runner concurrency and a 48-minute gate slow feedback | 4 | 2 | **8** | Medium | Parallel jobs, concurrency cancel on new pushes, fast unit/mutation jobs give feedback first |

## 4. 5 × 5 risk matrix

Rows = likelihood, columns = impact. Cell = risk IDs (score).

| L \ I | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | | | PR-05 (15) | PR-02 (20) | PR-01 (25) |
| **4** | | PJ-05 (8) | PR-06 (12), PJ-04 (12) | PR-04 (16), PJ-01 (16), PJ-02 (16) | PR-03 (20) |
| **3** | | PR-11 (6) | PR-09 (9) | PR-07 (12), PR-08 (12) | PJ-03 (15) |
| **2** | | | PR-10 (6) | | |
| **1** | | | | | |

## 5. How risk level decides technique and depth

| Level | Depth applied | Applied to |
|---|---|---|
| **High (15–25)** | White-box 100% statement + branch, MCC and MC/DC on compound decisions, mutation ≥95% with no unexplained survivor, API EP + 3-point BVA with read-back, state-transition (all allowed + ≥1 disallowed per state), access matrix | PR-01, PR-02, PR-03, PR-04, PR-05 |
| **Medium (8–14)** | EP + BVA, decision tables, targeted unit tests, tool scans with findings triaged | PR-06, PR-07, PR-08, PR-09 |
| **Low (1–7)** | Tool-based measurement against a target, one automated scenario per workflow | PR-10, PR-11 |

## 6. Exit criteria (measurable)

At least two are tied to the highest risks. The three marked **R** are the release criteria reported as actual vs target in the completion report.

| ID | Criterion | Target | Measured by | Risks |
|---|---|---|---|---|
| **EC-1 R** | Business-logic test strength | 100% statement and branch coverage of the 15 scoped functions **and** mutation score ≥ 95% with 0 unexplained survivors | CI `unit` and `mutation` jobs | PR-01, PR-02 |
| **EC-2 R** | Cross-employee access and state safety | 100% of access-matrix checks and state-transition tests pass; **0 open high-severity** defects in PR-01/PR-03/PR-04 | Playwright access checks, API state tests, GitHub Issues | PR-03, PR-04, PR-01 |
| **EC-3 R** | Performance of the selected operation | p95 ≤ 500 ms and < 1% unexpected failures at 5 concurrent users | k6 runs | PR-10 |
| EC-4 | No server errors on invalid input | 0 HTTP 500 across all generated invalid-input API cases | Area 2 API suite | PR-05 |
| EC-5 | Accessibility of the fixed screen | 0 critical/serious axe-core violations after the fix | axe-core + Lighthouse before/after | PR-11 |
