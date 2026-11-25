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

The populations overlap; count each API case once within its order. Exact selector IDs and assertions are retained in PROMPT03_REQUIREMENT_EVIDENCE.json.

---

Historical dated records follow.

# Area 2 API coverage matrix �?" Phase C checkpoint

## Prompt 1 completed — current contract checkpoint (24 November 2026)

The contract foundation is reconciled using two independent fresh runtime initializations, live production Swagger, active source/serializer/model introspection and actual role/state HTTP probes. See [Prompt 1 status](reports/RAYYAN_FINISH_01_STATUS.md) and [contract reconciliation](finish-line/CONTRACT_RECONCILIATION.md) for exact tested builds, commands and limitations.

Current canonical scope is **34 operations / 88 generated inputs / 713 IDs**; **184 IDs referenced, 529 unconsumed**, and **280 parametrized API scenarios**. All old 578 IDs survive and all old 399 unconsumed IDs have individual dispositions. The complete required-input inventory is **329 families**, including **241 outside generation**. All consumption and relational plans remain mandatory; inventory is not a pass. The old 275 first/reversed API passes belong to source 7189656a and are preserved separately.

[REMAINING_WORK.json](finish-line/REMAINING_WORK.json) assigns feasible remaining consumers to Codex for Rayyan in Prompt 2 and business-rule assertions/fixes in Prompt 3, with final verification/closure in Prompt 4. Overall release remains HOLD. Historical blocked/partial labels below describe earlier checkpoints; this section supersedes their current contract/runtime status without claiming teammate review or recovering the missing original A archive.


## Latest verified runtime - 24 November 2026

Run 45355537962 / source 32621b42 verified all 275 implemented API cases in
the full first-order collection. Separate focused/upstream/expanded/preflight
populations passed 16/8/177/1; do not sum these overlapping populations.
The reversed collection was cancelled at the 90-minute job limit, so a
completed second-order result and complete-scope acceptance remain missing.
Source 7189656a increases the job limit to 120 minutes without altering tests.
The inventory remains 179/578 generated IDs referenced and 399 unconsumed;
100% passing implemented scenarios is not full generated-input/FR coverage.
Strict owner-confirmed duplicate/terminal regressions passed without xfail.
Raw log and labelled summary: docs/team/evidence/area2/phase-c/
ci-45355537962-job.log and ci-45355537962-summary.json.

## Historical continuation - 24 November 2026

This section supersedes earlier pending-result statements below. Phase C is
**partially implemented; Hold remains in effect**. Wasay merged
[PR #2](https://github.com/includeduck/SQE-Horilla-Project/pull/2) on 23 November.
Remote `sqe-team` build is `2242c502090c81031e20df912b49809a03a1f523`;
local Git HEAD is still `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0` with preserved
uncommitted files. No local pull/reset is claimed.

[Run 45197384096](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45197384096)
completed on the merged build: **14 focused regressions passed**, **8 affected
upstream tests passed**, **41 independent tooling tests passed**, W1/W2 preflight
**1 passed**, full API collection **176 passed / 2 failed / 178 total**.
The focused collection includes four storage-only tests and repeated API tests;
these counts are separate populations and must not be added together.
Reversed execution and completeness were blocked by the old fail-fast runner.
Raw evidence: `docs/team/evidence/area2/phase-c/ci-45197384096-job.log`.

The two genuine remaining failures are
`STATE-LEAVE-cancelled-reject` (expected 400, observed 200) and
`GAP-ALLOCATION-DUPLICATE-001` (proposed 400, observed 200 plus another row).
Their business-rule oracles remain unresolved; neither assertion was weakened.
Requester refund, foreign-owner allocation PUT/DELETE, capped carry-forward and
extensionless attachment corrections now have actual passing-after evidence.

This continuation adds **97 executable API cases**: 73 generated self-service
update body cases, 15 additional attachment classes/boundaries, and nine further
pagination classes/minimum boundaries. Inventory is now **275 unique API cases**,
referencing **179/578 generated IDs**, with **399 unconsumed IDs** explicitly
listed in `tests/team/api/case_ledger.json`. New cases are pending runtime
verification; the 176/178 result belongs to the older merged build only.
Spec/data fingerprints are unchanged. Dynamic record IDs are bound after real
HTTP creation; update tests assert identity/count preservation and unchanged
balances on rejection. Files use real multipart bytes; null/omission/invalid
file JSON bindings are recorded. Pagination expectations explicitly model DRF's
fallback/clamp rather than pretending every schema-invalid query is rejected.

The producer now attempts the independent reversed API pass and completeness
check after an API collection failure, preserving the first nonzero exit.
Prerequisite/preflight failures still block dependent execution. Zero child exit
cannot hide missing/malformed/empty/failed/errored/skipped JUnit. New subprocess
regressions exercise these cases. Disposable test settings use Django's fast
MD5 test hasher for synthetic users, retaining password verification/JWT over
HTTP; this is no production hashing or password-security claim.

Local dependency installation was retried on 24 November and failed to resolve
pytest; Django/pytest remain absent and Docker's Linux engine is unavailable.
No local HTTP pass is claimed. The complete free remote runtime remains the
verification route. See the final continuation evidence below for this build's
actual checks/publication and any new runtime outcome.

Owner: Syed Muhammad Rayyan Hassan, **24I-3000**. Date: 23 November 2026.

**Implementation inventory is not an execution result.** Current source has 178 distinct API cases. Real remote runs are tracked by build/run in the C status report. No case is marked passed merely because its source or ID exists.

## Current inventory and traceability - 24 November 2026

| Executable family | Unique cases | Main FR/BR links | Runtime state of expansion |
|---|---:|---|---|
| Generated self-create/update scalar/date/enum/reference bodies | 144 | FR-01, FR-04, FR-05, FR-06, FR-07; BR-01/02 | 73 update cases newly implemented, pending |
| Original generated multipart slice | 5 | FR-01, FR-10 | Passed on merged historical build |
| Additional generated attachment classes | 15 | FR-01, FR-05; BR-02 | Newly implemented, pending |
| Generated page-size default/fallback/minimum/cap | 12 | FR-01, FR-10 | Nine additional cases pending |
| Generated missing-reference operations | 3 | FR-02, FR-08; BR-04 | Historical build evidence retained |
| Feasible BR-02 combinations | 24 | FR-05, FR-07; BR-02 | Historical build evidence retained |
| BR-04 authorization combinations | 8 | FR-08; BR-04 | Historical build evidence retained |
| State and actor transitions | 50 | FR-02/03/04/08/09; BR-03/04 | One unresolved historical failure |
| Connected workflows/regressions/repetition | 11 | FR-01 through FR-10, as scenario assertions apply | One unresolved duplicate historical failure |
| Missing/invalid JWT and non-owner generic read | 3 | BR-04 | Historical build evidence retained |
| **Total** | **275** | Counts each executable case once | New complete build pending |

Generated-ID implementation reference rate is **179/578 (30.97%)**, not a
runtime pass rate or an assertion that 30.97% of requirements are verified.
399 unconsumed IDs remain explicit in the ledger. FR-to-family links above are
traceability targets: acceptance requires reviewing actual assertions/results
against each requirement, including all applicable rejection/decision/role
criteria. Current accepted FR numerator remains undetermined, denominator ten.
The complete 32-row BR-02 table still has eight explicitly infeasible rows.
No skipped test is counted as tested. The following pre-continuation inventory
is retained as history and does not replace the current 275-case inventory.

## Historical 23 November denominators

| Criterion | Inventory / planned consumption | Verified execution |
|---|---|---|
| Scoped OpenAPI methods | 27 operations / 16 paths | Source AST checked; runtime outcomes must be read from current-build JUnit |
| Generated inputs | 578 data cases (488 EP / 90 BVA), 71 operation/input entries | Data generation/freshness independently verified; not an API pass count |
| Distinct generated IDs referenced by executable API cases | 82 / 578 | Refer to run-specific results; remaining 496 labels are listed in case_ledger.json |
| Executable API cases | 178 total, each counted once | Remote current-build results pending final status; local invocation blocked at missing pytest |
| BR-02 combinations | Full 32-row table; 24 executable, 8 explicitly infeasible | No skipped cases count as coverage; outcomes require actual HTTP execution |
| BR-04 ownership/permission/manager combinations | 8 / 8 vectors implemented | Actual outcomes in JUnit, never inferred from truth-table bookkeeping tests |
| State/role transitions | 50 catalog cases across 3 allocation and 5 leave states | Includes role-conditioned self-approval refusals; not a claim that a nonexistent allocation action has been tested |
| User roles | Employee, distinct approver, distinct outsider; admin setup only | Non-superuser assertions and independent balances are enforced by fixtures |
| Functional requirements | FR-01 through FR-10 remain traceability targets | Verified requirement coverage is pending result-to-assertion review, not test pass rate |

## Executable case inventory

| Family | Number | Source / stable identity |
|---|---:|---|
| Self-create scalar/date/enum/required/reference EP/BVA | 71 | `test_generated_inputs.py`; generated IDs, with two B IDs excluded to avoid duplicate accounting |
| Original multipart consumer | 5 | `test_generated_slice.py`; two numeric EP plus three filename BVA IDs |
| Generated page-size clamp | 3 | `test_queries_and_auth.py`; generated x-clamp-maximum IDs |
| Generated missing-reference paths | 3 | Same file; allocation_detail / leave_detail / approve missing-record IDs |
| BR-02 feasible combinations | 24 | `DEC-BR02-*` |
| BR-04 truth table | 8 | `AUTH-BR04-*` |
| Allocation/leave state and actor transitions | 50 | `STATE-ALLOC-*`, `STATE-LEAVE-*` |
| Shared W1/W2, cancellation, repetition and candidate regressions | 11 | `test_workflows.py`; IDs in case_ledger.json |
| Missing/invalid JWT and generic non-owner read | 3 | `AUTH-TOKEN-*`, `AUTH-NONOWNER-GENERIC-DETAIL` |
| **Total** | **178** | Each ID unique within API inventory |

## Binding and input accounting

- Normal create tests consume generated values and otherwise valid generated baselines. Native JSON intentionally omits the optional binary upload and records a bound-request hash. Binary boundary tests remain real multipart requests. The complete OpenAPI media/normalization contract still needs reconciliation.
- Falsy end-date values are normalized to start date by the actual POST handler; this wire-level oracle is recorded separately from the raw DateField schema predicate.
- File-name boundary is source-derived 100 characters and introspected by the fixture before use. No maximum file-byte count, arbitrary allocation maximum or universal half-day numeric increment is invented.
- Page-size limit is a clamp: 99/100/101 normalize to 99/100/100. Below-minimum/null/invalid pagination fallback semantics still need full generated consumption.
- Case/setup IDs are correlated from actual fixture records and HTTP creation readback. Unsupported or unbound dimensions remain explicit; path/query/action/update/generic body coverage is not certified from self-create coverage alone.
- Every targeted success/rejection includes state/balance/count readback. Refund regressions deliberately distinguish requester balance 5�+'2 from approver balance 7 and outsider balance 9.

## Decisions and state oracles

BR-02 conditions are assigned type, ordered dates, matching same-day breakdown, required attachment present, and no row satisfying the endpoint's overlap predicate. Reversed dates cannot simultaneously be a same-day mismatch: eight rows are retained as infeasible. A spanning existing record can satisfy the endpoint's overlap query even for reversed target dates; the table describes that source predicate explicitly.

BR-04 expects `not owner AND (permission OR reporting manager)`. All eight combinations are independent normal-user fixtures, including a self-manager/self-permission case that must still be denied.

The state catalog exercises requested/approved/rejected allocation and requested/approved/rejected/cancel_requested/cancelled leave. Requested allocation has no forbidden command among its four legitimate manager/owner operations, so its refusal example is explicitly actor-conditioned self-approval, not fictional pure-state coverage. Cancellation refusal after a decision also checks the persistent one-attempt flag. Approved allocation reversal and terminal cancelled-leave rejection remain documented source/draft-oracle questions. No fixture row is silently called team-approved.

## Requirements and remaining mandatory work

| Requirement | Implemented contribution | Remaining mandatory completion, assigned to Wasay/his agent in handoff.md |
|---|---|---|
| R3�?"R5 / every input and generated consumption | Reproducible EP/BVA generator, self-create/file/page/reference consumers and provenance | Consume remaining generated labels and missing filters/page/reason/dynamic-balance/media inputs, with accurate normalization expectations |
| R6 / decisions and transitions | 32-row BR-02 table, eight BR-04 rows, 50 state/actor cases | Reconcile unresolved graph/duplicate semantics and complete every remaining multi-condition business rule matrix |
| R7 / rejection/repetition/shared record | W1 allocation five �+' leave three �+' balance two; independent over-balance rejection; state/replay/readback regressions | Execute/retest clean twice, resolve genuine product failures and retain real evidence |
| R8/R13 / findings and root causes | Structured source candidates and precise HTTP reproducers in AREA2_DEFECTS.md | Attach actual failure/fix/retest evidence, Issues/RCA/Pareto/fixed and blocked PRs |
| R11 / CI producer | Fail-propagating runner and isolated remote verification workflow | Wasay's complete every-PR Sonar/all-tests/mutation gate, required checks and merge/deploy enforcement |
| R12�?"R14/R16 / records and contribution | Actual logs, status/management/disclosure, verified Rayyan commits and delivered owner issue | Complete actual-result reporting/GQM/risk acceptance and personal viva obligations without fabricated authorship |

## Current fingerprints

- Spec canonical SHA-256: `45e37bfbcd255fc567d5923b13076637f8777bbc4c48bb239f6c2e3fe398f0db`.
- Logical bindings SHA-256: `25b0b2a165dd1c31cf9ad9cdb0b317f1de106560b399cc9098e241a5875be4a0`.
- Generated data SHA-256: `38d69c57a2e33ede9682bb8b6b165d7c1398b578711983ecf05cd3f8e59e3521`.

`api/case_ledger.json` retains every unconsumed generated ID and infeasible decision row. `coverage_complete` remains **false**. The older B evidence refers to its earlier 518-case contract/build; do not conflate its hashes or test totals with this expanded C snapshot.

## C prerequisite retest observed during D

The expanded generated-input/attachment/pagination step completed successfully
in run 45348178584 on source 8a9ca964, after the source-backed creator-FK oracle
correction. The subsequent full Area 2 producer is running. This establishes
that the earlier five attachment helper failures no longer block the expanded
step; it is not a completed 275-case/reversed pass or complete input coverage.
Exact run-level counts will be taken from retained JUnit/job logs at completion.
Wasay does not need to redo that specific test-oracle diagnosis/correction.

## D prerequisite corrections and current owner decisions

The published SCOPE OD-01/OD-02 already require HTTP 400 for rejecting cancelled
leave and for identical pending employee/type/days/description allocations.
Source 32621b42 implements both narrow fixes without xfail. The existing
duplicate case additionally checks the generic route, distinct inputs and
approved history, retaining one unique scenario ID; total API count stays 275.
Focused CI now runs 16 rather than 14 cases. The historical four-defect result
population remains separate; the focused strict regression step passed in
run 45355537962, while full/reversed verification remains pending. Source-backed
expanded attachment creator correction has already passed its 177-case step.
