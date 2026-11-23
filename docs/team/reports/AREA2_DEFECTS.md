# Area 2 endpoint findings and triage

Syed Muhammad Rayyan Hassan, **24I-3000**, 23 November 2026.

This ledger separates **static candidates**, **reproduced failures** and
**corrected/retested defects**. A static source finding or unexecuted regression
is not a reproduced result. Current actual CI evidence must be attached below
or in the C status before changing a candidate's verification state.

| ID | Expected behavior and source | Static observation / reproducer | Severity / priority / risk | Verification and triage |
|---|---|---|---|---|
| A2-D01 | FR-09: rejecting approved leave restores its requester's deducted days; `LeaveRequestRejectAPIView.leave_calculation` and cancellation refund helper identify the balance being restored | `put` passes `request.user.employee_get` into the refund lookup. `test_refund_belongs_to_requester` sets requester 5→2 and approver 7, then expects requester 5 / approver 7 | High / P1 / A2-R-BALANCE | Static candidate; regression implemented; real observed result/retest pending retrieval. Do not claim correction yet. |
| A2-D02 | BR-04: non-owners receive controlled access denial, consistent with generic allocation ownership decorator | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` returns None for an existing foreign-owned record; PUT/DELETE dereference `.status`. Two `test_nonowner_self_allocation_route_denied` cases expect 403 and unchanged state | Medium / P1 / A2-R-OWNERSHIP | Static candidate; real HTTP result pending. Proposed correction: explicit existing permission/ownership denial, preserving valid owner behavior. |
| A2-D03 | FR-06 / BR-01: effective balance respects policy/cap/forecast, per `LeaveRequest.clean` | `leave_Validations` adds raw available+carry-forward; cap regression uses available 0, carry 5, cap 1, request 3 | High / P1 / A2-R-BALANCE | Static candidate; real outcome pending. Any fix must preserve source-backed forecast/employee holiday semantics and run affected regressions. |
| A2-D04 | Assignment repetition/no-duplicates expectation needs a defined logical identity | Identical pending employee/type/amount/description submissions have no visible deduplication/idempotency contract. `test_allocation_duplicate_creation_contract` explicitly proposes a 400 rejection with no extra row | Provisional medium / P2 / A2-R-DUPLICATE | **Oracle decision open.** Do not introduce a new uniqueness policy merely to pass. Owner must choose rejection/idempotent behavior consistent with scope; retain any real failing evidence. |
| A2-D05 | Draft BR-03 treats cancelled/rejected states as terminal | Ordinary leave rejection excludes rejected/cancel_requested but apparently allows cancelled→rejected. State catalog expects terminal refusal | Provisional medium / P2 / A2-R-STATE | **Oracle reconciliation open.** Source/draft disagreement is visible; no acceptance by teammates or instructor is invented. |
| A2-D06 | Positive allocation policy is not established by current API/schema | Required FloatField has no positive minimum or finite maximum; generated negative/zero classes currently document schema acceptance | Policy question / unscored / A2-R-CONTRACT | Do not fabricate a >0 allocation rule or maximum ten. Distinguish allocation amount from the documented positive effective leave-duration rule. |
| A2-D07 | BR-01 requires positive effective duration; date exclusions should use employee context | Serializer computes effective days without employee argument and lacks the model's positive-effective check; model includes capped carry-forward and forecast | High candidate / P1 / A2-R-BALANCE | Additional real zero-effective/employee-holiday/forecast reproducers still needed; assigned completion H-03/H-04. |
| A2-D08 | Optional rejection-reason compatibility must reconcile helper versus persistence | Helper trims/ignores nonstring/caps at 1000; leave request model reason has a different declared bound | Contract candidate / P2 / A2-R-CONTRACT | Missing generated normalization/persistence coverage remains H-03, not a fabricated defect result. |

## Required reproduction record

For every confirmed finding retain build SHA, generated case/spec/data identity,
normal user role, pre-state, HTTP method/path/body (no token), actual response,
post-state and exact failed assertion. A corrective change needs its own commit,
retest command and actual passing/failing result, with upstream totals separate.

Do not use xfail, unconditional skip, broad accepted status sets, modified
expectations or failure suppression to make a defect disappear. No application
source correction has been established by this initial static ledger.

## Shared defect-management obligations

The owner handoff is [issue #1](https://github.com/includeduck/SQE-Horilla-Project/issues/1).
It is a coordination issue, not proof that the product candidates above are
reproduced. Create/update genuine product Issues after reproduction, with
severity, priority, status, triage, root cause, corrective/preventive actions and
retest. The required two major-defect 5 Whys/fishbone analyses, Pareto categories,
and fixed/blocked PR evidence must use actual results. No fictional RCA meeting,
closed/reopened issue, PR or passing-after result is recorded here.

## Attachment failure and protected-branch update — 23 November 2026

Remote run 45183086568 reproduced storage exceptions for generated allocation
attachment filename boundaries 99 and 100 (log lines 1720/1816). The original
`horilla.models.upload_path` treated a filename without a dot as an extension,
leaving storage no basename to shorten within the FileField path budget.
A narrow correction now retains extensionless input as the basename; dotted
names retain their suffix. Four real FileSystemStorage regressions and the
existing five HTTP slice cases are configured as a targeted remote retest.
The source fix is proposed, not verified until those tests actually finish.
This supersedes earlier statements that application source is unchanged.

Branch protection now requires PRs. Evidence commit `b6e298ae646738e1122528b2835d7aa08f1f7015`
was published on `rayyan/phase-c-evidence` in PR #2, after its direct update to
`sqe-team` was rejected. Do not bypass protection. Wasay was notified through
issue #1 comment 7102792706. Further proposed corrections/evidence use the same
review branch; owner review/merge and group gate remain required.


## Final first-pass evidence and corrective proposals — 23 November 2026

Build `1948e0f`, run 45183086568 completed: W1/W2 preflight **1 passed**;
full collection **169 passed, 9 failed**, 184 warnings, 1038.66 seconds.
There were no setup errors in this collection. Reverse and completeness stages
were blocked by the failing first pass. Raw log: `ci-45183086568-job.log`;
summary: `ci-third-summary.json`; remote artifact 14824755317. Preflight repeats
one API scenario and does not increase the 178 unique-case denominator.

Confirmed failures: A2-D01 refund leaves requester balance at 2 instead of 5;
A2-D02 non-owner PUT/DELETE return 500 instead of controlled 403; A2-D03 raw
carry-forward accepts three days (201) despite effective cap one; A2-D09 valid
99/100 extensionless attachments trigger storage failure. Proposed narrow fixes
restore the requester, explicitly deny a foreign owner, apply existing model
carry-forward cap/policy in the serializer, and correctly split upload names.
Forecast/employee-holiday scope remains unfinished; this cap correction does
not claim to implement those separate gaps.

A2-D04 duplicate allocation and A2-D05 cancelled-to-rejected behavior also fail
the provisional tests. Their oracles conflict with current behavior and require
Wasay's explicit business-rule reconciliation. They are not silently fixed or
marked as successful. The targeted corrective retest additionally runs affected
upstream balance/carry-forward/file-display tests separately. Actual passing-after
results and full clean/reversed acceptance remain pending.

