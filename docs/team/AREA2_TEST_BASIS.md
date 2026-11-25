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

---

Historical dated records and implementation detail follow.

## Prompt 3 reconciled behavior — 25 November 2026

This section supersedes the historical incomplete-reader and unanswered
OD-01/OD-02 labels below. The canonical scope has 34 operations, 88 generated
input entries and 713 preserved IDs. The broader inventory has 350 mandatory
families (334 input/media/filter/query families and 16 business/reason families).
The implementation has 3,433 unique API cases including 2,256 supplementary wire
cases; these numbers measure implementation until actual source-bound JUnit
and requirement assertion selectors establish a pass.

Effective duration uses independent expected calendar/half-day calculations,
holiday and company-day sets with overlap removed once, and the target
employee's specific-holiday context. Positive effective duration applies to
leave requests. No positive allocation-amount policy is invented. Available
funds use existing carry-forward policy/cap and model forecast at its reset
boundary; approval rechecks current funds and does not credit future entitlement
early. Expiry tests explicitly run the existing expire_carryforward lifecycle
before checking validation, rather than inventing expiry by requested date.

All nine same-day breakdown pairs, active versus terminal/foreign overlap,
conditional attachment bytes, assignment, requested-only editing/deletion,
invalid action IDs, permitted manager/permission roles, self/nonowner denials,
repetition and connected grant/consume/refuse/refund are exercised. BR-02 keeps
24 feasible and eight evidenced infeasible combinations; BR-04 keeps all eight
permission/manager/self truth rows. Additional state/role cases exercise the
existing graph under four distinct actor modes. W1/W2 readback independently
corroborates persisted owner/status and exact available/carry debit/refund splits.

Reasons follow reject_reason_from: omission/null/nonstring become empty,
strings are stripped and capped at 1000, with actual persistence asserted.
The LeaveRequest TextField's declared max_length=255 is separate: the tested
SQLite persistence and explicit TextField.clean accept the tested longer text.
The helper limit is not a serializer rejection bound, and this work makes no
PostgreSQL claim. Optional cancel reasons are a source-discovered supplementary
family. An incompatible future mandatory-reason policy would require an owner
decision; it is not silently imposed here.

A response alone is never the workflow oracle. Current evidence and precise
per-FR/BR assertions are in finish-line/PROMPT03_REQUIREMENT_EVIDENCE.json,
finish-line/PROMPT03_INPUT_LEDGER.json and reports/RAYYAN_FINISH_03_STATUS.md.
No human approval, whole-project release or final Prompt 4 execution is inferred.

---

Historical dated records follow. Current source-specific results above supersede their older pending/count labels.

# Area 2 test basis: Phase B prerequisite reconstruction

## Prompt 1 completed — current contract checkpoint (24 November 2026)

The contract foundation is reconciled using two independent fresh runtime initializations, live production Swagger, active source/serializer/model introspection and actual role/state HTTP probes. See [Prompt 1 status](reports/RAYYAN_FINISH_01_STATUS.md) and [contract reconciliation](finish-line/CONTRACT_RECONCILIATION.md) for exact tested builds, commands and limitations.

Current canonical scope is **34 operations / 88 generated inputs / 713 IDs**; **184 IDs referenced, 529 unconsumed**, and **280 parametrized API scenarios**. All old 578 IDs survive and all old 399 unconsumed IDs have individual dispositions. The complete required-input inventory is **329 families**, including **241 outside generation**. All consumption and relational plans remain mandatory; inventory is not a pass. The old 275 first/reversed API passes belong to source 7189656a and are preserved separately.

[REMAINING_WORK.json](finish-line/REMAINING_WORK.json) assigns feasible remaining consumers to Codex for Rayyan in Prompt 2 and business-rule assertions/fixes in Prompt 3, with final verification/closure in Prompt 4. Overall release remains HOLD. Historical blocked/partial labels below describe earlier checkpoints; this section supersedes their current contract/runtime status without claiming teammate review or recovering the missing original A archive.


## Current continuation - 24 November 2026

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

Owner: Syed Muhammad Rayyan Hassan, **24I-3000**, `rayyanhasan899`. Date: 23 November 2026.

## Authority and status

The official SQE brief, page 2, requires generated EP and three-point BVA inputs consumed by API tests, with shared-record readback. `TEAM.md` assigns Area 2 to Rayyan. `SCOPE.md` supplies FR-01–FR-10 and BR-01–BR-04, but explicitly remains a draft. Wasay retains Area 1/CI and Zain Area 3 coordination.

The previous Phase A archive and its live-tested contract are unavailable in this checkout. This document and `tests/team/generator/openapi.json` reconstruct only the foundation needed to continue independent B work. They do not recover or certify Phase A, finalize all its business oracles, or reproduce its historical test evidence. See `reports/SQE_IMPLEMENTATION_PHASE_A_STATUS.md` and `Communication.md`.

OpenAPI **3.0.3 JSON** is used rather than YAML because JSON requires no new dependency for independent generation. Do not create a competing YAML copy. This is a scoped source contract, not an export of the application's Swagger 2.0 output. Formal OpenAPI validation and comparison with live Swagger remain blocked by missing runtime packages.

## Verified source relationships

| Fact / decision | Evidence | Consequence |
|---|---|---|
| Versioned API and legacy alias both exist | `horilla_api/apps.py`, `HorillaApiConfig.ready` | New test routes use `/api/v1/`; legacy routes remain untouched. |
| Selected routes and inherited handlers exist | `horilla_api/api_urls/leave/urls.py`; `api_views/leave/views.py` | AST regression checks all 27 selected operation/method pairs, including inherited cancellation handlers. This is static evidence, not URL resolver execution. |
| Allocation create amount is a required FloatField without numeric limits | `api_serializers/leave/serializers.py`, `LeaveAllocationRequestCreateSerializer`; `leave/models.py:2452` | Generate finite numeric, negative/zero/positive, omission/null/type classes. No invented positive minimum or maximum of ten. Intended amount policy remains a C triage question. |
| Allocation PUT uses a different model serializer | `LeaveAllocationRequestSerilaizer`; generic/self allocation PUT views | Its amount is optional/nullable; preserve this difference from creation. |
| Description is required unbounded text | `leave/models.py:1403`, `2462`; serializer field lists | Use minimum nonblank length one after DRF trimming; no artificial maximum. Runtime introspection still pending. |
| Attachment is an optional nullable FileField | `leave/models.py:1404`, `2456`; create serializers | A filename maximum of 100 is inferred from inherited Django/DRF defaults, explicitly pending runtime introspection. File content must be nonempty under DRF defaults. The fixture asserts both defaults before HTTP execution. No invented file-byte limit. |
| Breakdown enum has three values | `leave/models.py`, `BREAKDOWN`, `LeaveRequest` date breakdowns | Enumerate full day / first half / second half, invalid enum, null and omission; no arbitrary numeric BVA on an enum. |
| Relative date order is a real limit | `leave_Validations` checks `start_date <= end_date`; `LeaveRequest.clean` | `x-date-order` reads names from the spec and uses the bound start date to generate end-date −1/0/+1 calendar days. |
| Employee create/update fills missing/null end date from start date | employee and generic leave POST/PUT handlers | End date remains optional/nullable at the wire level; this does not exempt other required fields or date validity. |
| Self allocation creation returns 200 with no object body | `EmployeeLeaveAllocationGetCreateAPIView.post` | HTTP consumer obtains new IDs from the employee's own list, then reads the detail. Generic allocation create returns 201. |
| Audit creator points to a user | `horilla/models.py:119` and `HorillaModel.save` | Corroborate `created_by_id` against the synthetic HorillaUser ID, never Employee ID. These IDs need not match. |
| Rejection reason is normalized rather than schema-rejected | `api_methods/base/methods.py`, `reject_reason_from` | Reason/body generation is explicitly incomplete. Do not falsely specify a hard HTTP rejection limit of 1000 or silently resolve the 255-character model discrepancy. |
| Page size is capped, not an input-rejection bound | `api_methods/base/pagination.py`, `HorillaPageNumberPagination.max_page_size` | Do not encode `page_size <= 100` as a rejection oracle. Query/filter/grouping behavior remains unreviewed. |

Paths in this table starting with `api_` are relative to `horilla_api/`.

## Bindings and expectations

`bindings.json` contains reproducible synthetic placeholders, never real database IDs or credentials. The HTTP fixture replaces employee/type IDs using the freshly seeded disposable DB, writes a runtime JSON artifact, reads it, and verifies its freshness before consumption. Other placeholder IDs remain unbound because this slice never executes those cases.

Each case has a baseline, exactly one mutated body/path/query dimension, required/nullable predicates, source constraint, FR/BR IDs, technique/class and value/omission. BVA adds unit, step, limit and inclusivity. `expected.oracle` separates schema predicates, missing-record expectations and date-order predicates. A schema-valid request is **not** automatically valid under balance, date-breakdown, ownership, overlap or state rules. The full artifact is not an automatic HTTP execution list.

References resolve locally; missing/external/cyclic references and unsupported relevant constraints fail visibly. Required null differs from missing; negative length/cardinality has no representable wire input and is recorded as N/A. Finite unbounded allocation numbers have EP but no invented numeric BVA. Bounded fractional numbers require an explicit justified `x-step`; no general half-day step is assumed from FloatField alone.

## Remaining oracle and coverage decisions

BR-01 effective duration, capped carry-forward and forecast; BR-02 breakdown matching, assignment, overlap and conditional attachment; BR-03 the complete state graph, allocation reversal and repeat behavior; and BR-04 all ownership/permission paths still need the full A/C scenario basis and runtime verification. Date-order generation covers only one BR-02 condition. In particular, restoring balance on rejection must affect the requester, not the acting approver; the audit's candidate defect remains unexecuted and unmodified.

`openapi.json` contains eight explicit exclusions, copied into every generated artifact with `coverage_complete: false`. Unknown relevant constraints cause failure rather than a complete-coverage claim. Query/filter, rejection normalization and dynamic effective-balance boundaries must be reconciled before all-input coverage can be accepted.
## Phase C supplement — 23 November 2026

The earlier sections describe the Phase B baseline. Phase C now exercises
generated self-create body inputs, pagination clamp boundaries, decisions,
states, authentication and workflows. `case_ledger.json` records 178 unique
API scenarios referencing 82 of 578 generated IDs. The 496 unconsumed IDs,
filter/grouping, rejection normalization and dynamic-balance scope remain
unaccepted. See `API_COVERAGE_MATRIX.md` for current denominators. Remote run
45183086568 has reached HTTP assertions after the isolated fixture repair;
final acceptance is pending. FileField defaults are asserted by the fixture,
and the exact final test outcome must establish whether they were verified.
Provisional cancellation/duplicate oracles require owner reconciliation, not
automatic production changes to satisfy the test.

