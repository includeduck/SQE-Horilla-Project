## Final execution closeout — 25 November 2026

Rayyan's project execution assignment is finished. **Whole-project release: HOLD.** No further technical execution or additional prompt is expected from Rayyan.

The final application/API verification source is `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`; Actions checked synthetic merge `801351079aada8c399db2212d9c033737e032e0d` with `sqe-team` base `0a5ac6443dadb50ab5fd6ea749f41dd108a19486`. [Run 45627793460](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45627793460) verifies **3,433/3,433 API cases in each of two orders**, with zero failures/errors/skips/missing IDs and strict complete-scope acceptance. Each collection is the exact union of 16 fresh isolated deterministic shards; reversal occurs within each shard, not a claim of one monolithic reversed process.

**713/713 generated IDs, all former 399 missing IDs, 350/350 mandatory input families, FR-01–FR-10 and BR-01–BR-04 are verified** from real source-bound assertions. Ten personal browser flows pass; the consuming regeneration has six baseline passes and exactly two predicted strict variant failures with four passes. Separate overlapping populations and full links are in [RAYYAN_FINAL_CLOSEOUT.md](reports/RAYYAN_FINAL_CLOSEOUT.md), the final evidence index and machine ledger. Never sum them into a fictitious unique-test total.

All remaining project execution is **Wasay / Wasay's agent — mandatory**, with exact attempts, dependencies and acceptance in root [handoff.md](../../handoff.md) and `finish-line/REMAINING_WORK.json`. Current shared gate evidence is genuinely red for missing Sonar service/credentials and mutation runner/policy; supplied units pass. No independent review, merged PR #8, required branch/deploy enforcement, teammate authorship, human effort or passed viva is inferred.

The PDF/ZIP is a **Rayyan contribution, not the final group submission**. Earlier dated results/ownership below are historical and superseded by the final handoff; they do not assign new execution to Rayyan.

---

---

### Final per-flow outcomes — run45627793417

| Flow | Actual outcome | Visible/persistent assertion |
|---|---|---|
| UC-RAY-01-MAIN | passed | Five-day requested allocation; zero balance |
| UC-RAY-01-A1 | passed | Uploaded synthetic file bytes match owned record |
| UC-RAY-01-A2 | passed | Description error then one successful corrected record |
| UC-RAY-01-E1 | passed | Missing type refused; no row or balance mutation |
| UC-RAY-01-E2 | passed | Missing amount refused; no row or balance mutation |
| UC-RAY-02-MAIN | passed | Three-day requested leave; unchanged five-day balance |
| UC-RAY-02-A1 | passed | Same-day matching half produces exactly0.5 requested day |
| UC-RAY-02-A2 | passed | Insufficient-balance error then one corrected three-day leave |
| UC-RAY-02-E1 | passed | Insufficient balance refused; unchanged records/funds |
| UC-RAY-02-E2 | passed | End-before-start refused; unchanged records/funds |

## Historical dated appendix (not current ownership or pending work)

# Rayyan's personal use cases

Contributor: Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B. Prepared 24 November 2026.
These specifications and automation are Rayyan's proposed personal contribution.
The current checkout and open PR inventory contain no Zain browser framework or
case allocation; no teammate acceptance is invented. Zain retains his wider
Area 3 evaluations. IDs remain available for reconciliation without duplicating
another member's work.

## UC-RAY-01: employee submits a leave allocation request

Workflow W1; FR-01/FR-04/FR-10 and BR-04. Actor: normal employee Team Employee.
Preconditions: disposable seeded company, assigned Team Annual Leave type,
available/carry-forward balances zero, no allocation/leave requests, distinct
approver/outsider accounts. Admin is used for fixture setup only.

Main steps: sign in through the real login form; open Leave Allocation Requests;
use its Create control; select the assigned type and verify the form binds the signed-in employee; enter five days
and a description; click the application's Save control. Expected displayed
result: success notification. Postconditions: exactly one owned requested
allocation for five days, exact description/type, balance still zero until
approval. HTTP detail/list and independent ORM corroborate persistence.

| Flow / executable ID | Deviation and steps | Displayed assertion | Persistent postconditions |
|---|---|---|---|
| MAIN / UC-RAY-01-MAIN | Submit five days with description | Success alert | One requested allocation; zero balance |
| Alternative 1 / UC-RAY-01-A1 | Attach synthetic PDF before submitting | Success alert | Same record/owner/amount; stored file bytes equal uploaded bytes |
| Alternative 2 / UC-RAY-01-A2 | Submit blank description; read required-field error; enter description and resubmit | Error first, then success | No row/balance change on first attempt; exactly one row after correction |
| Exception 1 / UC-RAY-01-E1 | Leave required type unselected and submit | Required-field error | No allocation and unchanged all-user balances |
| Exception 2 / UC-RAY-01-E2 | Clear requested amount and submit | Required-field error | No allocation and unchanged all-user balances |

## UC-RAY-02: employee requests leave using W1's balance

Workflow W2; FR-05/FR-06/FR-07/FR-10 and BR-01/BR-02. Actor: same normal employee.
Preconditions: W1 setup creates and approves allocation five through the existing
real HTTP fixture; balance five; no leave request, no holiday/company exclusions,
future non-overlapping dates, leave type requires approval and no attachment.
The target W2 write is always through the actual browser form.

Main steps: sign in; open My Leave Requests; use Create; select assigned type;
enter future start/end spanning three full days and a description; Save.
Expected displayed result: success notification. Postconditions: one owned
requested three-day leave, exact description/owner/amount; balance remains five
while requested. Approval/debit is already tested by the C integration scenario;
this use case does not claim a UI approval action was automated.

| Flow / executable ID | Deviation and steps | Displayed assertion | Persistent postconditions |
|---|---|---|---|
| MAIN / UC-RAY-02-MAIN | Submit three full days | Success alert | One requested leave; balance five |
| Alternative 1 / UC-RAY-02-A1 | Same date and matching first-half breakdowns | Success alert | Exactly half a requested day; balance five |
| Alternative 2 / UC-RAY-02-A2 | Submit six days against five; read balance error; change to three and resubmit | Correctable balance error, then success | First attempt creates no row; correction creates one three-day row |
| Exception 1 / UC-RAY-02-E1 | Submit six days and stop after rejection | Insufficient-balance error | No leave request; all-user balances unchanged |
| Exception 2 / UC-RAY-02-E2 | Set end before start and submit | Date-order error | No leave request; all-user balances unchanged |

## Automation and counting

`tests/team/e2e/test_rayyan_use_cases.py` parametrizes all ten IDs; each browser
flow is counted once, independently of API-level cases. Playwright controls the
real login/list/modal/form. HTTP/ORM are setup/readback only, not substitutes for
browser target writes. Select2's native select is operated in the browser and
its normal change event is dispatched. No endpoint, form or persistence is mocked.

Run in a complete application environment:

```sh
python -m pip install -r tests/team/requirements-phase-d.txt
python -m playwright install --with-deps chromium
python -m pytest -c tests/team/pytest-area2.ini tests/team/e2e -v -s -o junit_family=xunit1 --junitxml=browser.xml
```

Use `AREA2_BROWSER_EVIDENCE` for a new trace/screenshot directory. The CI runner
uses disposable SQLite/media plus test-only static serving; production URLs,
password settings and existing databases are preserved. Source 7189656a / run
45388276537 verified all ten declared UI flows: 10 passed, zero failures/errors/
skips, 340.34 seconds. The strict HTML completion report succeeded. Actual XML,
log, screenshots and traces are in artifact 14917252664; decoded job log and
browser-verified-summary.json are retained in docs/team/evidence/area2/phase-d/.
Keyboard/Lighthouse/axe/ZAP/k6/recovery completeness is not claimed.
