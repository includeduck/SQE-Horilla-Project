# Phase D implementation status

24 November 2026. Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B.

## Current decision

In progress, **Hold**. The complete attached D prompt (107 lines, 16447 bytes)
was read. Independent D work proceeds while C's open policy/coverage issues stay
explicit. No entire-phase completion or new browser/HTTP pass is inferred.

## Prerequisite verification and repair

Protected sqe-team is `2242c502090c81031e20df912b49809a03a1f523`. Continuation PR #8
head before D work is `3f2fda6bec27fde8165d06375f9e114f2abccb67`; it is draft/open.
Local HEAD remains the preserved `da76b337` checkout plus uncommitted files.

C run 45342013246 completed: 14 focused regressions passed; eight upstream
regressions passed; expanded subset 172 passed / five failed / 177 collected.
All five failures were the new attachment helper's creator-field assertion on
LeaveRequest. Source establishes an optional Employee FK overriding the base
HorillaUser FK; the API does not expose/set it. The test now preserves mandatory
owner/identity/file-byte assertions and checks the actual field model instead
of requiring a nonexistent user-audit contract. This is a test-oracle correction,
not a production fix. Original failure log is retained; runtime retest pending.

C's unresolved duplicate and terminal-state oracles remain unchanged. Current
API inventory is 275 cases / 179 of 578 generated IDs; remaining 399 IDs are
still explicit. D is not certification that A-C requirements have all passed.

## Implemented D work

- Controlled experiment changes two existing SelfAllocationCreate constraints:
  description minLength 1 to 3 and filename budget 100 to 80. These are isolated
  hypothetical spec edits, not invented production limits. Canonical files stay
  unchanged; stale baseline data against variant spec is actually rejected.
- The generator produced different, fingerprinted outputs and structured case
  comparison independently. Baseline expected HTTP results: six passes. Variant
  expected results: four passes and exactly two real strict assertion failures,
  because unchanged production accepts length-two description/filename 81.
- A strict HTTP consumer and runner retain pytest's genuine nonzero variant
  output; any extra failure/error/skip/missing result fails the experiment.
- Two individually attributed browser use-case specifications and all ten flows
  are implemented with actual forms, visible results and HTTP/ORM postconditions.
- Minimal reusable Python Playwright setup, disposable static-serving settings,
  and a free Ubuntu workflow run regeneration and browser activities separately.
  Sonar/mutation thresholds and Wasay's group gate are not replaced.

## Verified independent experiment

Command: `python tests/team/generator/demonstrate_regeneration.py --output
docs/team/evidence/area2/phase-d/independent-regeneration-20261124`.
Exit zero; stale-output rejection and unchanged canonical baseline asserted.
Baseline spec SHA: 45e37bfbcd255fc567d5923b13076637f8777bbc4c48bb239f6c2e3fe398f0db.
Variant spec SHA: 769fa6b449a3f8f9970a74c182b80e1db0e95ede2a36342b74d287583d61c16a.
Full local outputs include both specs/data/comparison; CI recreates these in its
artifact rather than treating a manually rewritten dataset as regeneration.

## Pending verification and completion

Browser selectors, real visible confirmations and all ten postconditions require
actual runtime checks. Baseline/variant HTTP outcomes are predictions until the
new job completes. Completion report, evidence index, final progress/risk/GQM,
viva exercise and package manifest are being assembled by this agent before any
new handoff. Existing C/group dependencies remain visible; no additional D task
is automatically assigned to Wasay merely because implementation takes work.

## First browser runtime failure and correction

The first push run 45348178607 browser job reached ten setup errors before UI
assertions: Playwright's synchronous driver kept an event loop active while
Django attempted synchronous database fixture setup. This is a harness error,
not ten product defects. The browser fixture/flows now use async Playwright;
ORM corroboration uses sync_to_async, and Django's async-safety guard remains
enabled. The original job log is preserved separately; passing retest is pending.

## Verified real HTTP regeneration result - 24 November 2026

Run 45348178607, regeneration job 138287747685 on source 8a9ca964, completed
successfully. Six strict baseline HTTP cases passed. The variant produced four
passes and exactly two genuine failed strict assertions, with pytest exit one:
`self_allocation_create:body:description:BVA:minLength-below` and
`self_allocation_create:body:attachment:BVA:x-filename-maxLength-above`.
The driver inspected exact failed IDs and zero errors/skips and recorded
experiment_demonstrated true. This is the predicted spec/server mismatch, not
an assertion that production enforces the hypothetical stricter spec.
Raw job output: docs/team/evidence/area2/phase-d/ci-45348178607-regeneration.log.
The canonical spec/data remain unchanged. This independently completes the
controlled regeneration/consumption demonstration; browser verification and
whole Area 2 acceptance remain separate.

## Second browser observation and targeted selector correction

Async Playwright repaired setup: run 45348808900 reached all ten test bodies,
but all ten timed out at the legacy login button label. Source review located
the active horilla_theme login override, whose button reads Sign In instead of
Secure Sign-in. Login now locates the credential form's actual submit control;
success assertions target the operation's specific text, not a stale login
notification. No authentication or permission bypass is introduced. The original
10-failure log is retained. Subsequent runs stop at the first unexpected browser
failure, with missing flows explicitly not counted as passes, so iteration does
not repeat the same broken setup across ten cases.

Area 2 workflow wiring now includes relevant PRs to sqe-team, preserving the
existing producer and failure exits. The complete Sonar/mutation gate is still
Wasay's architecture. Reading classic branch protection returned 403 (integration
lacks access); the accessible ruleset list was empty. That does not prove merge
or deployment protection is absent, and no enforcement claim is fabricated.

## Current Phase D verified progress

Independent checks now total 49 passing tests, including browser-report checks
that reject missing/failed/errored/skipped/extra cases and escape untrusted
failure text. Raw output is independent-tests-final.txt. The strict HTTP
regeneration demonstration is verified on run 45348178607 (six baseline passes;
variant four passes and exactly two predicted strict failures, no errors/skips).
A later async-source regeneration run 45348808900 also completed successfully;
its browser activity failed separately on the legacy login label.

Current browser retest is run 45350628323 on 476b15d6. It uses the active-theme
credential form submit control, operation-specific confirmation text, async
Playwright/ORM handling, maxfail=1 and a genuine HTML/JUnit report. At this dated
checkpoint the result is still pending. Missing flows after fail-fast are not
counted as passes. C retests remain independent populations.

The relevant-PR Area 2 and Phase D producer wiring is implemented. Classic
protection inspection returned 403; required-check/merge/deploy enforcement is
therefore not certified. This owner-only verification is distinct from the
producer/source work completed here. No new owner handoff is made while this
agent continues its browser debugging and report/evidence finalization.

## Third browser observation and own-employee binding

Run 45350628323 passed real UI login and opened the actual allocation modal.
Its first flow then timed out looking for an employee select. The normal-user
form binds employee_id as a hidden control; BaseModelForm sets it from the
request user, while the visible modal contains type/days/file/description. The
test now asserts that own-employee binding instead of attempting an admin-style
dropdown. No hidden value is changed and role restrictions are preserved. The
first flow failed and the other nine were not executed under maxfail=1; the
HTML report marks this incomplete. Another genuine retest is being run here.

## C prerequisite retest observed during D

The expanded generated-input/attachment/pagination step completed successfully
in run 45348178584 on source 8a9ca964, after the source-backed creator-FK oracle
correction. The subsequent full Area 2 producer is running. This establishes
that the earlier five attachment helper failures no longer block the expanded
step; it is not a completed 275-case/reversed pass or complete input coverage.
Exact run-level counts will be taken from retained JUnit/job logs at completion.
Wasay does not need to redo that specific test-oracle diagnosis/correction.

## Fourth browser observation: three real flows passed

Run 45351673393 on dca27fa8 verified UC-RAY-01-MAIN, A1 and A2, including visible
operation confirmation, persisted owner/count/balance and attachment bytes.
E1 then failed before submission because its test tried to select an already
disabled placeholder. The exception now leaves the required type unselected
from the initial form rather than changing disabled controls. This is a real
normal-user omission flow, not a manufactured DOM state. The remaining six
flows were not reached under fail-fast. Raw log is retained and another real
retest continues here. No D browser debugging has been assigned to Wasay.

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
