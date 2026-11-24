# Area 2 endpoint findings and triage

## Verified result update - 24 November 2026

This update supersedes the earlier static/pending labels below. PR #2 was merged
as `2242c502090c81031e20df912b49809a03a1f523`. Run 45197384096 passed 14 focused
regressions and eight affected upstream tests; full API result was 176 passed /
2 failed. A2-D01, A2-D02, A2-D03 and A2-D09 are **corrected and retested on that
merged build**. A2-D04 and A2-D05 still fail their unresolved provisional
oracles. A2-D06/D07/D08 remain policy questions/candidates, not retested fixes.

See [AREA2_RCA_CONTRIBUTION.md](AREA2_RCA_CONTRIBUTION.md) for two major-defect
5 Whys/cause diagrams, corrective/preventive actions and a Pareto table over
four confirmed defects. Nine failing cases before correction represented four
confirmed defects plus two oracle disputes; do not equate case failures to
unique defects. Raw merged-run evidence is in
`../evidence/area2/phase-c/ci-45197384096-job.log`. The original failed run is
retained separately. Product Issues/closure/triage and final group reporting
remain mandatory Wasay handoffs. No new Issue was posted during this turn.

Syed Muhammad Rayyan Hassan, **24I-3000**, 23 November 2026.

This ledger separates **static candidates**, **reproduced failures** and
**corrected/retested defects**. A static source finding or unexecuted regression
is not a reproduced result. Current actual CI evidence must be attached below
or in the C status before changing a candidate's verification state.

| ID | Expected behavior and source | Static observation / reproducer | Severity / priority / risk | Verification and triage |
|---|---|---|---|---|
| A2-D01 | FR-09: rejecting approved leave restores its requester's deducted days; `LeaveRequestRejectAPIView.leave_calculation` and cancellation refund helper identify the balance being restored | `put` passes `request.user.employee_get` into the refund lookup. `test_refund_belongs_to_requester` sets requester 5â†’2 and approver 7, then expects requester 5 / approver 7 | High / P1 / A2-R-BALANCE | Static candidate; regression implemented; real observed result/retest pending retrieval. Do not claim correction yet. |
| A2-D02 | BR-04: non-owners receive controlled access denial, consistent with generic allocation ownership decorator | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` returns None for an existing foreign-owned record; PUT/DELETE dereference `.status`. Two `test_nonowner_self_allocation_route_denied` cases expect 403 and unchanged state | Medium / P1 / A2-R-OWNERSHIP | Static candidate; real HTTP result pending. Proposed correction: explicit existing permission/ownership denial, preserving valid owner behavior. |
| A2-D03 | FR-06 / BR-01: effective balance respects policy/cap/forecast, per `LeaveRequest.clean` | `leave_Validations` adds raw available+carry-forward; cap regression uses available 0, carry 5, cap 1, request 3 | High / P1 / A2-R-BALANCE | Static candidate; real outcome pending. Any fix must preserve source-backed forecast/employee holiday semantics and run affected regressions. |
| A2-D04 | Assignment repetition/no-duplicates expectation needs a defined logical identity | Identical pending employee/type/amount/description submissions have no visible deduplication/idempotency contract. `test_allocation_duplicate_creation_contract` explicitly proposes a 400 rejection with no extra row | Provisional medium / P2 / A2-R-DUPLICATE | **Oracle decision open.** Do not introduce a new uniqueness policy merely to pass. Owner must choose rejection/idempotent behavior consistent with scope; retain any real failing evidence. |
| A2-D05 | Draft BR-03 treats cancelled/rejected states as terminal | Ordinary leave rejection excludes rejected/cancel_requested but apparently allows cancelledâ†’rejected. State catalog expects terminal refusal | Provisional medium / P2 / A2-R-STATE | **Oracle reconciliation open.** Source/draft disagreement is visible; no acceptance by teammates or instructor is invented. |
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

## Attachment failure and protected-branch update â€” 23 November 2026

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


## Final first-pass evidence and corrective proposals â€” 23 November 2026

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

## Retrieved owner decision - 24 November 2026

Issue #1 contains a 23 November comment by includeduck confirming both strict
400 oracles: cancelled leave must not be rejected again (BR-03 / OD-01), and
an identical pending allocation must not create a duplicate (OD-02). This
supersedes earlier statements that Wasay had not answered those two policies.
The comment's D04/D05 labels reverse this ledger's existing labels; match by
behavior and test name, preserving existing IDs rather than silently renumbering.

The existing tests still assert 400 and unchanged persistent state. The current
Phase D instruction requires genuine failures to remain visible, so the owner's
requested xfail markers have not been added. No product correction or retest
is inferred from a comment. The concrete remaining work is the two narrow
product fixes and strict passing retests, not asking for the same decision again.
The same comment confirms merged PRs #2/#7 and requests evidence-backed closure
of Issues #3-#6. Their technical fixes/retests already exist; issue lifecycle
changes require the authorized owner workflow.

Source: https://github.com/includeduck/SQE-Horilla-Project/issues/1 (includeduck
comment updated 2026-11-23T14:46:01Z). No new external message was sent here.

## Fifth browser result and product correction

Run 45353554904 / browser job 138305655757 on 8593715e verified the first four
allocation flows, including E1 required-type validation. UC-RAY-01-E2 failed:
blank requested_days was accepted and the real allocation table displayed a
new requested record with None days. The other five leave flows were not reached
under the then-enabled maxfail=1. This is a product validation failure, not a
selector error. Raw evidence: ci-45353554904-browser-fifth.log.

A2-D10: LeaveAllocationRequestForm inherited the model's nullable/blank amount
without overriding requiredness. The API serializer and bulk allocation form
already require requested_days. FR-01 and the existing amount contract support
requiring it in the individual form too. The narrow correction marks only that
form field required; no model migration, positive minimum, maximum or production
password/auth change is introduced. The unchanged browser E2 assertion is the
regression and the four passing creation/correction/file flows protect valid use.

With fixture/login setup now verified, the next browser job executes every flow
instead of stopping on the first failure, retaining all independent results.
The fix is proposed until the actual full retest completes. Severity medium,
priority P1, risks A2-R01/A2-R07; do not count it as retested or add it to the
earlier four-defect Pareto population without identifying the new population.
This agent is implementing/retesting the fix; it is not assigned to Wasay.

## Two previously blocked oracle fixes implemented here

The published SCOPE.md already contains Wasay's OD-01 and OD-02 decisions,
confirmed by his issue #1 comment. This agent therefore implemented the two
narrow corrections rather than assigning those easy fixes back to Wasay:
reject ordinary rejection of cancelled leave before refund/state mutation;
reject an allocation matching employee/type/days/description of an existing
requested allocation in the shared create serializer (both creation routes).
The existing strict assertions remain; no xfail is added. Duplicate coverage
also verifies distinct descriptions/amounts and non-pending history remain valid.

The focused CI collection now contains those two additional regressions (16
cases rather than the prior 14), separate from the unchanged 275 unique API
case denominator. Actual passing retests are pending; old failing logs remain.
This is sequential repeated-submission protection, not a claim of concurrent
idempotency or a new database-wide uniqueness policy.
