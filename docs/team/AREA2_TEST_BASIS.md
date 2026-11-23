# Area 2 test basis: Phase B prerequisite reconstruction

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

