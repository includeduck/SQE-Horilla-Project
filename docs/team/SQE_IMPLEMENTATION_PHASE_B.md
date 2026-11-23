# Codex Implementation Prompt B

## A. Context

Execute **only implementation Phase B** for `includeduck/SQE-Horilla-Project`, on behalf of **Syed Muhammad Rayyan Hassan, 24I-3000**, `rayyanhasan899`, section SE-5B.

Rayyan owns Area 2, API/integration testing, OpenAPI and automated EP/three-point BVA generation/regeneration. Wasay owns static/unit/MCC/MC/DC/mutation/CI; Zain owns Area 3 coordination and usability/accessibility/security/performance/recovery. Shared management and two use cases per member also apply. This phase implements the generator and a minimal HTTP consumer. The complete API suite is Phase C, and the two-constraint demonstration/personal browser completion is Phase D.

The existing Django/DRF Horilla leave module implements W1 leave allocation and W2 leave consumption sharing `AvailableLeave`. The upstream baseline is `6c15617b8297b7a6775daa6c29aefcc48b1eb29f`. At planning HEAD `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0`, team test folders were placeholders. Phase A should establish the actual environment, test basis, scoped spec, input/coverage matrix and synthetic lifecycle. Reinspect current files rather than trusting that A ran successfully.

Read `docs/team/SQE_PHASE_2_IMPLEMENTATION_ROADMAP.md`, `SQE_PHASE_1_PERSONAL_AUDIT.md`, `SQE_IMPLEMENTATION_PHASE_A.md`, `reports/SQE_IMPLEMENTATION_PHASE_A_STATUS.md`, `TEAM.md`, `SCOPE.md`, current Area 2 basis/matrices, `tests/team/README.md` and the actual chosen spec. The [official seven-page brief](https://chatgpt.com/library?file_id=libfile_7ca0240df8688191b399f878fa329e4b&account_id=personal) governs requirements, particularly page 2 automated generation and page 5 viva. Record direct PDF access limitations if any and use the roadmap's referenced extraction for independent work.

## B. Objective

Build a scoped, reproducible generator that reads the reviewed OpenAPI contract and outputs valid/invalid EP classes and three-point BVA cases. Prove a real HTTP test slice consumes that output with traceable assertions.

## C. Requirements

1. Read the spec to generate EP classes and values at each applicable real boundary. Valid/invalid groups must cover every selected input category from A. API tests must consume generated output. [Brief page 2; roadmap R3-R5]
2. EP invalid cases vary one invalid input while keeping unrelated input/setup valid. BVA values are just below, at and above actual limits with an explicit unit, inclusivity and expected predicate. Enums/unbounded values have EP and justified BVA applicability. [Brief page 2]
3. Support actual scoped data types, required/optional/null rules, enums, documented ranges/lengths/collections, formats and local references used by the reviewed spec. Support dynamic employee/date/balance bindings in the agreed representation. Do not claim support for unused schema features or silently drop required constraints.
4. Produce deterministic case identities/provenance and data/spec fingerprints so stale output and regeneration effects are detectable. This is the implementation design used to demonstrate assignment coverage.
5. Use normal seeded employee/approver roles, real HTTP Requests and persisted-state readback in the consuming slice. Keep all team tests under `tests/team/`. [Brief pages 1-2]
6. Update coverage, actual progress/effort, test instructions and AI-use records without fabricated evidence. [Brief pages 2, 5 and 7]

## D. Repository investigation and prerequisite gate

Inspect Git status and newer teammate contributions. Read A's status report and inspect the actual spec, fixture settings, declared dependencies, initialized state and coverage inventory. Run its relevant smoke/schema validation commands, with synthetic isolated data. An absent report is not proof of failed implementation if files/evidence establish the foundation, but record that gap and repair a small in-scope prerequisite if possible.

Inspect `horilla_api/api_urls/leave/urls.py`, leave serializers/views, auth routes, `horilla_api/apps.py`, pagination helpers and `leave/models.py`/`methods.py` to verify constraints before encoding them. Prefer the validated `/api/v1/` path and actual Swagger dialect chosen in A. Reuse compatible teammate tooling/configuration.

If a spec/oracle/environment dependency is missing, diagnose and safely repair within Rayyan's scope when supported by existing evidence. Ask only for a material unresolved business decision. Do not generate cases claiming coverage of blocked constraints. Continue independent generator work that can be verified without the blocked server, and report HTTP evidence as pending if unavailable.

## E. Implementation instructions

### 1. Generator and interface

Create or extend a small readable generator under `tests/team/generator/`, proposed entry point `generate.py`. Reuse an existing implementation if introduced since planning. Accept explicit spec and output paths and the fixture/binding context where needed. Expose a reproducible command documented in `tests/team/README.md`; choose details consistent with the chosen dialect.

Resolve the spec's actual local references and input locations. Distinguish body payloads, path/query values and harness credentials/headers. Required checks differ from nullable checks. Enum/type/format/reference classes need meaningful valid and invalid representatives. Treat schema constraints and relational business constraints according to the documented representation. Avoid a framework supporting the entire OpenAPI ecosystem when a scoped reader is sufficient.

Generate cases from spec constraints rather than hardcoded per-endpoint expected values. A small documented scenario layer can bind current balance, employee IDs, known-missing IDs, calendar/date anchors and attachment fixtures, but it must not replace the spec as the source of declared limits. Preserve enough provenance to demonstrate how each value was derived.

Use a stable synthetic date anchor or recorded run anchor and reproducible seed. Separate baseline valid values from the single mutated input. Distinguish absent fields from explicit null, empty values and wrong types. Generated HTTP requests must be serializable in their actual media type. Avoid invalid setup inadvertently causing a different validation error first.

For numeric/date/length bounds, correctly handle inclusive/exclusive limits and applicable units. A floating day count does not automatically imply arbitrary precision or a half-day unit. Derive any domain increment from the accepted contract and document it. Use integer counts for lengths, days for date limits where appropriate, and exact or tolerance-aware numeric handling compatible with the API.

Include documented custom extensions only for real scoped relationships such as effective requested duration versus runtime balance or start/end ordering. Unknown relevant constraints must cause a visible diagnostic and incomplete coverage status. For genuinely irrelevant unsupported features, report exclusions explicitly.

### 2. Output and traceability

Write machine-readable JSON or the established equivalent under `tests/team/generator/`. Each case should identify case ID, operation/method, input location/name, requirement/rule IDs, EP/BVA class, value/omission/binding, otherwise valid baseline request, expected predicate, source constraint and fingerprint. This is a recommended structure and may be adapted to existing compatible conventions.

Record the spec and binding fingerprints. A consumer must reject or regenerate stale data rather than silently reuse it. Keep volatile run metadata separate from deterministic comparison data. Exclude credentials/tokens and personal data from artifacts. Preserve failed outputs/logs as real evidence and keep transient run artifacts out of unrelated source paths.

Update `API_COVERAGE_MATRIX.md` with generated versus manually bound inputs and justified N/A entries. Generation success alone does not establish that API cases ran or that behavior passed.

### 3. Focused generator verification

Write focused regression tests for the constraints actually used by the scoped contract, including reference resolution, missing versus nullable, enum/wrong type, numeric/date boundaries, valid baseline preservation and deterministic output. Add checks that unsupported relevant constraints are visible and invalid EP tests change only the targeted dimension.

The same spec and logical bindings must generate equivalent ordered case data. Changing a supported constraint in a small verification fixture must change relevant output, proving that values are derived. This is generator verification only. Preserve the complete two-real-constraint assignment demonstration for Phase D.

### 4. Minimal HTTP consumer

Reuse A's isolated real server/DB and normal roles. Add a small pytest/Requests consumer under `tests/team/api/` using parametrization from the generated artifact or generator interface. Exercise at least one valid EP representative, one isolated invalid EP representative and a three-point boundary set for a genuine selected limit. Choose cases supported by the reviewed contract, not an invented limit.

Each executed case must report its case/spec/data identity. Assert expected response/error semantics and persisted state after success/rejection. Use HTTP readback under the employee role for their balance/request, with fixture ORM checks only as independent corroboration/setup. Ensure a valid case really exercises application behavior rather than a mocked endpoint.

A known product defect may cause a genuine failure. Keep that failure and source-backed expectation visible, record the dependent Phase C repro, and avoid status-only success assertions or redefining expected behavior solely to pass. Do not duplicate the full Phase C suite here.

### 5. Documentation and integration contract

Document exact generator and consumer commands, required environment, expected output format, input case selection and freshness checks. Update management estimates/actual measurable activity and AI disclosure. Keep one cohesive fixture/configuration design and preserve Wasay/Zain interfaces. Provide Linux-compatible invocation for later CI where practical without taking over CI architecture.

## F. Restrictions

- Preserve application behavior, existing style/names, stable FR/BR IDs and compatibility. Avoid restructuring, duplicate schemas, unused generic abstractions and unnecessary dependencies.
- No unrelated HR features, artificial maximums or replacement of existing schema infrastructure.
- Test independent code under `tests/team/`; upstream tests remain reference material and earn no marks.
- Product bug fixes and full decision/state/integration coverage belong to C. Zain's browser/security/performance/recovery and Wasay's unit/mutation/gate retain ownership.
- Use synthetic local disposable data and free/open-source tools. Preserve existing unverified DBs and secrets.
- No commits, push, published issues/PRs or external messages without separate execution-session authorization. Document required own-account commits as pending when absent.
- Complete B only and wait. Do not automatically execute C.

## G. Testing and completion conditions

Run generator-focused checks, validate the spec, compare repeated generation, inspect invalid-case isolation and boundary derivation, and test stale/unsupported-constraint handling. Execute the minimal consumer against a real HTTP server and capture exact command, result and case lineage. Confirm logical state reset/order independence for the slice.

Completion means the generator produces the declared supported coverage and the consumer genuinely uses its output. Report generator correctness, HTTP execution and product correctness separately. An unavailable server does not justify claiming the consuming requirement complete. Leave concrete failures/blockers visible and continue verifiable independent work.

## H. Completion report

Write `docs/team/reports/SQE_IMPLEMENTATION_PHASE_B_STATUS.md` with inspected HEAD/diff, A prerequisite verification, created/modified files, generator capabilities/exclusions, source constraints and fingerprints, requirement IDs, exact commands/versions, checks and actual pass/fail/block counts, evidence paths, incomplete coverage, teammate dependencies and next readiness.

Return a concise completion summary covering files, functionality, requirements completed, actual tests/results, remaining issues/dependencies and next step. Identify **SQE_IMPLEMENTATION_PHASE_C.md** only with its actual prerequisites. Wait for the user's instruction.
