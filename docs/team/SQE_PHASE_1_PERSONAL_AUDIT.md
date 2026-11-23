# SQE Phase 1 Personal Responsibility Audit

Prepared for **Syed Muhammad Rayyan Hassan** on **22 November 2026**.

Repository examined at `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0`, branch `sqe-team`. The GitHub branch resolved to the same commit during this audit. Repository location is `includeduck/SQE-Horilla-Project`.

## Audit basis and principal findings

Rayyan explicitly owns **Area 2**, comprising API and integration testing, an accurate OpenAPI specification, an EP/three-point BVA data generator, and regeneration after specification changes. His practical deliverable is an independently authored, repeatable test system for two connected Horilla leave workflows. The application and its API already exist in the upstream baseline. The team-owned API tests and generator have yet to be implemented. [Evidence E1, E2, E4, E7]

The user's corrected roster identifies Rayyan, Muhammad Wasay Tariq, and Zain Bin Jabir. This matches the three names in the repository except that Rayyan is recorded as “Muhammad Rayyan Hassan.” **Phase 2 identity correction.** Rayyan confirmed his roll number as **24I-3000** on 22 November 2026. The current roster, submission names and this audit now use that identifier. The remaining implementation findings describe the audited commit. Residual mentions of Marwa in the earlier request have no supporting assignment or contribution evidence in this repository. [E1; user's Phase 2 instruction]

There is also a mandatory **two-use-cases-per-member** requirement in the assignment. Zain owns Area 3, but the team must explicitly allocate Rayyan's two use cases and their authorship. Shared test management, individual commits, AI disclosure, and viva preparation also apply to Rayyan. [E1, E7]

### Evidence conventions

| ID | Source and exact locator | What it establishes |
|---|---|---|
| E1 | `docs/team/TEAM.md`, lines 3-17, especially roster lines 7-9 and shared duties line 13 | Explicit area ownership, GitHub accounts, section and submission naming |
| E2 | `docs/team/SCOPE.md`, sections 1-6, lines 3-81 | Draft workflows, FR-01 through FR-10, BR-01 through BR-04, roles and assumptions |
| E3 | `docs/team/SETUP.md`, lines 3-16, 18-93 | Documented environment, setup, seed, reset and smoke commands |
| E4 | `tests/team/README.md`, lines 3-15, and complete tracked `tests/team/` tree at audited commit | Separate team tests and intended area folders, currently placeholders |
| E5 | `scripts/team/seed_team.py`, lines 17-112; `reset.ps1`, lines 12-38; `smoke_api.py`, lines 6-24 | Existing setup support and limited smoke check |
| E6 | `docs/team/AI_USE_RECORD.md`, lines 3-8 | Wasay's disclosed scaffold work and outstanding scope/registration review |
| E7 | **SQE_Final_Project Fall 2026.pdf**, all seven pages, especially sections 1, 2, 6 and 7, pages 1-3 and 5-7 | Mandatory academic requirements and rubric |
| E8 | `horilla_api/api_urls/leave/urls.py`, lines 9-55; `horilla_api/apps.py`, lines 22-38 | Leave route map and versioned/legacy API mounts |
| E9 | `horilla_api/api_views/leave/views.py`, classes identified throughout this report | Actual endpoint implementations and response behavior |
| E10 | `horilla_api/api_serializers/leave/serializers.py`, lines 12-102, 180-215, 258-291, 418-454, 490-514 | API input fields and validation |
| E11 | `leave/models.py`, lines 157-173, 732-772, 1376-1446, 1980-2000, 2046-2209, 2445-2494 | Data model, state choices and model validation |
| E12 | `leave/methods.py`, lines 13-30, 208-310; `leave/services.py`, lines 106-116 | Day calculation, cancellation and balance helper |
| E13 | `.github/workflows/unit-tests.yml` and `quality.yml`, trigger lines 6-11; complete `.github/workflows/` inventory | Inherited CI and missing team quality gate |
| E14 | Git history from upstream baseline through audited HEAD; commit `4bd2314ed` and its `TEAM.md` diff | Team additions, explicit reassignment and observed authorship |
| E15 | GitHub repository metadata, branch search, issue search, PR search and HEAD PR-workflow-run query on audit date | Public repository, one listed branch, no returned issues/PRs or HEAD PR runs |
| E16 | `README.md`, Features, Quick Start and License; `LICENSE`; `horilla/settings/base.py`, lines 235-243; `requirements.txt`, lines 28, 53, 56, 63, 82 | HRMS features, application stack, database and dependencies |
| E17 | `horilla_api/api_decorators/base/decorators.py`, lines 137-213; `horilla_api/api_methods/base/pagination.py`, lines 6-27; `horilla_api/api_methods/base/methods.py`, lines 89-101 | Approver authorization, pagination and reason normalization |

File line numbers refer to the audited commit. Relative paths are repository-relative. **Explicit** means directly assigned by a source. **Observed** means supported by inspected files or Git data. **Inferred** means an engineering interpretation that needs agreement or execution evidence.

The assignment PDF is supplied outside the Git repository. Its current seven-page copy was read in full. It can be opened through the [assignment brief](https://chatgpt.com/library?file_id=libfile_9c8f6701fa408191963b68c0d655809d&account_id=personal). No assignment PDF or DOCX is tracked in this checkout.

### Investigation scope and limitations

The audit inventoried all **9,137 tracked files**, inspected the full top-level structure and all team documentation/scripts, searched tracked text for member names and task documents, inspected the relevant leave models, methods, API views, serializers, permissions, upstream regression tests, application settings and workflow configuration, and compared every team commit with the pinned baseline. Git history is complete locally, with **6,851 reachable commits** and a non-shallow checkout. [E4, E8-E14]

No `handoff.md` or equivalent filename was found in current tracked/untracked project files or the queried reachable handoff Markdown history. No separate team implementation plan, personal contribution document, test report, OpenAPI artifact or assignment document was found. Unrelated vendor assets and other HR modules were inventoried and searched for ownership, with detailed code review concentrated on Rayyan's assigned workflows.

The working tree initially had no changes. This audit creates only this report. Runtime testing was unavailable in the current checkout because `.venv`, `.env`, `TestDB.sqlite3` and `tests/team/.baseline.sqlite3` are absent. No installation, database reset, application write, test-data creation, implementation, commit or push was performed. Accordingly, source findings below do not claim a passing test run.

Direct `git ls-remote` failed with a host/network resolution error. Connected GitHub access succeeded independently. It confirmed `sqe-team` at local HEAD, a public repository and no additional branch after pagination. Searches returned no issues and no PRs, including closed PRs. The HEAD workflow query returned no PR-triggered runs. Search results cannot establish deleted history, unpushed work, or the state of every past Actions run. Branch protection and deployment settings were not verified. [E15]

## Section 1. Project Overview

### Objective and selected problem

Horilla is a web-based HR management information system. It already manages employees, recruitment, attendance, leave, payroll, performance, assets, helpdesk, projects and reporting. The university project evaluates the quality of a selected part of that existing system through automated tests and evidence. [E16; E7, section 1]

The selected module is **Leave Management**. The quality question is whether granting and consuming employee leave preserves the correct shared balance, permissions and request states, including invalid inputs, rejected operations and repeated submissions. [E2, sections 2-5]

| Workflow | Starting data and action | Intended observable result |
|---|---|---|
| W1, leave allocation | Employee has assigned Team Annual Leave with zero available days. Submit an allocation request for five days and approve it as a separate approver. | Allocation becomes approved and employee's available balance becomes five. |
| W2, leave request | Use the five days granted by W1. Submit and approve a three-day leave request, then attempt a separate, non-overlapping three-day request. | First approval leaves two days. The second request fails balance validation and preserves the balance of two. |

The shared persistent record is `AvailableLeave(employee_id, leave_type_id)`, particularly `available_days` and `carryforward_days`. Its model declares uniqueness for employee plus leave type. Holidays, company leave settings, breakdowns and effective date calculations influence how much leave is consumed. Select deterministic dates and settings before asserting numerical results. [E2, lines 23-42 and 79-81; E11, lines 747-772; E12, lines 13-30]

### Technologies and architecture

| Layer | Existing implementation |
|---|---|
| Runtime and framework | Python, Django 5.2, Django REST Framework and SimpleJWT. Team setup chooses Python 3.12.10. `requirements.txt` supports Python 3.12-3.14 and specifies `Django~=5.2.17` and DRF 3.18.3. Documented installed Django 5.2.19 is historical environment evidence. |
| Browser interface | Django templates, class-based and function-based views, HTMX, jQuery, JavaScript and SCSS/CSS. |
| HTTP API | DRF `APIView` handlers, serializers and custom authorization decorators. `/api/v1/` is mounted alongside the `/api/` alias. |
| Persistence | Django ORM and migrations. Default local SQLite path is `<repo>/TestDB.sqlite3`; PostgreSQL is supported through environment configuration. |
| Existing API documentation | `drf-yasg` schema generation, Swagger UI and ReDoc. Published schema accuracy for selected leave operations still needs review. |
| Team's planned verification tools | pytest/Requests for Area 2, SonarQube/coverage/mutation for Area 1, Playwright/Lighthouse/axe/ZAP/pip-audit/k6 for Area 3, GitHub Actions for integration. Most team tooling is planned only. |

API requests pass through authentication, route selection, authorization and serializer validation, then update Django model records. Browser forms and model validation use overlapping but distinct paths. This distinction matters because the API serializer does not automatically enforce every condition found in `LeaveRequest.clean()`. [E8-E12, E17]

### Repository structure and entry points

| Paths | Purpose and relevance |
|---|---|
| `manage.py`, `horilla/asgi.py`, `horilla/wsgi.py` | Management/server entry points. `manage.py` sets `DJANGO_SETTINGS_MODULE=horilla.settings`. |
| `horilla/settings/`, `horilla/urls.py` | Settings package and main routing. The settings are split across `base.py`, `security.py`, `addons.py`, `local_settings.py` and `__init__.py`. |
| `horilla_api/` | API routes, views, serializers, schema, authentication, permissions and upstream API regression tests. |
| `leave/` | Selected business module, ORM models, migrations, browser forms/views, services, methods and upstream tests. |
| `base/`, `employee/`, `horilla_auth/`, `auth/` | Company, employee, reporting relationships, accounts and related shared functionality. |
| `docs/team/`, `scripts/team/`, `tests/team/` | Team requirements/ownership/setup, seed/reset/smoke scripts and designated team test folders. |
| `docs/team/evidence/`, `docs/team/reports/` | Currently empty evidence/report destinations containing `.gitkeep`. |
| `.github/`, `Makefile`, `.coveragerc`, `pyproject.toml` | Inherited review templates, CI, coverage and lint setup. |
| `attendance/`, `asset/`, `payroll/`, `pms/`, `project/`, `recruitment/`, `helpdesk/`, `onboarding/`, `offboarding/`, `report/` | Other HR features and possible integrations. Their existence does not assign their development to Rayyan. |
| `accessibility/`, `biometric/`, `dynamic_fields/`, `facedetection/`, `geofencing/`, `horilla_audit/`, `horilla_automations/` | Shared access/extension, device, configuration, auditing and automation functionality. |
| `horilla_backup/`, `pg_backup/`, `horilla_crumbs/`, `horilla_dbtemplate/`, `horilla_documents/`, `horilla_ldap/`, `horilla_meet/`, `horilla_theme/`, `horilla_tour/`, `horilla_views/`, `horilla_widgets/`, `master_import/`, `notifications/`, `outlook_auth/`, `whatsapp/` | Supporting platform apps and optional integrations. |
| `static/`, `templates/`, `media/`, `load_data/` | Browser assets, templates, uploads placeholder and upstream synthetic/demo fixtures. Vendor Playwright files under static assets are library contents. |
| `Dockerfile`, `docker/`, `docker-compose*.yml` | Existing container setup. |
| `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE` | Upstream product/release/contribution/security/licence documentation. Team assignments appear in `docs/team/TEAM.md`. |

The tracked documentation inventory also includes Docker publication notes, API documentation, DB-template and tour documentation, upstream asset/SCSS readmes, and an employee import spreadsheet. No ownership allocation was found in those supporting materials. The detailed leave API entry point is `horilla_api/api_urls/leave/urls.py`; API prefixes are added in `horilla_api/apps.py`, lines 34-38. [E8, E16]

### Expected final deliverable

The assignment requires one group PDF and a ZIP containing the Git repository including `.git`, a public GitHub link, reproducible setup and test data, tests/scripts/tool versions, CI configuration, documented defect-fix and blocked PR evidence, results, ownership, AI disclosure and a release/hold decision with actual versus target release criteria. `TEAM.md` proposes `Project_24I-3071_24I-3000_24I-3130_B.pdf` and `.zip`, with the section suffix still requiring confirmation. Rayyan supplies the Area 2 evidence and his shared contributions to this package. [E7, sections 6-7; E1, lines 15-17]

## Section 2. Team Responsibility Distribution

| Team Member | Assigned Responsibilities | Related Modules | Evidence |
|---|---|---|---|
| Syed Muhammad Rayyan Hassan, recorded as Muhammad Rayyan Hassan, `rayyanhasan899` | **Explicit Area 2**. API/integration tests, OpenAPI, EP/BVA generator and regeneration. Shared management and individual academic requirements. | `tests/team/api/`, `tests/team/generator/`; tests exercise `horilla_api/.../leave/` and `leave/`. | `TEAM.md` line 8; `tests/team/README.md` lines 8-9; assignment pages 2, 5 and 7. |
| Muhammad Wasay Tariq, `includeduck` | **Explicit Area 1**. SonarQube, white-box tests, statement/branch coverage, MCC/MC/DC, mutation and CI gate. Shared management. | `tests/team/unit/`, future Sonar/mutation configuration and `.github/workflows/`. Existing setup scripts and draft docs were authored in his commits. | `TEAM.md` line 7; AI-use entries lines 7-8; four post-baseline commits. |
| Zain bin Jabir, `i243130-coder` | **Explicit Area 3**. Use cases/Playwright, usability/accessibility, defensive security, performance and recovery. Shared management. | `tests/team/e2e/`, `security/`, `perf/`, `recovery/` and corresponding reports. | `TEAM.md` line 9; `tests/team/README.md` lines 10-13. |

**Ownership overlap requiring coordination.** The brief's two use cases per member applies to Rayyan and Wasay as well as Zain. Zain can own the browser framework and Area 3 coordination, while individual use-case contributions still need names and test IDs. Recovery is assigned to Zain even though it uses an API/integration runner and can reuse Rayyan's fixtures. API permission checks overlap with Zain's security access matrix. These are coordination dependencies, and the repository contains no finer division. [E1, E4; E7, pages 2 and 5]

### Contribution evidence

| Commit | Observed change | Supported attribution |
|---|---|---|
| `9acf7a345` | Adds team scope, setup, AI-use record, scripts and empty test/report folders. | Authored and committed by Muhammad Wasay Tariq. AI-use entry describes scaffold assistance. |
| `f933fa467` | Adds roster, initially leaving Rayyan/Zain area choice open. | Wasay authored the document. |
| `4bd2314ed` | Explicitly changes Rayyan to Area 2 and Zain to Area 3. | Direct task-assignment evidence from the diff. |
| `da76b3371` | Adds SE-5B section and member GitHub links. | Wasay authored roster metadata. |

Only these four commits differ from the pinned upstream baseline, affecting **19 files with 401 insertions**. All four include an AI co-author trailer. The tracked application implementations and upstream tests predate these additions. No Rayyan- or Zain-authored post-baseline work is visible in the audited branch. This establishes observable commit attribution, while `TEAM.md` establishes task ownership. Unpushed or separately stored work remains unknown. [E14]

GitHub returned no assignment issues, PR discussion, completed PR or blocked PR to supplement that allocation. Inherited `.github/CODEOWNERS` routes upstream review and does not assign university duties. [E15; `.github/CODEOWNERS`, lines 1-18]

## Section 3. My Personal Responsibilities

### 3.1 Establish the API test basis and endpoint contract

**Meaning and reason.** Determine exactly which HTTP operations support W1/W2, what each input means, and how expected outcomes follow FR-01 through FR-10 and BR-01 through BR-04. The spec must describe real interfaces and document deliberate business assumptions or discrepancies. [E2; E7, page 2]

**Expected functionality.** Review the upstream generated schema, retain it if accurate, or provide a corrected scope-specific OpenAPI document. Cover authentication, request bodies, path/query parameters, file inputs where applicable, role requirements, status/error responses and readback shapes. Verify the chosen version/prefix and schema dialect before implementing its reader. Model balance/date relationships explicitly as documented constraints or justified extensions where plain schema properties cannot express them. Do not invent a fixed allocation maximum from the seed's ten-day leave-type setting. [E8-E11]

**Related files.** Existing `horilla_api/urls.py`, `apps.py`, `api_urls/auth/urls.py`, `api_urls/leave/urls.py`, leave serializers/views, `leave/models.py`, and draft `SCOPE.md`. Proposed output location is `tests/team/generator/openapi.yaml` or an equivalent reviewed JSON artifact. This filename is a planning recommendation.

**Dependencies.** Team agreement on draft rules, working seeded local application and stable endpoint scope. The schema route is `swagger<format>/`, so upstream's own regression test uses `/api/v1/swagger.json/`, including the trailing slash. `README_API_DOCS.md` advertises `/api/swagger.json` without it. Swagger access is public under DEBUG and admin-restricted otherwise. [E2, line 3; `horilla_api/tests/test_api_versioning.py`, lines 28-46; `horilla_api/urls.py`, lines 19-29]

**Expected output.** Reviewed spec, endpoint/input inventory, requirement mappings and recorded assumptions. Explicit Area 2 ownership is at `TEAM.md` line 8 and `tests/team/README.md` line 8.

### 3.2 Build specification-driven EP and three-point BVA generation

**Meaning and reason.** EP groups inputs expected to behave alike. BVA exercises just below, at and just above each genuine boundary. The assignment requires the generator to read OpenAPI and requires API tests to consume the output. A table manually typed into tests would leave this requirement incomplete. [E7, page 2]

**Expected functionality.** Derive valid/invalid classes for the selected endpoints' input types, required/optional fields, nullability, enums, references and documented limits. Generate three-point boundary cases with justified units, such as a day for dates or an agreed half-day step for leave balances. Use valid baseline requests and vary one invalid input per EP case. Dynamic employee IDs, assigned leave types, balances and date windows must be bound to current synthetic fixtures. Unsupported constraints should be reported visibly so coverage gaps can be explained. These are implementation interpretations of the brief, not an assigned requirement to build a general-purpose OpenAPI tool. [E7, page 2; E10-E12]

**Related files.** `tests/team/generator/` currently contains only `.gitkeep`. Proposed additions are a generator script, a generated JSON case dataset and concise usage/constraint notes. API consumers belong in `tests/team/api/`.

**Dependencies.** Accurate spec, input inventory, deterministic fixtures and a defined boundary unit for floating-point day counts. Description is a text field without a finite model maximum, so no arbitrary length boundary should be invented. Optional attachments require file/multipart handling only for accepted scope configurations. [E10, lines 180-193 and 258-270; E11, lines 1403-1408 and 2462]

**Expected output.** Runnable generator and machine-readable cases mapping input, class/boundary, operation and expected outcome. Explicit sources are `TEAM.md` line 8, `tests/team/README.md` line 8 and assignment page 2.

### 3.3 Implement API and integration tests using generated data

**Meaning and reason.** Exercise the running HTTP API and inspect its resulting records. Assertions must prove more than HTTP success. They must confirm correct status, owner, balances and absence of unintended records or changes. [E7, page 2]

**Expected functionality.** Authenticate as the employee and separate approver. Test generated valid and invalid input groups, three-point boundaries, relevant multi-condition decisions, allowed/disallowed transitions and repeated operations. Include unauthorized access and ownership cases that support BR-04, coordinated with Zain's browser checks. For each success or rejection, retrieve the affected request and employee balance and compare persisted results against the starting state. Tests must remain order-independent except for explicitly integrated W1-to-W2 scenarios. [E2; E7, page 2]

**Related files.** Implement under `tests/team/api/`, with shared fixtures/configuration under `tests/team/` if needed. Inspect `EmployeeLeaveRequestGetCreateAPIView`, `LeaveAllocationRequestGetCreateAPIView`, `EmployeeLeaveAllocationGetCreateAPIView`, approval/rejection/cancellation classes, serializers and `AvailableLeave`/`LeaveRequest`/`LeaveAllocationRequest` models. Existing `smoke_api.py` checks only login and balance-list HTTP status. [E5, lines 10-24; E9-E11]

**Dependencies.** Seed/reset behavior, valid dates, API prefix/response contract, generated datasets and normal-user permission setup. A second non-owner employee may be needed for permission/isolation cases. Changes to source after agreed defect triage need regression coverage and coordination with Wasay.

**Expected output.** Team-authored pytest/Requests tests, runnable command, case identifiers, results and a coverage matrix. The brief says “all API coverage criteria” without defining a concrete checklist. An operation/method, input, response, decision, transition, role and shared-state matrix is a proposed interpretation pending confirmation. Explicit sources are `TEAM.md` line 8, `tests/team/README.md` line 9 and assignment page 2.

### 3.4 Prove shared-state integration and repeated-request behavior

**Meaning and reason.** Demonstrate that the five days produced by W1 are the same balance consumed by W2. Test behavior after rejection and repeated requests so duplicate creation, credit or debit cannot be hidden by a response code. [E2, lines 23-42; E7, page 2]

**Expected functionality.** From reset state, allocate five, approve once, read balance five, request three, approve once, read balance two, then submit an independent over-balance request and confirm balance two. Also repeat approval/rejection/cancellation and relevant creation submissions, recording whether the intended contract rejects or safely handles duplicates. The existing create handlers do not expose an idempotency-key contract, so establish intended duplicate identity with the team and record observed weaknesses without claiming unsupported guarantees. [E9, lines 77-101, 271-295, 784-810 and 966-973]

**Related files.** `tests/team/api/` integration scenarios and fixtures, `AvailableLeave` readback endpoints, request detail endpoints and reset scripts. Recovery fault injection remains Zain's documented task, although these fixtures can support it. [E4, line 13]

**Dependencies.** Working W1/W2 APIs, stable requirements, deterministic reset, and an agreed cancellation contract. Expected output is an assertion-backed shared-state sequence and duplicate/state coverage evidence. Sources are `SCOPE.md` sections 2-4 and assignment page 2.

### 3.5 Demonstrate regeneration after two constraint changes

**Meaning and reason.** Prove the generator reacts to the specification and prepare to handle a changed spec in the viva. [E7, pages 2 and 5]

**Expected functionality.** Preserve an initial spec/output, change two genuine documented constraints in a controlled variant, regenerate, show which EP classes/boundary values changed and have API tests consume the regenerated cases. Explain whether a spec-only change intentionally predicts failures against the unchanged server or whether the application rule changed too. A schema edit alone cannot establish a new server behavior.

**Related files.** Proposed `tests/team/generator/` spec variants/output and `docs/team/evidence/` comparison artifacts, with API result references. These artifacts do not yet exist.

**Dependencies.** Completed generator and consuming tests. Expected output is reproducible before/after evidence and an explanation of expected affected tests/gates. Explicit references are `TEAM.md` line 8 and assignment page 2, Automated test data generation.

### 3.6 Supply results, defects and CI integration for Area 2

**Meaning and reason.** Provide evidence others can rerun and integrate into the final report and PR gate. Wasay owns CI implementation, while Rayyan must provide a reliable Area 2 command and result contract. [E1, lines 7-8 and 13; E7, pages 2-3 and 5]

**Expected functionality.** Report tested endpoints, case counts by level, requirement coverage, weaknesses, unresolved failures and limitations. Reproduce candidate defects, then contribute severity, priority, triage, root cause, risk link and fix/retest evidence. Provide commands, dependencies/tool versions and deterministic data setup. Ensure actual test failure exits reach Wasay's gate. No issue creation or external message is part of this audit.

**Related files.** Future Area 2 reports/evidence in `docs/team/reports/` and `docs/team/evidence/`, test documentation, shared traceability and GitHub Issues/PRs. The existing issue template has reproduction/expected/actual fields but no complete SQE severity/priority/triage workflow.

**Dependencies.** Executed tests, shared risk register, agreed defect handling and Wasay's CI. Expected output is an Area 2 report and independently rerunnable suite, integrated into all-test CI. Sources are `TEAM.md` line 13, assignment sections 2 and 6, and `.github/ISSUE_TEMPLATE/bug_report.yml`.

### 3.7 Complete shared and individual academic contributions

**Meaning and reason.** Area ownership is only one component of the brief. Rayyan must contribute to shared management and demonstrate his own understanding and authorship. [E7, pages 2, 5 and 7]

**Expected functionality and output.** Supply a three-point Area 2 estimate and actual effort, API risks and technique/depth rationale, traceability links and coverage counts, defect/RCA evidence, weekly GQM progress, completion/residual-risk assessment and the Area 2 part of the release decision. The group needs at least eight product and two project risks on a 5x5 matrix, at least three measurable exit criteria with two tied to highest risks, and RCA using 5 Whys plus fishbone for at least two major defects, plus Pareto analysis. These are group totals with shared ownership. [E1, line 13; E7, page 2]

Rayyan must also contribute **two use cases**, each with at least two alternative and two exception flows, and ensure every flow has Playwright assertions for displayed result and postconditions. For three members the wording implies at least six member-attributed use cases within the two workflow scope. Exact selection and automation split with Zain remain unresolved. The two workflow usability tests may count toward this total under the brief's page 4 provision. [E7, pages 2 and 4]

**Related files and dependencies.** Shared documents in `docs/team/`, use-case specifications and `tests/team/e2e/`, and `AI_USE_RECORD.md`. Coordinate with Zain on browser tests and Wasay on report/CI integration. Each member must commit their own work, keep prompts, disclose checked AI use and rerun/explain selected tests in the viva. This audit itself should be added to the shared AI-use record during the next authorized documentation update. The existing record was left intact in Phase 1. [E1, line 15; E6; E7, sections 6-7]

## Section 4. Existing Implementation Status

Completed below applies to an inspected documentary or structural deliverable only when that narrower output is actually present. Runnable application behavior remains unverified here.

| Task | Expected Implementation | Current Status | Existing Files | Remaining Work |
|---|---|---|---|---|
| Baseline identification and team area allocation | Exact upstream hash and named area owners | Completed | `SCOPE.md` lines 10-19; `TEAM.md` lines 7-9; baseline object and four team commits | Roll number confirmed as 24I-3000 in Phase 2; confirm final submission suffix. |
| Final scope/test basis | Agreed rules, roles and workflow oracles | Partially Completed | `SCOPE.md` FR/BR tables, explicitly DRAFT | Resolve code differences and verify in running system. |
| Reproducible environment | Working local setup, seed and reset | Needs Verification | `SETUP.md`; inspected seed/reset scripts | Recreate environment later and prove repeatability. Historical “verified” claim is not a current run. |
| Upstream W1/W2 implementation | Existing allocation/request API and shared balance handling | Needs Verification | Leave views/serializers/models and upstream tests | Run team tests and investigate candidate defects below. |
| Team test directory scaffold | Separate area folders and naming basis | Completed | `tests/team/README.md` and seven `.gitkeep` folders | Populate folders in implementation phase. |
| API smoke probe | Authenticate and check balance-list response | Partially Completed | `scripts/team/smoke_api.py` lines 10-24 | Does not assert seed identity/balance, W1/W2, rejection or persisted changes. Runtime result absent. |
| Reviewed OpenAPI for selected endpoints | Accurate fields, constraints, responses and role contract | Not Started | Upstream dynamic Swagger infrastructure exists | Review/export or write scoped spec and contract inventory. |
| EP/BVA generator | Spec reader generating classes and boundary values | Not Started | `tests/team/generator/.gitkeep` | Implement reader, generation and case provenance. |
| Consumed generated datasets | API tests directly use generated cases | Not Started | Empty generator/API folders | Connect output to test parametrization and fixtures. |
| W1/W2 API/integration suite | Generated data, decisions, transitions, rejection, readback and repetition | Not Started | `tests/team/api/.gitkeep` | Implement and execute own tests with result evidence. |
| Two-constraint regeneration | Before/after specs, regenerated cases and effect | Not Started | None | Select valid constraints and capture reproducible comparison. |
| API coverage/results/defect report | Criteria and FR/BR mapping with actual results | Not Started | Evidence/report `.gitkeep` files | Establish coverage interpretation, execute and report. |
| Rayyan's member-attributed browser cases | Two use cases and automated flows | Not Started | `tests/team/e2e/.gitkeep` | Agree case authorship with Zain, specify and automate. |
| Shared management documents | Plan, estimates, risks, criteria, traceability, RCA, monitoring and completion | Not Started | Scope draft and ownership line only | Create actual management documents and maintain them. |
| AI-use record | Checked disclosures and preserved prompts | Partially Completed | Two Wasay entries in `AI_USE_RECORD.md` | Complete their TODO reviews and add later member activity. |
| Area 1 tests, Sonar and mutation | Team unit coverage, MCC/MC/DC, mutation and analysis | Not Started | Unit placeholder and inherited upstream tooling | Wasay must build required team evidence. |
| Area 3 evaluations | Browser, accessibility, security, performance and recovery | Not Started | Empty e2e/security/perf/recovery folders | Zain must implement and execute scoped activities. |
| Team PR quality gate | Every PR runs Sonar, all tests and mutation with enforceable thresholds | Not Started | Inherited `.github/workflows/` | Wasay must target team branch, integrate suite and verify enforcement. |
| Final PDF, Git ZIP and release decision | Full submission with real evidence and `.git` | Not Started | Naming suggestion in `TEAM.md` | Produce after required testing and decisions. |
| Live validation in this audit checkout | Existing environment to execute checks | Blocked | `.env`, `.venv`, DB and snapshot absent | Runtime setup belongs to a later authorized phase. |

No team test execution totals, measured API coverage or pass rate can be reported from this checkout. Upstream tests contain useful reference scenarios but earn no assignment marks. [E4, line 3; E7, page 1]

## Section 5. Missing Work and Implementation Gaps

### Missing Area 2 artifacts and interfaces

The OpenAPI artifact, generator, generated cases, API fixtures, API test modules, test runner configuration, regeneration examples, API traceability and result reports are absent. The root `pyproject.toml` configures linting rather than team pytest discovery. Runtime dependencies include Requests and upstream coverage support, but no team pytest/pytest-django configuration or separate team dependency declaration was found. Select and record only the dependencies the chosen implementation requires. [E4-E5; `requirements.txt`; `pyproject.toml`]

Tests need to discover synthetic record IDs and handle paginated GET responses. `/available-leave/` returns the authenticated employee's own records, not arbitrary employees' balances. Employee-token readback is therefore important after approver actions. The common paginator accepts `page_size` with a maximum of 100. [E9, lines 37-46; E17]

### Source findings requiring execution and triage

The following are **candidate defects or documented mismatches**. None was reproduced through HTTP during this audit. Their eventual severity and risk score require observed impact and team triage.

| Finding | Exact implementation evidence | Implication for Rayyan's tests |
|---|---|---|
| Leave rejection selects the acting approver's balance | `views.py` lines 822-853 queries `AvailableLeave` with the `employee_id` passed from `request.user.employee_get`, while restoring amounts from another employee's leave request. | With current seed, approver has no assigned leave balance, so rejection may error. If an approver balance exists, another person's balance may be credited. Check both balances and request state. This is the most direct shared-state defect candidate. |
| API balance validation differs from model/test basis | Serializer lines 53-55, 93-95 uses uncapped available plus carry-forward. Model lines 2128-2159 rejects non-positive effective days, caps carry-forward and adds forecast. API approval serializer lines 505-511 also uses available plus carry-forward. | Test zero-effective dates and selected cap/forecast configurations. Record which rule is the intended oracle. Current seed with no carry-forward/attachment cannot exercise every documented condition. |
| Employee-specific holiday context differs | API serializer lines 46-51 calls `cal_effective_requested_days` without employee; model lines 2120-2125 supplies employee. Helper lines 1345-1349 filters personal holidays only when employee is supplied. | A leave-type configuration excluding holidays may count another employee's personal holiday. Add a targeted synthetic case if needed to validate scoped holiday rules. |
| Allocation amount has no positive minimum at API level | Create serializer line 259 declares a required FloatField without `min_value`; model lines 2452-2454 has no minimum validator; save lines 2485-2486 delegates directly to super. Approval lines 951-957 adds the value to balance. | Probe zero and negative numeric requests and resulting state. No documented fixed maximum was found. Propose intended amount rule before asserting one. |
| Employee allocation update/delete can dereference missing owner result | `views.py` lines 1158-1171 returns an object only for the owner, with no explicit return/error for a real non-owned allocation. PUT and DELETE then access `.status`. | Use a second employee's record and verify a controlled denial with unchanged state. A server error is plausible from static inspection. |
| Approval credit/debit and request status use separate saves | Allocation approval lines 951-971 and leave approval lines 738-797 contain separate balance/status saves, with no local transaction/row lock. | Sequential repetition is partly guarded by status, while concurrent or interrupted writes need separate verification. Coordinate fault injection with Zain and review surrounding transaction settings before confirming atomicity defects. |
| Cancellation contract in draft is broader than API behavior | Draft BR-03 includes requested-to-cancelled. API `/cancel/` delegates to `request_leave_cancellation`, which requires approved, non-expired leave and only permits one cancellation request. Decision endpoints perform the final refund. | Scope must explicitly choose the allowed state graph. Include pending/denied/repeated/expired cases and use `/cancellation-approve/` or `/cancellation-reject/` as appropriate. |
| Allocation rejection includes an approved-to-rejected path | Draft describes requested-to-approved/rejected. API lines 985-995 reverses approved allocation with a floor of zero; lines 1004-1013 permits rejection unless already rejected. | Define the intended approved-to-rejected behavior, especially after granted days have been consumed. Test exact balance effect against that agreement. |
| Rejection reason is optional in implementation | `reject_reason_from` lines 89-101 accepts only strings, trims and caps at 1000; handlers save it only when non-empty. Draft FR-03 says rejection with a reason. Leave request model's reason maximum is 255. | Clarify mandatory versus optional reason and actual accepted length, then test absent/empty/wrong-type/overlength cases with persisted readback. |
| Generic and employee allocation creation differ | Generic POST lines 271-295 accepts `employee_id`, records creator and returns 201 plus body. Employee POST lines 1141-1152 forces employee identity and returns 200 without object body. | Define which route supports each role. Recover request IDs through scoped GET when necessary and describe distinct responses accurately in OpenAPI. |

Paths `views.py` and serializer/model references in this table refer respectively to `horilla_api/api_views/leave/views.py`, `horilla_api/api_serializers/leave/serializers.py`, and `leave/models.py`.

### Integration and shared-document gaps

The seed provides an employee, approver, admin, company and one zero-balance leave assignment. It deliberately excludes attachment requirements and carry-forward. It does not cover a second employee, explicit permission-holder without manager relationship, attachment-required leave type or cap/forecast scenarios. Extend fixtures only where agreed rules need them. The seed's “idempotent” description means reuse of records, but it resets balance to zero and does not remove pre-existing requests. The full database reset is required to establish the documented no-existing-allocation start condition. [E5, lines 75-107; E2, line 26]

Existing CI triggers target `dev/v2.0` and `2.0`, while this repository uses `sqe-team`. No team Sonar configuration, mutation configuration or all-team-test quality gate was found. No PR evidence was returned. Wasay must address CI; Rayyan should supply the suite command and expected failures. Inherited `.coveragerc`/Makefile floors do not establish the required team 100% statement/branch criterion. [E13-E15; E7, pages 2-3]

Upstream `CONTRIBUTING.md` and the PR template target upstream's `dev/v2.0`. The team has only `sqe-team` visible. The eventual team contribution workflow needs explicit instructions that match its own branch and quality gate. `SETUP.md` also starts from an upstream clone and baseline checkout, which omits team scripts until team changes are present. Improve those reproduction instructions during the authorized implementation phase. [E3, lines 20-26; `.github/PULL_REQUEST_TEMPLATE.md`; E15]

The registration-sheet confirmation remains TODO in `AI_USE_RECORD.md`. Shared test plan, risk register, measurable exit criteria, estimates, traceability, defects/RCA/Pareto, progress and completion documents are missing. An empty report folder establishes a destination only. [E6-E7]

## Section 6. Exact Work Required From Me

The following is dependency-ordered work for a later implementation phase. **Mandatory** refers to the brief, **Repository-specific** to the documented Horilla scope, and **Recommended** to a useful implementation choice.

1. **Repository-specific.** Use confirmed roll number 24I-3000 and review draft FR/BR definitions with Wasay and Zain. Resolve cancellation, allocation reversal, rejection reason and API/model validation differences before treating them as oracles. Confirm repository registration evidence with the team. [E1-E3, E6; user's Phase 2 correction]
2. **Mandatory and Repository-specific.** Reproduce the pinned application with synthetic accounts and demonstrate correct seed/reset behavior. Record actual tool versions and commands. Keep tests on normal employee/approver accounts for rule checks. [E3, E5; E7, page 1]
3. **Mandatory.** Inventory all inputs and operations needed for W1/W2, agree API coverage criteria, derive EP classes, every genuine boundary, decision combinations and transition coverage. Map them to FR/BR IDs. [E2; E7, page 2]
4. **Mandatory.** Review upstream Swagger and reuse it if accurate, otherwise create a scoped OpenAPI contract. Resolve dialect, paths, responses, numeric/date units, optionality and dynamic constraints. [E7, page 2; E8-E11]
5. **Mandatory.** Implement the OpenAPI reader and EP/three-point BVA generator, producing machine-readable cases covering the selected inputs. [E1, E4; E7, page 2]
6. **Mandatory and Repository-specific.** Implement independent authentication/data fixtures and API tests that consume generator output. Assert outcome bodies and persisted request/balance changes, including unchanged state after every relevant rejection. [E5, E9; E7, page 2]
7. **Mandatory.** Complete W1-to-W2 integration, decision tables, all agreed state transitions, at least one invalid transition from each state, ownership/rule rejection and repeated-request/no-duplicate checks. Count each executable API case once. [E2; E7, page 2]
8. **Mandatory.** Reproduce candidate defects, document observed weaknesses and participate in triage/RCA. Coordinate one evidence-backed fix PR and failure-before/pass-after regression with Wasay, without assuming every candidate needs a source change. [E7, pages 2-3 and 5]
9. **Mandatory.** Change two agreed spec constraints, regenerate, show changed classes/boundaries and demonstrate the effect on the consuming suite. Preserve genuine before/after evidence and prepare the live-spec viva explanation. [E7, pages 2 and 5]
10. **Mandatory individual requirement.** Agree Rayyan's two use cases with Zain, write required alternative/exception flows and contribute their automated Playwright assertions/postconditions. Keep their attribution visible. [E7, page 2]
11. **Mandatory shared requirement.** Supply estimates/actual effort, risks, exit criteria input, traceability, defect data, weekly GQM results and completion/residual risk conclusions. Add checked AI disclosure and preserve prompts. [E1, line 13; E7, pages 2, 5 and 7]
12. **Mandatory.** Hand Wasay a deterministic API/generator command and integrate it into every-PR CI. Verify a real failing suite blocks the required gate and supports the group's documented blocked PR. [E1, line 7; E7, page 3]
13. **Mandatory.** Supply Area 2 report/evidence/tool versions for the PDF/ZIP, commit your own work from your account in a later authorized phase and rehearse rerunning/explaining tests and spec changes. [E1, line 15; E7, sections 6-7]
14. **Recommended.** Add small generator regression tests for constraint interpretation and stable case identifiers when implementing it, so the viva's changed spec cannot silently reuse stale cases. This is a correctness check supporting the assigned generator, with no new product feature. [Derived from E7, page 2]

## Section 7. Suggested Implementation Order

All filenames below that are absent today are **proposed locations**, not existing artifacts or additional assignment obligations.

| Step | What to do and likely files | Prerequisites and team dependency | How completion can be verified |
|---|---|---|---|
| 1. Finalize test basis | Review `docs/team/SCOPE.md`, `TEAM.md`; record endpoint/rule decisions and scope coverage. | Correct roster/identifier, registration and agreement with both teammates. | Each FR/BR has a defensible oracle and owner; disputed transitions/limits are resolved explicitly. |
| 2. Establish environment | Follow/refine `SETUP.md`; inspect seed/reset and create only needed synthetic fixtures. | Python/runtime dependencies and local DB. Agree shared initial state with Zain. | Two fresh/reset runs give the same balances/identities, with no stale requests. |
| 3. Define contract and matrix | Review/export Swagger, create `tests/team/generator/openapi.yaml` or JSON; coverage/partition notes under `docs/team/`. | Running app and agreed scope. Wasay's rule targets should use the same definitions. | Every scoped input/method/role/response maps to code and a documented expected result. |
| 4. Implement generator | Add generator/case output under `tests/team/generator/`; optional focused regression checks. | Reviewed contract, schema dialect and boundary units. | For each declared relevant constraint, output contains justified EP classes/BVA values, invalid cases vary one input, and changes are detectable. |
| 5. Build HTTP test foundation | Add test fixtures/configuration and initial W1/W2 tests in `tests/team/api/`; update `tests/team/README.md`. | Authentication, reset/ID discovery and generated datasets. | Clean run authenticates both roles and proves basic grant/consume/readback using generated cases. |
| 6. Finish behavior coverage | Add rejection/decision/state/repetition and non-owner cases in API suite. | Defined oracle and valid baseline scenarios. Coordinate permissions/recovery fixtures with Zain. | Traceability shows relevant inputs/classes/boundaries and required transitions; request and balance readback support every result. |
| 7. Investigate and retest defects | Reports/evidence, risk links, later issues and regression tests; application files only for triaged changes. | Reproduced behavior. Agree fix ownership with Wasay and avoid concurrent edits. | Original assertion fails on old behavior, corrected behavior passes, and retained evidence matches the build. |
| 8. Demonstrate regeneration | Spec variants and output comparison under generator/evidence folders. | Working generator plus consuming suite. Coordinate changed business rule with Wasay if source changes too. | Two constraint changes produce explained dataset differences and predicted test/gate effects. |
| 9. Complete member use cases | Specifications and Rayyan-attributed tests in `tests/team/e2e/`. | Zain's framework/data setup and allocation of six member cases across the two workflows. | Rayyan's two cases each cover main, two alternative and two exception flows with displayed result and postconditions. |
| 10. Integrate CI and finish evidence | API execution docs, reports, shared management/AI record; Wasay edits team workflow. | All suite commands and dependencies stable; shared evidence from Zain. | CI runs Area 2 on a team PR, failure propagates, blocked/fixed PR evidence exists, report cites actual results, and final package is reproducible. |

Steps 9 and shared management can advance alongside API implementation after their prerequisites are agreed. Management records should be maintained throughout, including estimates before execution and actual effort afterward. The sequence does not require Rayyan to complete Wasay's mutation work or Zain's performance evaluation before starting his own API tests. [E1, E7]

## Section 8. Questions and Ambiguities

1. **Personal identifier resolved in Phase 2.** Rayyan explicitly confirmed **24I-3000**. Current roster, submission names and personal contribution metadata must use it. [User's Phase 2 instruction]
2. **Scope approval.** Has the team reviewed and accepted the draft scope? It remains explicitly DRAFT, with outstanding AI-use review TODOs. [E2, line 3; E6, line 8]
3. **Registration.** Was Horilla registered in SE-5B's shared sheet in time, and where is that evidence? The audit did not access the sheet. [E6, line 7; E7, page 1]
4. **API coverage definition.** Does the instructor provide a checklist for “all API coverage criteria” beyond the PDF? The supplied brief uses the phrase without enumerating those criteria. Proposed dimensions in section 3.3 need agreement. [E7, page 2]
5. **Per-member use cases.** Which two use cases belong to Rayyan, and how will authorship/automation be divided with Zain? Area 3 ownership alone does not resolve the per-member wording. [E1, E7]
6. **Contract oracles.** Should the test basis require model-level cap/forecast/positive-effective-day rules at the API, and what is the intended amount/duplicate/reason contract? Source behavior and draft expectations differ. [E2, E9-E12]
7. **Workflow boundaries.** Are cancellation decisions and approved allocation reversal included in the final selected workflows? They are present in code and draft state descriptions, but their exact permitted transitions disagree. [E2, BR-03; E9, lines 867-1014; E12]
8. **Schema dialect and reuse.** Can the upstream generated Swagger describe every selected input/response/constraint accurately? No exported scoped spec or generator choice exists yet. [E8, E10; `horilla_api/schema.py`]
9. **Current environment proof.** Can the historical setup record be reproduced on the present machine? No local project environment/database was available for verification. [E3, line 4]
10. **Unpublished contributions.** Do Rayyan, Wasay or Zain have unpushed branches, separate reports or test results? Current branch history and GitHub search reveal only the scaffold/roster additions. [E14-E15]
11. **CI enforcement.** Which team PR target and branch protection settings will enforce required checks? Inherited workflows target upstream branches, and protection settings were not verified. [E13, E15]
12. **Defect ownership.** Who will implement source fixes after reproduction, and which defect will support the required fixed/blocked PR evidence? No issues or PRs currently establish that plan. [E15; E7, page 3]
13. **Submission suffix.** Should the instructor's section token be `B` or `SE-5B`? `TEAM.md` itself asks for confirmation. [E1, line 17]

### Phase 1 completion check

| Requested check | Audit result |
|---|---|
| Relevant documentation investigated | All team docs/scripts read, upstream product/contribution/API/setup materials reviewed, available assignment PDF read in full, project-document/name searches completed. |
| Assigned source inspected | Leave routes, authentication, views, serializers, models, day/cancellation methods, permissions, pagination and upstream tests reviewed. |
| Team duties separated | Rayyan Area 2, Wasay Area 1 and Zain Area 3 are explicitly supported by `TEAM.md`; shared and per-member duties identified separately. |
| Progress accurately distinguished | Empty team test folders identified as Not Started; inherited code and historical setup claims retained as Needs Verification. |
| Evidence supplied | File/line or section references, exact baseline/HEAD and commit diffs support major conclusions. Static defect candidates are labelled for reproduction. |
| Clarifications exposed | Roll number resolved in Phase 2. Coverage criteria, rule oracles, use-case authorship, registration, CI and submission naming remain visible above. |
| Phase boundary respected | The only deliverable created is this Markdown audit. Implementation awaits the Phase 2 instruction. |

### AI assistance disclosure for this audit

ChatGPT/Codex inspected local files and Git history, queried connected GitHub metadata and the supplied assignment, and drafted this report. The investigation cross-checked assignment duties with `TEAM.md`, route definitions, serializer/model logic and the baseline diff. Runtime outcomes are unverified. Rayyan should review the report's conclusions and record what he checked or changed in the team's AI-use record during the next authorized documentation update, retaining the Phase 1 prompt. [E7, section 7]
