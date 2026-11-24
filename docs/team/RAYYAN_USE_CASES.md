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
use its Create control; select assigned type and own employee; enter five days
and a description; click the application's Save control. Expected displayed
result: success notification. Postconditions: exactly one owned requested
allocation for five days, exact description/type, balance still zero until
approval. HTTP detail/list and independent ORM corroborate persistence.

| Flow / executable ID | Deviation and steps | Displayed assertion | Persistent postconditions |
|---|---|---|---|
| MAIN / UC-RAY-01-MAIN | Submit five days with description | Success alert | One requested allocation; zero balance |
| Alternative 1 / UC-RAY-01-A1 | Attach synthetic PDF before submitting | Success alert | Same record/owner/amount; stored file bytes equal uploaded bytes |
| Alternative 2 / UC-RAY-01-A2 | Submit blank description; read required-field error; enter description and resubmit | Error first, then success | No row/balance change on first attempt; exactly one row after correction |
| Exception 1 / UC-RAY-01-E1 | Clear required leave type and submit | Required-field error | No allocation and unchanged all-user balances |
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
requested three-day leave, exact dates/type/description; balance remains five
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
password settings and existing databases are preserved. Runtime results remain
pending until actual JUnit/visible/persistent assertions finish. Implementation
is not a pass. Keyboard/Lighthouse/axe/ZAP/k6/recovery completeness is not claimed.
