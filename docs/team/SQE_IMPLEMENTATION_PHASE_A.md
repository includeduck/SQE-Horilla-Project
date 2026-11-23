# Codex Implementation Prompt A

## A. Context

Execute **only implementation Phase A** for `includeduck/SQE-Horilla-Project` on behalf of **Syed Muhammad Rayyan Hassan, 24I-3000**, GitHub `rayyanhasan899`, section SE-5B. This prompt is intended for the later implementation stage. Its presence in the repository does not authorize automatic execution.

Rayyan owns Area 2, API/integration testing, OpenAPI and EP/three-point BVA test-data generation with regeneration. Wasay owns Area 1, static analysis, white-box coverage/MCC/MC/DC, mutation and CI quality gates. Zain owns Area 3 coordination, browser/use cases, usability/accessibility, defensive security, performance and recovery. Shared test management applies to all. The assignment also explicitly requires two use cases per member with all flows automated, so Rayyan has a personal contribution coordinated with Zain.

Horilla is an existing Python/Django/DRF HRMS. Selected workflows are W1 allocating employee leave and W2 requesting/approving leave that consumes the same `AvailableLeave(employee_id, leave_type_id)` balance. The canonical scope example is zero balance, allocate five, approve a three-day leave, then reject an independent three-day request with balance remaining two. Browser UI, API and persistence already exist. At planning time only team scaffolding existed in `tests/team/api/` and `generator/`. Recheck current state before assuming that remains true.

Read the official seven-page [assignment brief](https://chatgpt.com/library?file_id=libfile_7ca0240df8688191b399f878fa329e4b&account_id=personal), `docs/team/SQE_PHASE_1_PERSONAL_AUDIT.md`, `SQE_PHASE_2_IMPLEMENTATION_ROADMAP.md`, `TEAM.md`, `SCOPE.md`, `SETUP.md` and `tests/team/README.md`. The official assignment governs academic requirements. Team allocation governs ownership. Scope is explicitly DRAFT. If the PDF is inaccessible, use the roadmap's page-referenced extraction while recording that direct verification is pending, and request the missing authoritative text only when a decision depends on it.

The baseline is `6c15617b8297b7a6775daa6c29aefcc48b1eb29f`; planning HEAD was `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0` on `sqe-team`. Use current files and preserve newer teammate contributions. Rayyan has confirmed his roll number as 24I-3000.

## B. Objective

Establish a reproducible, isolated local testing foundation and an evidence-backed API contract/input inventory. Define the scope/oracles, generator requirements, API coverage matrix and Rayyan's two use-case specifications before building the generator or full test suite.

## C. Requirements

1. Verify local web/API/storage functionality with synthetic data and a repeatable setup/reset procedure. Record actual tool versions, upstream URL, licence and baseline. Confirm where repository-registration evidence is stored, or mark that shared dependency pending. [Brief section 1, page 1]
2. Preserve FR-01 through FR-10 and BR-01 through BR-04 IDs. Ensure at least eight total functional requirements, at least three per workflow, four business rules including boundary/Boolean decision/state change, and two distinct normal-user roles are covered. Resolve meaning with code/docs or explicit justified assumptions. [Brief page 1; `SCOPE.md`]
3. Review the generated API specification and reuse it if accurate. Otherwise create a minimal accurate scoped OpenAPI artifact. Inventory every selected body/path/query input, authentication handling, required/optional/null rules, types/enums, real bounds, media types, roles and success/error responses. [Brief page 2]
4. Plan EP for every valid/invalid input group, one invalid value per EP test, three-point BVA at each genuine limit, decision combinations for each multi-condition rule, all allowed state transitions and at least one invalid transition from each state. Document BVA inapplicability for genuinely unbounded/discrete inputs instead of inventing limits. [Brief page 2]
5. Define coverage for rule rejections, repeated requests/no duplicates and persisted shared-record readback after success/rejection. Include the W1-to-W2 integrated example. [Brief page 2]
6. Specify two Rayyan-attributed use cases, each with preconditions, main flow, at least two alternative and two exception flows, displayed expected outcome and persistent postconditions. Coordinate allocations with Zain; keep distinct case IDs. [Brief page 2]
7. Record honest Area 2 three-point estimates and contributions to shared planning, risks, criteria and traceability. The group needs eight product/two project risks, 1-5 likelihood/impact on a 5x5 matrix, three measurable exit criteria with two linked to highest risks. Record proposed values as proposed and keep teammates' missing contributions visible. Update AI disclosure with actual checks and retain this prompt. [Brief pages 2, 5, 7]

## D. Repository investigation before edits

Inspect Git status/branch/history and current team files. Read the phase roadmap and audit in full, then verify the relevant claims against current source. Inventory any new tests/specs/configurations before choosing new filenames.

Inspect these existing interfaces in particular.

- `horilla_api/apps.py` mounts `/api/v1/` and `/api/`. Prefer the versioned prefix for new tests while preserving aliases. Swagger JSON is served by `horilla_api/urls.py` at `/api/v1/swagger.json/`, with a trailing slash. It may need admin access outside DEBUG.
- `horilla_api/api_urls/auth/urls.py`, `api_views/auth/views.py` and authentication settings define JWT login and headers.
- `horilla_api/api_urls/leave/urls.py`, `api_views/leave/views.py`, `api_serializers/leave/serializers.py`, `api_decorators/base/decorators.py`, pagination and reason helpers define actual behavior.
- `leave/models.py`, `methods.py`, `services.py`, relevant forms/views and migrations define records, rules and possible API/UI differences.
- `scripts/team/seed_team.py`, `reset.ps1`, `smoke_api.py`, `docs/team/env.example`, `horilla/settings/` and current test tooling define environment/data lifecycle.
- Read upstream leave/API regression tests as reference evidence. Implement independently authored team cases, with no upstream tests counted toward assignment results.

Recheck the audit's candidate findings. API/model balance differences, missing positive allocation validation, rejection selecting the acting approver's balance, cancellation graph mismatch, allocation reversal, optional reason/length ambiguity, generic versus self-service creation differences and non-owner allocation fall-through all require evidence. Record observed code behavior separately from intended oracle. Product correctness must not be inferred from the mere presence of a handler.

## E. Implementation instructions

### 1. Establish environment and safe data lifecycle

Reuse an existing compatible team environment/configuration when present. Otherwise create the minimum supported local Python environment and necessary open-source test dependencies. Inspect available Python versions and repository compatibility. Record actual versions rather than copying historical version claims. Avoid unrelated upgrades.

Use a dedicated disposable synthetic test database and local server. Prefer pytest-django's real test-server lifecycle with Requests if the repository has no better team convention. Keep application settings unchanged when a scoped test setting/fixture can supply isolation. Resolve exact DB paths before any reset. Preserve any existing unverified database and application environment. Reuse the seed logic to create company, employee, approver and assigned leave type in the disposable database without running its default destructive reset against unrelated data.

Verify that a fresh start produces zero balance and no existing requests, separate employee/approver identities and correct manager/permissions. The seed is not a complete reset because it resets balance while retaining existing requests. Demonstrate two reproducible initializations with the same logical state. Record how the server and fixtures use the same database and how cleanup works. Preserve Windows compatibility and provide the appropriate reproducible Linux approach for CI without rewriting unrelated scripts.

Perform a small real HTTP smoke check for login and employee balance readback, with timeouts and actual assertions. This is environment validation. Full API tests belong to Phase C. Admin can set up data, while employee/approver execute rule scenarios. Do not add application reset/testing endpoints.

### 2. Resolve test basis and inventory

Create or update `docs/team/AREA2_TEST_BASIS.md` and `API_COVERAGE_MATRIX.md`, reusing equivalent teammate artifacts if present. Include source/line references, endpoint-method-role inventory, fields/locations/types/media/constraints/defaults, response shapes, valid/invalid classes and applicable boundaries. Include path IDs, query pagination/filter inputs actually used, omissions/nulls/wrong types and reference existence/ownership. Do not expand to unrelated HR endpoints.

Cover W1 generic or employee allocation endpoints as justified, approval/rejection/detail, W2 create/detail/edit/approval/rejection/cancellation and balance readback. Include assignment or cancellation-decision endpoints where required by scope/setup or the agreed state graph. Explicitly record excluded endpoints and why they are outside W1/W2.

Create rule decision and state matrices, including each state and invalid action. Clarify whether terminal-state behavior, requested cancellation and approved allocation reversal follow the draft, documented assumptions or a reported defect. Resolve what duplicate creation means for the selected record and acknowledge absence of an idempotency-key contract. Do not silently substitute observed defects for intended rules.

Use source-backed reversible assumptions permitted by the brief. Ask the user only when an unresolved business decision cannot be justified and materially changes implementation. Continue independent work and label dependent coverage blocked while waiting. Finalizing source-backed assumptions does not require automatic instructor/team approval of every routine choice.

The phrase “all API coverage criteria” is undefined in the PDF. Document a proposed operation/method, input/response, role, decision/transition and shared-state checklist, and adopt any supplied instructor checklist. Keep code statement/branch coverage with Wasay.

### 3. Create the contract

Export/review current Swagger if usable. If creating a new artifact, default to scoped OpenAPI 3.0.3 in `tests/team/generator/openapi.yaml`, unless repository context supports reuse in the existing dialect. Record the chosen dialect and conversion. Validate syntax, references, paths/methods and schema. Do not claim undocumented fields or status codes.

Declare real constraints and expected predicates. Dynamic rules such as current balance or relative date limits need explicit scenario bindings or documented spec extensions that the generator can read. Define boundary units from actual domain behavior, using half days only where justified. The seed's leave-type `total_days=10` is not evidence of a maximum allocation request. Unbounded text must not receive a fabricated maximum.

### 4. Personal/shared records

Create `docs/team/RAYYAN_USE_CASES.md` with two cases within existing workflows, proposed IDs `UC-RAY-01` and `UC-RAY-02` if unused. Their exact selection is provisional until checked for overlap with Zain's allocation. Alternative/exception flows must be real, testable app behavior. Plan browser outcomes and postconditions. Do not implement broad Area 3 evaluations.

Use existing shared management documents. If absent, create `docs/team/AREA2_MANAGEMENT.md` for Rayyan's contributions with explicit pending group inputs. Include scope/risk approach, roles/environment/data, dependency schedule, entry/exit/suspend/resume rules, three-point estimates, product/project risk contributions and proposed measurable criteria. Do not fabricate dates, approval, effort, weekly history or execution results. Preserve this prompt and update `AI_USE_RECORD.md` honestly.

## F. Restrictions

- Preserve working functionality, stable FR/BR IDs, existing naming/style and compatibility.
- Avoid restructuring, duplicate frameworks/helpers, unapproved features and unrelated dependency/application changes.
- This phase may add environment/test foundation, specification and documentation. The generator, full suite and source bug fixes belong to later phases.
- Preserve Wasay's Area 1/CI and Zain's specialist modules. Reuse their new interfaces if present.
- Use free/open-source tools and synthetic local data. Keep secrets/tokens/local DBs out of Git and reports.
- No commits, pushes, issue/PR publication or external messages unless separately authorized in the execution session. Record the mandatory own-account commit requirement as pending when authorization is absent.
- Finish this phase only. Do not launch Phase B automatically.

## G. Testing, verification and completion conditions

Verify both clean initializations, exact synthetic logical state, employee/approver JWT and balance HTTP checks, server/database alignment, schema validation and operation coverage. Cross-check every selected input against serializers/routes and every intended rule against its evidence. Ensure every matrix entry has coverage planned or a concrete blocker, and all FR/BRs retain mappings.

Check the two use cases each contain main plus at least two alternative and two exception flows with postconditions. Confirm estimates precede implementation, proposed criteria have units/denominators/risk links and AI entries distinguish Codex's checks from Rayyan's pending review.

Completion requires actual evidence for the environment/spec foundation and an honest status for unresolved oracles. Missing packages/network or user decisions must be reported with attempted recovery and dependent tasks. Continue permissible independent work, then leave an accurate Partial/Blocked phase report when the foundation cannot be verified.

## H. Completion report

Write `docs/team/reports/SQE_IMPLEMENTATION_PHASE_A_STATUS.md`. Include inspected commit and working-tree changes, requirement IDs R1-R16 from the roadmap, created/modified files, implemented foundation/contracts, source-backed decisions, exact commands/tool versions/results, evidence paths, unresolved conflicts/blockers, teammate dependencies, estimates/actual effort when measurable, and readiness for B.

End your user response with concise files/results/pending items and identify **SQE_IMPLEMENTATION_PHASE_B.md** as the next prompt only if its prerequisites are met. Wait for the user's next instruction.
