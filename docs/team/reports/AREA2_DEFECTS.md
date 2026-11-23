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
