# Rayyan finish 03: business rules and strict defect corrections

25 November 2026. Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B.

## Current evidence and corrective checkpoint

The complete strict business baseline on f41dc58b (run 45544239475) executed
354 cases across four shards: **315 passed / 39 failed / zero setup errors or
required skips**. Of the failures, 27 demonstrated six distinct product defects;
12 were this agent's incorrect assumption that Django TextField.clean installs
a max-length validator. Actual >255-character SQLite persistence was already
observed successfully before that mistaken final harness assertion. The test
now asserts the actual clean behavior and keeps the helper's independent 1000
limit, declared 255 metadata and untested PostgreSQL behavior distinct.

An expanded-baseline full-suite shard on a021dec5 (45544984779 / 138972520699)
completed with 211 passes and four failures, including actual unauthorized
ownership transfer: HTTP 201 with Team Outsider persisted instead of controlled
403. It establishes a seventh distinct product defect. The superseded whole
run was then intentionally cancelled to release free CI capacity, retaining its
completed failures/artifacts; it is not a completed collection or passing gate.
The dedicated expanded baseline remains independently retained.

The seven narrow source corrections address nonpositive duration, target-specific
holidays, existing model forecast entitlement, complementary half-day overlap,
approval's current policy/cap recheck, body validation before allocation balance
mutation, and authorization of a changed update target. Product Issues #14-#20
retain exact before inputs/results/balances and source/run identities. Source
corrections remain proposed until their strict passing-after checks finish.

All 713 canonical IDs and their actual request payloads are preserved. The five
coarse unimplemented-reader flags have explicit implementation resolutions in
PROMPT03_EXCLUSION_RECONCILIATION.json; no case or mandatory family was removed.
Schema closure metadata changes the spec/data fingerprints to a7fb5df7/c8714857.
Declared reader completeness does not establish a pass: actual source-bound
JUnit for all 3,433 cases, both independent orders, every input family and every
FR/BR assertion selector still drives the strict gates. All 64 independent
tooling checks pass locally; generator freshness and all mapping partitions pass.

Original defects #3-#6 were updated and closed using their merged PR #2 fixes
and actual later 16-case focused plus eight-case upstream passing evidence on
796b84bd; those populations remain separate. New fixes in PR #8 are not called
merged or owner accepted. Final integrated acceptance is still Prompt 4 work.

## Earlier implementation checkpoints

Execution is in progress. This checkpoint adds 164 effective-duration, holiday,
breakdown, balance, forecast, expiry, overlap, assignment and attachment contexts
over all four generic/self create/update operations; 72 reason/persistence
contexts; the remaining 21 canonical generated reason/date-order cases; three
current-policy approval checks and an approved-allocation refusal atomicity
regression. Existing decision/state/integration tests remain strict.

The four-shard real HTTP workflow retains source-bound JUnit and complete
request/pre-state/post-state observations. This is a baseline reproduction
checkpoint; no passing runtime result or new product fix is claimed yet.
Local sources compile. Current local Django/pytest dependencies are absent;
the existing isolated GitHub Actions runtime remains the verification route.

The conflict with sqe-team was confined to AI_USE_RECORD.md. Merge f41dc58b
preserves all published teammate Sonar/unit files and both members' disclosures.
Its first real baseline is run 45544239475, four independent business shards.
The two Prompt 2 harness corrections retain exact ownership and selection
assertions: detail responses use object identity, and the self-list filter's
nonmatching type is bound to a distinct valid second request rather than an
invalid form choice that the source ignores.

Additional implemented contexts cover all 124 decision/state/role combinations,
two target-reference transfer denials and two split available/carry-forward
W1/W2 refund sequences. New Prompt 3 inventory: 389 distinct cases; total 3,433
API cases, all 713 canonical IDs mapped, 2,256 supplementary wire cases.
The optional cancellation-request reason is one source-discovered supplementary
input, making 350 mandatory input families (334 prior-stage and 16 business/
reason families). This is implementation accounting, not passing execution.

Refreshed Prompt 2 evidence: source 796b84bd, run 45455049960, completed with two
failures in EACH 3,044-case order: self detail authentication response parsing
and self leave-type nonmatching fixture binding. All remaining cases passed.
These two harness/oracle contexts are being repaired here; failures are retained.
Validation/upstream run 45455050118 and browser/regeneration run 45455049919
completed successfully. Exact job populations will be reconciled from real logs.

OD-01/OD-02 and seven established corrections are retained. No xfail, required
skip, forced exit, concurrent duplicate feature or new database uniqueness
policy is introduced. Prompt 4 is not executed by this checkpoint.
