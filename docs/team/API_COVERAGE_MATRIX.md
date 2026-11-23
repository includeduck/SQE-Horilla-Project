# Area 2 API coverage matrix — Phase C checkpoint

Owner: Syed Muhammad Rayyan Hassan, **24I-3000**. Date: 23 November 2026.

**Implementation inventory is not an execution result.** Current source has 178 distinct API cases. Real remote runs are tracked by build/run in the C status report. No case is marked passed merely because its source or ID exists.

## Denominators

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
- Every targeted success/rejection includes state/balance/count readback. Refund regressions deliberately distinguish requester balance 5→2 from approver balance 7 and outsider balance 9.

## Decisions and state oracles

BR-02 conditions are assigned type, ordered dates, matching same-day breakdown, required attachment present, and no row satisfying the endpoint's overlap predicate. Reversed dates cannot simultaneously be a same-day mismatch: eight rows are retained as infeasible. A spanning existing record can satisfy the endpoint's overlap query even for reversed target dates; the table describes that source predicate explicitly.

BR-04 expects `not owner AND (permission OR reporting manager)`. All eight combinations are independent normal-user fixtures, including a self-manager/self-permission case that must still be denied.

The state catalog exercises requested/approved/rejected allocation and requested/approved/rejected/cancel_requested/cancelled leave. Requested allocation has no forbidden command among its four legitimate manager/owner operations, so its refusal example is explicitly actor-conditioned self-approval, not fictional pure-state coverage. Cancellation refusal after a decision also checks the persistent one-attempt flag. Approved allocation reversal and terminal cancelled-leave rejection remain documented source/draft-oracle questions. No fixture row is silently called team-approved.

## Requirements and remaining mandatory work

| Requirement | Implemented contribution | Remaining mandatory completion, assigned to Wasay/his agent in handoff.md |
|---|---|---|
| R3–R5 / every input and generated consumption | Reproducible EP/BVA generator, self-create/file/page/reference consumers and provenance | Consume remaining generated labels and missing filters/page/reason/dynamic-balance/media inputs, with accurate normalization expectations |
| R6 / decisions and transitions | 32-row BR-02 table, eight BR-04 rows, 50 state/actor cases | Reconcile unresolved graph/duplicate semantics and complete every remaining multi-condition business rule matrix |
| R7 / rejection/repetition/shared record | W1 allocation five → leave three → balance two; independent over-balance rejection; state/replay/readback regressions | Execute/retest clean twice, resolve genuine product failures and retain real evidence |
| R8/R13 / findings and root causes | Structured source candidates and precise HTTP reproducers in AREA2_DEFECTS.md | Attach actual failure/fix/retest evidence, Issues/RCA/Pareto/fixed and blocked PRs |
| R11 / CI producer | Fail-propagating runner and isolated remote verification workflow | Wasay's complete every-PR Sonar/all-tests/mutation gate, required checks and merge/deploy enforcement |
| R12–R14/R16 / records and contribution | Actual logs, status/management/disclosure, verified Rayyan commits and delivered owner issue | Complete actual-result reporting/GQM/risk acceptance and personal viva obligations without fabricated authorship |

## Current fingerprints

- Spec canonical SHA-256: `45e37bfbcd255fc567d5923b13076637f8777bbc4c48bb239f6c2e3fe398f0db`.
- Logical bindings SHA-256: `25b0b2a165dd1c31cf9ad9cdb0b317f1de106560b399cc9098e234a5875be4a0`.
- Generated data SHA-256: `38d69c57a2e33ede9682bb8b6b165d7c1398b578711983ecf05cd3f8e59e3521`.

`api/case_ledger.json` retains every unconsumed generated ID and infeasible decision row. `coverage_complete` remains **false**. The older B evidence refers to its earlier 518-case contract/build; do not conflate its hashes or test totals with this expanded C snapshot.
