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

## Prompt 3 technical evidence supplement — 25 November 2026

Sections 1–8 and OD-01/OD-02 are preserved. Source-backed API business consumers
now implement duration/holiday/target/forecast/cap/expiry, reason normalization,
all scoped state/role decisions and connected W1/W2 balance invariants. See
AREA2_TEST_BASIS.md and finish-line/PROMPT03_REQUIREMENT_EVIDENCE.json for exact
assertion selectors and actual source-specific outcomes. The current inventory
is 34 operations / 88 generated input entries / 713 preserved IDs / 350 broader
mandatory families; 3,433 API scenarios include 2,256 wire cases. Historical
184-reference/529-unconsumed/329-family counts below describe Prompt 1 only.

Reasons are optional under the existing API helper; its 1000-character strip/
truncation and model TextField's declared 255 bound are explicitly distinguished.
No concurrent duplicate feature, new allocation positivity rule, forecast
credit-at-approval policy, PostgreSQL enforcement or human scope signoff is
invented. The old instruction to mark known decisions xfail is superseded by
the user's strict-regression instruction: the tested 400 assertions stay active.
Current raw/derived evidence and technical completion are separate from owner
review, protected integration, final Prompt 4 and whole-group acceptance.

---

Historical dated records follow. Current source-specific results above supersede their older pending/count labels.

# Test Scope and Test Basis: Horilla HRMS, Leave Module

> **DRAFT.** The team must review, verify against the running app, and edit this before it is used as the test basis.
> Rule and requirement IDs are referenced by the traceability matrix, so keep them stable once agreed.

> 23 November 2026 Area 2 checkpoint: see [AREA2_TEST_BASIS.md](AREA2_TEST_BASIS.md)
> and [API_COVERAGE_MATRIX.md](API_COVERAGE_MATRIX.md) for the source-reconstructed B
> contract, current generated coverage and explicit runtime/oracle gaps. This
> supplement does not convert this draft into an approved or live-verified basis.

## 1. System under test

| Item | Value |
|---|---|
| System | Horilla HRMS (open-source Human Resource Management System) |
| Upstream URL | https://github.com/horilla-opensource/horilla |
| Licence | LGPL-2.1 (see `LICENSE`) |
| Branch | `2.0` |
| Baseline commit | `6c15617b8297b7a6775daa6c29aefcc48b1eb29f` ("[REL] Prepare 2.4.0", 2026-11-10) |
| Stack | Python 3.12, Django 5.2, Django REST Framework (JWT auth), htmx/jQuery UI |
| Storage | SQLite locally (PostgreSQL supported via `DATABASE_URL`) |
| Browser UI | `http://localhost:8000/` |
| HTTP API | `http://localhost:8000/api/leave/...` (Swagger at `/api/swagger/`) |
| Module under test | `leave/` (models, services, views) plus `horilla_api/api_views/leave/` |

## 2. Selected workflows

### W1: Leave allocation (balance is granted)
| | |
|---|---|
| Starting condition | Employee E has leave type "Annual Leave" assigned with `available_days = 0`. An allocation request for E does not exist. |
| User action | E (or HR) creates a leave allocation request for 5 days; a leave approver approves it. |
| Expected outcome | Allocation request status changes `requested → approved`; E's `AvailableLeave.available_days` increases by 5. |
| API | `POST /api/leave/allocation-request/`, `PUT /api/leave/allocation-approve/<id>/`, `PUT /api/leave/allocation-reject/<id>/`, `GET/POST /api/leave/assign-leave/` |

### W2: Leave request (balance is consumed)
| | |
|---|---|
| Starting condition | E has `available_days = 5` for "Annual Leave" (produced by W1). |
| User action | E submits a leave request for 3 working days; the approver approves it. Then E requests 3 more days. |
| Expected outcome | First request `requested → approved`; balance becomes 2. Second request is **rejected by validation** ("Does not have sufficient leave balance…"); balance stays 2. |
| API | `POST /api/leave/user-request/`, `PUT /api/leave/approve/<id>/`, `PUT /api/leave/reject/<id>/`, `PUT /api/leave/cancel/<id>/`, `GET /api/leave/available-leave/` |

### Shared record
**`AvailableLeave`** (one row per employee and leave type), specifically `available_days` (and `carryforward_days`).
- W1 **writes** it (approval of an allocation adds days).
- W2 **reads** it (balance check in `LeaveRequest.clean`) and **writes** it (approval deducts days; cancel/reject restores).

## 3. Functional requirements (draft)

| ID | Workflow | Requirement |
|---|---|---|
| FR-01 | W1 | An employee can create a leave allocation request for an assigned leave type with a requested number of days and a description. |
| FR-02 | W1 | A leave approver can approve a `requested` allocation request; approval adds the requested days to the employee's available balance. |
| FR-03 | W1 | A leave approver can reject a `requested` allocation request with a reason; the balance is not changed. |
| FR-04 | W1 | An allocation request can only be edited while its status is `requested`. |
| FR-05 | W2 | An employee can submit a leave request for an assigned leave type with start/end date and breakdown (full day / first half / second half). |
| FR-06 | W2 | The system rejects a request whose effective requested days exceed the available balance (available + capped carry-forward + forecasted). |
| FR-07 | W2 | The system rejects a request whose dates overlap an existing non-cancelled, non-rejected request of the same employee. |
| FR-08 | W2 | A leave approver can approve a `requested` leave request; approval deducts the requested days from the balance. |
| FR-09 | W2 | A leave approver can reject a leave request; any deducted days are restored. |
| FR-10 | W2 | The employee's available-leave view shows the updated balance after W1 or W2 changes it. |

## 4. Business rules (draft)

| ID | Type (brief requirement) | Rule | Source |
|---|---|---|---|
| BR-01 | **Boundary / limit** | Effective requested days must be `> 0` and `≤ available_days + min(carryforward_days, carryforward_max) + forecasted_days`. | `leave/models.py` `LeaveRequest.clean` |
| BR-02 | **Decision, ≥2 Boolean conditions** | A request is accepted only if: leave type is assigned to the employee **AND** `start_date ≤ end_date` **AND** (if single day) start and end breakdown match **AND** (if the type requires an attachment) an attachment is present **AND** no overlapping active request exists. | `LeaveRequest.clean` |
| BR-03 | **Change of state** | Leave request states: `requested → approved / rejected / cancelled`; `approved → cancel_requested → cancelled` (or back to `approved` if cancel is rejected). `rejected` and `cancelled` are terminal. Allocation requests: `requested → approved / rejected`, editable only in `requested`. | `LEAVE_STATUS`, `LEAVE_ALLOCATION_STATUS`, API approve/reject/cancel views |
| BR-04 | Permission / access | Only a user with leave-approver permission (or the employee's reporting manager) can approve or reject requests; an employee can only see and edit their own requests. | `approver_permission_required` in `horilla_api/api_views/leave/views.py` |

Candidate extra rules if the team needs them: past-date restriction (`EmployeePastLeaveRestrict`), restricted-leave date ranges (`RestrictLeave`), carry-forward cap.

## 5. User roles

| Role | Can | Cannot |
|---|---|---|
| **Employee** (normal user) | Create/view own allocation and leave requests; view own balance; cancel own requests. | Approve/reject any request; see other employees' requests; assign leave types. |
| **Leave Approver / HR Admin** (`leave.change_leaverequest`, `leave.change_leaveallocationrequest`, or reporting manager) | Approve/reject allocation and leave requests; assign leave types; view all requests. | n/a (superuser bypasses some validation; note this when testing). |

## 6. Test basis notes and assumptions

- Expected behaviour comes from the source code above and Horilla docs (https://www.horilla.com/). Where docs and code disagree, record the discrepancy as a potential defect and state which one is treated as the oracle.
- **Assumption A1:** tests that check validation run as a **non-superuser**, because `LeaveRequest.clean` skips the past-date and restricted-leave checks for superusers.
- **Assumption A2:** leave days are counted per `calculate_requested_days` with holidays/company leaves excluded per leave-type settings; test data avoids holidays unless a test targets them.

## 7. Oracle decisions

Team decisions on expected behaviour where the code and documentation do not settle it. Tests use these as their oracle; a mismatch is logged as a defect, never "fixed" by changing the expected result.

| ID | Date | Situation | Decision (expected behaviour) | Basis | Observed at baseline |
|---|---|---|---|---|---|
| OD-01 | 2026-11-23 | Reject (`PUT /api/leave/reject/<id>/`) a leave request whose status is already `cancelled` | Reject with **HTTP 400**; status and balance unchanged | BR-03: `cancelled` is terminal | HTTP 200 (transition accepted) → **defect** |
| OD-02 | 2026-11-23 | Submit an allocation request identical to the same employee's existing **pending** request (same leave type, days, description) | Reject with **HTTP 400**; no second record created | Brief §2: repeated requests must not create duplicates | Duplicate accepted → **defect / endpoint weakness** |

Tests for open decisions are marked `xfail(strict=True)` with the defect issue number, so they stay visible as known failures and turn into an error (XPASS) once the defect is fixed.

## 8. Prompt 1 technical scope supplement — 24 November 2026

Technical reconciliation is completed as documented in finish-line/CONTRACT_RECONCILIATION.md and reports/RAYYAN_FINISH_01_STATUS.md; this does not invent human scope approval. Preserve sections 1–7 and OD-01/OD-02. The existing strict corrected regressions remain active without xfail.

The versioned W1/W2 contract now selects 34 method/route operations (previously 27). Added operations are assignment list/create/detail/update/delete plus leave-type reference and employee-available-type reference reads, required by FR-01 assignment and W1/W2 type binding. Active source exposes 56 leave method/route operations; all 22 non-selected configuration-write/bulk/status/helper operations have explicit reasons in finish-line/OPERATION_INPUT_INVENTORY.json.

One canonical OpenAPI 3.0.3 JSON remains in tests/team/generator/openapi.json. Generated 713 IDs cover 88 operation/input entries; the complete inventory has 329 mandatory families, 241 outside generation. All old IDs and the old 399 dispositions remain traceable. Current references/collection totals are 184/713 and 280 scenarios, not full executed coverage. The full contract remains mandatory across Prompts 2–4. Actual production Swagger 2.0 is compared semantically with resolver/serializer/model behavior; it is not a competing canonical contract.

No additional policy approval was invented. Full runtime/coercion/filter/media and source-backed state/decision plans are technical test-basis work; exact consumption and new relational outcomes remain pending. Overall release HOLD and team signoff obligations remain.
