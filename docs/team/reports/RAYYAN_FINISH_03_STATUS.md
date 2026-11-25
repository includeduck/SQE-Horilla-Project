# Rayyan finish 03 — verified business rules and strict defect corrections

25 November 2026. Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B.

**Prompt 3 technical status: COMPLETE on the recorded source.**
No failed, missing, errored or skipped required API assertion remains in either
complete order. Prompt 4 has not been executed. Whole-project release remains
HOLD for accepted integration, shared gates and final package/ownership closeout.

## Actual source and final results

Application/test source: `fecac354c9b5d8ea47ac732a2b089ed3cc148620`.
Actual tested PR merge: `7c07376fa19a092cd445737ef817681413ae1e4b`,
against `sqe-team` base `0a5ac6443dadb50ab5fd6ea749f41dd108a19486`.
The final publication adds reports and the independently tested read-only
evidence helper. It does not claim new application behavior or a passing
check for an unobserved documentation commit.

| Separate population | Actual result | Run |
|---|---|---|
| Full API, first order | 3,433 passed; zero failures/errors/skips/missing IDs | [45609322121](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322121) |
| Full API, reversed order | 3,433 passed; zero failures/errors/skips/missing IDs | Same run, independent 16 shards |
| Strict complete-scope guard | Both orders accepted; overall Area 2 job passed | Same run, coverage job 139222175260 |
| Generated IDs / former gap / input families | 713/713; 399/399; 350/350 verified | Same source-bound JUnit reconciliation |
| Business/state/role/workflow | 482 passed in four shards: 124 / 125 / 103 / 130 | [45609322065](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322065) |
| Affected business upstream / original team units | 82 passed / 24 passed, separately | Same business run |
| Focused / focused upstream / expanded | 16 / 8 / 182 passed, separately | Full API run, job 139188710703 |
| Wire validation / advanced filters | 238 / 7 passed, separately | [45609321905](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609321905) |
| Further affected upstream | 27 passed plus two subtests | Same validation run |
| Personal browser flows | All ten passed; strict HTML report passed | [45609321873](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609321873) |
| Controlled regeneration | Six baseline passes; variant four passes and exactly two predicted strict failures; experiment succeeded | Same Phase D run |
| Two independent fresh foundations | Each passed one W1/W2 foundation plus five smoke cases | [45609321841](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609321841) |
| Schema / freshness / tooling / media reader | Passed / passed / 68 passed / four passed | [45609322104](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322104) |

These overlapping populations are never added into a larger unique-case count.
The scoped implementation is 34 operations, 88 canonical generated input entries,
713 canonical IDs, 2,256 supplementary wire cases and 3,433 unique API scenarios.
The 350 mandatory families comprise 334 input/media/query/filter families and
16 business/reason families. A collected/mapped ID alone was never called a pass.

Derived complete coverage and generated/case execution ledgers
are retained in [artifact 15024156843](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322121/artifacts/15024156843)
Original JUnit and raw HTTP/state logs remain in the 32 shard artifacts and
separate business artifacts indexed in PROMPT03_VERIFICATION.json.
The repository copies the actual execution summary, requirement evidence,
input ledger and reconciled remaining work. Evidence reader run
[45625562265](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45625562265) independently verified source
identity and reconstructed all five original report files without altering them.

## FR/BR assertion evidence

| Requirement | Required asserted cases per order | Result |
|---|---:|---|
| FR-01 | 76 | Verified in both orders |
| FR-02 | 29 | Verified in both orders |
| FR-03 | 47 | Verified in both orders |
| FR-04 | 9 | Verified in both orders |
| FR-05 | 424 | Verified in both orders |
| FR-06 | 171 | Verified in both orders |
| FR-07 | 57 | Verified in both orders |
| FR-08 | 286 | Verified in both orders |
| FR-09 | 191 | Verified in both orders |
| FR-10 | 347 | Verified in both orders |
| BR-01 | 171 | Verified in both orders |
| BR-02 | 188 | Verified in both orders |
| BR-03 | 270 | Verified in both orders |
| BR-04 | 340 | Verified in both orders |

Exact case IDs, consumer files, required assertions, source/spec identity and
the empty failed/missing lists are retained in PROMPT03_REQUIREMENT_EVIDENCE.json.
This verifies the selected assertions on the recorded source, not human scope
signoff or an exhaustive Cartesian product of every possible application state.

## Delivered behavior, source changes and retained failures

The 389 new business-file cases include 164 duration/holiday/breakdown/balance/
reference/attachment contexts, 72 reason/persistence cases, 124 state/role cases,
21 remaining canonical reason/date-order cases, three current-policy approvals,
one malformed-approved-allocation atomicity case, two target-transfer denials
and two connected available/carry split-refund sequences. Existing decision,
state, auth, reference and W1/W2 assertions remain active.

Seven genuine business defects were corrected in
`e4d6f3ce5e0f57ce9e20667096bf30a58a2b50e2`: nonpositive effective duration,
missing target-specific holiday context, missing existing forecast entitlement,
complementary half-day overlap, current approval carry policy/cap, body validation
before allocation reversal, and changed-target authorization. The target guard's
write-only follow-up is `83666052c12d483b01d3f373fdf665b32b9f48ab`.

Failing-before business source f41dc58b / run 45544239475 executed 354 cases:
315 passed and 39 failed; 27 failures represented six product defects and
twelve represented this agent's incorrect TextField.clean length assumption.
The complete decoded logs and exact HTTP/pre/post observations remain under
evidence/area2/finish-03/. A later completed shard of run 45544984779 on a021dec5
had 211 passes and four failures, including unauthorized persisted ownership
transfer; the overall run was subsequently cancelled and is not called complete.

The retained 13200cd9 full baseline, run 45549984738, executed all 3,433 cases in
each order with the SAME two date-order field-error failures per order.
It verified 711 generated IDs and 348 families; all former 399 missing IDs
already passed. The positive-duration check had intercepted the established
end_date error. Follow-up `4a719a178941f1a935c4acf29ad7170dc0005dac` restores
early inverted-date refusal; the strict generated tests remain unchanged.
The subsequent complete passing run above is the actual retest. This is a
regression within A2-P3-01, not an additional Pareto defect.

Prompt 2's object-versus-page and valid nonmatching self-list fixture repairs
retain the same exact ownership/selection assertions. Reason tests explicitly
distinguish helper strip/truncation at 1000 from LeaveRequest TextField's declared
255 and observed longer SQLite persistence/clean behavior; no PostgreSQL claim
or new mandatory-reason policy is invented. Expiry runs the existing lifecycle;
forecast permits submission at the existing reset boundary without early credit
at approval. OD-01/OD-02 and the seven established corrections are preserved.
No new allocation positivity, concurrent duplicate or database uniqueness feature
was introduced. No required xfail, skip, relaxed assertion or forced success exit
was used. Removing the stale original-team strict xfail retained its 400 assertion.

## Defects, management and publication

The current population is 22 distinct confirmed Area 2 product defects across
dated builds: seven established, eight Prompt 2 and seven Prompt 3. Behavior-to-
Issue/actual-fix mapping is in PROMPT03_DEFECT_POPULATION.json. Missing historical
D04/D05/D10 product records are now Issues #29/#30/#31 under rayyanhasan899.
Issues #3–#6 remain warranted merged/retested closures; the other eighteen
remain open pending accepted review/merge of draft PR #8. Area 1 Issues #11–#13,
coordination #1, harness mistakes and extra failing parametrizations are excluded.

Updated records include AREA2_DEFECTS, two-major-defect 5 Whys/cause controls and
the 22-defect Pareto (retaining historical four/seven snapshots), SCOPE/test basis,
risk/GQM/criteria, coverage/requirement matrix, evidence/AI records, prior-stage
carryover status, Communication and handoff. FR evidence is 10/10 and BR evidence
4/4 on this source. Human effort/estimate variance, density without measured size,
human triage/review/viva and unobserved reopen history are not fabricated.

The local workspace became unavailable; its files were preserved. Connected
GitHub publication and free isolated Actions supplied execution. The read-only
report helper initially failed a redirected-download authentication check;
cd028cb9 fixed the helper, and both five-reader reconciliation runs passed.
This is disclosed harness repair, not another product defect.

## Exact final-stage and external carryover

All 350 input-family rows are verified on the recorded source. Prompt 4 must
perform final integrated verification on the final history; reconcile final
reports/criteria, static inventory/package manifests and genuine available
all-area artifacts; finish feasible carryover; then publish the definitive
ownership closeout. It is not executed here and no fifth prompt is expected.

Wasay/agent retains actual owner review and protected integration of PR #8,
overall Sonar/unit/mutation/required merge/deployment administration and authentic
Area 1/3/group-package inputs with Zain. Reconnecting/synchronizing the laptop
must preserve existing working files. These are precise dependencies, not a
transfer of completed routine debugging. No teammate acceptance or final
no-further-execution statement is asserted prematurely.
