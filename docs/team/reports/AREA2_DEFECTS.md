## Verified Prompt 3 result — 25 November 2026

This source-specific result supersedes historical incomplete-input, pending-retest
and unanswered OD-01/OD-02 labels below. On `fecac354c9b5d8ea47ac732a2b089ed3cc148620`,
[run 45609322121](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322121) passed **3,433/3,433 API
cases in EACH independent order**, with no failures, errors, required skips or
missing IDs. The strict complete-scope guard accepted both orders.
**713/713 canonical generated IDs, all former 399 missing IDs, and 350/350
mandatory input families are verified.** Explicit requirement assertion selectors
verify FR-01–FR-10 and BR-01–BR-04; tags or mappings alone are not the evidence.

The authoritative source-bound summaries and individual rows are in
`docs/team/finish-line/PROMPT03_EXECUTION_SUMMARY.json`,
`PROMPT03_REQUIREMENT_EVIDENCE.json`, `PROMPT03_INPUT_LEDGER.json` and
`REMAINING_WORK.json`. The derived complete coverage, case-execution and generated-ID
ledgers remain in [artifact 15024156843](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322121/artifacts/15024156843).

Separate overlapping populations on the same source passed: 482 business/state/
role/workflow cases; 82 affected upstream tests; 24 original team units; 16
focused regressions; eight focused upstream tests; 182 expanded cases; 238 wire
validation cases; seven advanced-filter cases; 27 further upstream tests plus
two subtests; all ten personal browser flows; two fresh foundations with five
smoke cases each; 68 tooling and four media-reader checks. Regeneration passed
six baseline cases and retained exactly two predicted strict variant failures
with four passes, in its separate controlled experiment. These totals are not
added into a larger unique-case count.

Prompt 3's scoped technical work is complete. **Whole-project release remains
HOLD** pending accepted integration, owner/shared quality gates and Prompt 4's
final integrated/report/package/ownership closeout. PR #8 remains draft/open;
no owner approval, merge, human effort, review or viva is inferred.

The current distinct-defect population remains 22 across dated builds: original seven + eight Prompt 2 + seven Prompt 3. Issues #3–#6 are merged/retested/closed; #14–#31 remain open pending accepted PR #8 integration. Source corrections, regression fixes and harness repairs do not create additional Pareto defects. Exact fixing commits for P2-01 and P2-02/03/04 are a8a7a7d0 and 59537e7e; 796b84bd is the later common retest source for those earlier fixes.

---

## Prompt 3 reconciled defect records — 25 November 2026

This dated mapping supersedes historical unexecuted/oracle-open labels below.
There are **22 distinct confirmed Area 2 product defects across dated builds**:
the historical seven, eight Prompt 2 defects and seven Prompt 3 defects. Issue
#1 is coordination; Area 1 Issues #11–#13 and harness failures are outside this
population. Three missing historical product records were created as #29–#31
under rayyanhasan899; they remain open pending PR #8 integration.

| Stable defect | Product Issue | Behavior | Actual correction | Lifecycle |
|---|---|---|---|---|
| A2-D01 | [#4](https://github.com/includeduck/SQE-Horilla-Project/issues/4) | rejecting approved leave refunds the acting approver instead of requester | `546cb620` | Merged/retested; closed |
| A2-D02 | [#5](https://github.com/includeduck/SQE-Horilla-Project/issues/5) | foreign-owned self-allocation PUT and DELETE return 500 | `546cb620` | Merged/retested; closed |
| A2-D03 | [#6](https://github.com/includeduck/SQE-Horilla-Project/issues/6) | API leave creation ignores carry-forward policy cap | `546cb620` | Merged/retested; closed |
| A2-D04 | [#29](https://github.com/includeduck/SQE-Horilla-Project/issues/29) | Identical pending allocation submissions create duplicate records | `32621b42` | Retested proposal; owner merge pending |
| A2-D05 | [#30](https://github.com/includeduck/SQE-Horilla-Project/issues/30) | Ordinary rejection accepts an already cancelled leave request | `32621b42` | Retested proposal; owner merge pending |
| A2-D09 | [#3](https://github.com/includeduck/SQE-Horilla-Project/issues/3) | accepted extensionless attachment filenames fail storage at 99/100 characters | `a1cfb4ab` | Merged/retested; closed |
| A2-D10 | [#31](https://github.com/includeduck/SQE-Horilla-Project/issues/31) | Browser allocation form accepts an empty requested-days amount | `bf44fe6c` | Retested proposal; owner merge pending |
| A2-P2-01 | [#21](https://github.com/includeduck/SQE-Horilla-Project/issues/21) | Malformed employee identifiers crash the target permission lookup | `a8a7a7d0` | Retested proposal; owner merge pending |
| A2-P2-02 | [#22](https://github.com/includeduck/SQE-Horilla-Project/issues/22) | Non-object API bodies crash server-owned identity injection | `59537e7e` | Retested proposal; owner merge pending |
| A2-P2-03 | [#23](https://github.com/includeduck/SQE-Horilla-Project/issues/23) | Invalid groupby_field escapes as an API server error | `59537e7e` | Retested proposal; owner merge pending |
| A2-P2-04 | [#24](https://github.com/includeduck/SQE-Horilla-Project/issues/24) | Generic allocation creation accepts an unauthorized foreign employee | `59537e7e` | Retested proposal; owner merge pending |
| A2-P2-05 | [#25](https://github.com/includeduck/SQE-Horilla-Project/issues/25) | Zero detail IDs lose the route argument in permission dispatch | `796b84bd` | Retested proposal; owner merge pending |
| A2-P2-06 | [#26](https://github.com/includeduck/SQE-Horilla-Project/issues/26) | Malformed AJAX relation filter choices crash before form validation | `796b84bd` | Retested proposal; owner merge pending |
| A2-P2-07 | [#27](https://github.com/includeduck/SQE-Horilla-Project/issues/27) | Sessionless JWT HTML API responses crash sidebar menu construction | `796b84bd` | Retested proposal; owner merge pending |
| A2-P2-08 | [#28](https://github.com/includeduck/SQE-Horilla-Project/issues/28) | Malformed registered advanced date filters return 500 | `796b84bd` | Retested proposal; owner merge pending |
| A2-P3-01 | [#14](https://github.com/includeduck/SQE-Horilla-Project/issues/14) | API accepts zero and negative effective leave duration | `e4d6f3ce` | Retested proposal; owner merge pending |
| A2-P3-02 | [#15](https://github.com/includeduck/SQE-Horilla-Project/issues/15) | API excludes another employee's specific holiday and accepts an over-balance request | `e4d6f3ce` | Retested proposal; owner merge pending |
| A2-P3-03 | [#16](https://github.com/includeduck/SQE-Horilla-Project/issues/16) | API refuses valid forecast entitlement at and after the reset boundary | `e4d6f3ce` | Retested proposal; owner merge pending |
| A2-P3-04 | [#17](https://github.com/includeduck/SQE-Horilla-Project/issues/17) | API rejects complementary non-overlapping half-day leave requests | `e4d6f3ce` | Retested proposal; owner merge pending |
| A2-P3-05 | [#18](https://github.com/includeduck/SQE-Horilla-Project/issues/18) | Approval ignores current carry-forward policy/cap | `e4d6f3ce` | Retested proposal; owner merge pending |
| A2-P3-06 | [#19](https://github.com/includeduck/SQE-Horilla-Project/issues/19) | Malformed approved-allocation rejection deducts balance before returning 400 | `e4d6f3ce` | Retested proposal; owner merge pending |
| A2-P3-07 | [#20](https://github.com/includeduck/SQE-Horilla-Project/issues/20) | Generic update lets an ordinary owner transfer a request to another employee | `e4d6f3ce` | Retested proposal; owner merge pending |

All seven new business defects were reproduced before source edits. Complete
decoded before logs are in evidence/area2/finish-03/; Issues #14–#20 retain exact
request, actual response and balance snapshots and link the tested source/run.
The expanded ownership failure belongs to the completed shard of the later
cancelled run 45544984779, not a completed full-suite baseline. Initial business
baseline 45544239475: 354 cases, 315 passes, 39 failures; 27 failing cases
represented six product defects and twelve represented the incorrect
TextField.clean harness assumption. Multiple cases do not create extra defects.

The positive-duration fix initially changed inverted-date error precedence.
Source 13200cd9 / run 45549984738 returned HTTP 400 with non_field_errors where
the unchanged canonical tests require end_date. Correction 4a719a17 restores
early field-specific date-order refusal before calculating duration. It is a
follow-up to A2-P3-01, with its before JSON/excerpt retained, not an extra
Pareto defect. Required test assertions were not relaxed.

Reject/cancel reasons are source-backed optional normalized text: null,
omission and nonstrings are ignored, strings are stripped then capped at 1000.
LeaveRequest.reject_reason declares TextField(max_length=255); real SQLite
persistence and TextField.clean accept tested text above 255. The 254/255/256
and 999/1000/1001 tests distinguish these boundaries. No PostgreSQL enforcement
or new mandatory-reason policy is claimed; whole non-object bodies are refused
before state/balance mutation. A2-D08 is a reconciled contract discrepancy,
not a newly fabricated confirmed product defect. Allocation numeric positivity
(A2-D06) remains outside the accepted effective-duration rule.

Current final passing-after/full-scope evidence is recorded at the top of
RAYYAN_FINISH_03_STATUS.md and PROMPT03_EXECUTION_SUMMARY.json. No unmerged
Issue is closed on the strength of automated results alone; owner review and
accepted integration remain separate from the technical retest.

---

Historical dated records follow. Current source-specific results above supersede their older pending/count labels.

# Area 2 endpoint findings and triage

## Latest verified corrections - 24 November 2026

This section supersedes historical oracle-open and retest-pending labels below.
Source 32621b42, run 45355537962 verified 16 focused regressions, eight upstream,
177 expanded and 275 full first-order API passes as separate populations. The
reverse collection timed out; no full-run/repeatability acceptance is inferred.
Raw log: ../evidence/area2/phase-c/ci-45355537962-job.log.

| Finding | Established correction and actual passing-after evidence | Residual limitation |
|---|---|---|
| A2-D04 pending duplicate | Owner OD-02 defines employee/type/days/description identity. Shared create serializer rejects a second requested record with 400. Strict test covers both create routes, unchanged state, distinct amount/description and approved history; passed focused and full-first collections. | Sequential API resubmission guard; concurrent idempotency and a UI-wide uniqueness policy are not claimed. Medium/P2 remains proposed triage; risk A2-R03. |
| A2-D05 cancelled-to-rejected | Owner OD-01 confirms terminal cancellation. Reject handler returns 400 before state/refund mutation. Unchanged STATE-LEAVE-cancelled-reject assertion passed focused and full-first collections. | Other accepted workflow/input coverage and group review remain open. Medium/P2 remains proposed triage; risk A2-R04. |
| A2-D10 blank form amount | Individual allocation form now requires requested_days. Run 45355537997 verified unchanged UC-RAY-01-E2 rejection, no new row and unchanged balances; the four valid/correction/file/type flows passed too. | PR #8 remains draft/unmerged. No positive amount minimum was invented. Medium/P1 proposed; risks A2-R01/A2-R07. |

All three genuine failing-before logs are retained. A2-D04/D05 were reproduced
before owner-policy reconciliation; A2-D10 was exposed by real browser state.
Later Create-selector failures are this agent's harness regressions, not more
product defects. Seven distinct corrected/retested defects now have evidence
across the historical merged and current draft sources; the original four-defect
Pareto population remains dated and a separate seven-defect update is supplied.

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
| A2-D01 | FR-09: rejecting approved leave restores its requester's deducted days; `LeaveRequestRejectAPIView.leave_calculation` and cancellation refund helper identify the balance being restored | `put` passes `request.user.employee_get` into the refund lookup. `test_refund_belongs_to_requester` sets requester 5�+'2 and approver 7, then expects requester 5 / approver 7 | High / P1 / A2-R-BALANCE | Static candidate; regression implemented; real observed result/retest pending retrieval. Do not claim correction yet. |
| A2-D02 | BR-04: non-owners receive controlled access denial, consistent with generic allocation ownership decorator | `EmployeeLeaveAllocationUpdateDeleteAPIView.get_allocation_request` returns None for an existing foreign-owned record; PUT/DELETE dereference `.status`. Two `test_nonowner_self_allocation_route_denied` cases expect 403 and unchanged state | Medium / P1 / A2-R-OWNERSHIP | Static candidate; real HTTP result pending. Proposed correction: explicit existing permission/ownership denial, preserving valid owner behavior. |
| A2-D03 | FR-06 / BR-01: effective balance respects policy/cap/forecast, per `LeaveRequest.clean` | `leave_Validations` adds raw available+carry-forward; cap regression uses available 0, carry 5, cap 1, request 3 | High / P1 / A2-R-BALANCE | Static candidate; real outcome pending. Any fix must preserve source-backed forecast/employee holiday semantics and run affected regressions. |
| A2-D04 | Assignment repetition/no-duplicates expectation needs a defined logical identity | Identical pending employee/type/amount/description submissions have no visible deduplication/idempotency contract. `test_allocation_duplicate_creation_contract` explicitly proposes a 400 rejection with no extra row | Provisional medium / P2 / A2-R-DUPLICATE | **Oracle decision open.** Do not introduce a new uniqueness policy merely to pass. Owner must choose rejection/idempotent behavior consistent with scope; retain any real failing evidence. |
| A2-D05 | Draft BR-03 treats cancelled/rejected states as terminal | Ordinary leave rejection excludes rejected/cancel_requested but apparently allows cancelled�+'rejected. State catalog expects terminal refusal | Provisional medium / P2 / A2-R-STATE | **Oracle reconciliation open.** Source/draft disagreement is visible; no acceptance by teammates or instructor is invented. |
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

## Attachment failure and protected-branch update �?" 23 November 2026

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


## Final first-pass evidence and corrective proposals �?" 23 November 2026

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
