# SQE Phase 2 Implementation Roadmap

Prepared on 22 November 2026 for **Syed Muhammad Rayyan Hassan, 24I-3000**, GitHub `rayyanhasan899`, section SE-5B.

> Execution checkpoint, 23 November 2026: Phase A's previous Linux archive is not
> available in the laptop checkout. Phase B has a source-reconstructed contract,
> generator and initial consumer, with independent regression results recorded
> in [its status report](reports/SQE_IMPLEMENTATION_PHASE_B_STATUS.md). HTTP,
> environment/schema verification and complete input coverage remain blocked or
> incomplete. This checkpoint does not change the historical planning findings
> below or authorize starting C/D before the current B acceptance conditions pass.

## 1. Decision and execution order

Rayyan owns **Area 2**, API/integration testing, OpenAPI and automated EP/three-point BVA data generation with regeneration. Four implementation phases are justified because the contract must precede generation, generated cases must precede the full consuming suite, and regeneration requires a working suite. His individual use cases, shared management contributions and viva evidence are included. Wasay retains Area 1 and CI ownership. Zain retains Area 3 coordination and its specialist evaluations.

| Order | Ready-to-use prompt | Purpose | Required evidence before the next prompt |
|---|---|---|---|
| 1 | [SQE_IMPLEMENTATION_PHASE_A.md](SQE_IMPLEMENTATION_PHASE_A.md) | Establish reproducible isolated setup, resolve test-basis decisions, review/write the scoped API contract and plan coverage. | Actual environment checks, reviewed spec, endpoint/input inventory, documented oracle decisions and A status report. |
| 2 | [SQE_IMPLEMENTATION_PHASE_B.md](SQE_IMPLEMENTATION_PHASE_B.md) | Implement the spec-driven generator and a small HTTP consumer proving its output is used. | Generator verification, deterministic output/provenance, real consumed HTTP cases and B status report. |
| 3 | [SQE_IMPLEMENTATION_PHASE_C.md](SQE_IMPLEMENTATION_PHASE_C.md) | Complete API/integration coverage, state/repetition/readback checks and defect reproduction/regression. | Coverage accounting, clean-run results, genuine defect evidence and C status report. |
| 4 | [SQE_IMPLEMENTATION_PHASE_D.md](SQE_IMPLEMENTATION_PHASE_D.md) | Demonstrate two-constraint regeneration, complete Rayyan's browser cases and Area 2 reporting, verify available CI integration and prepare the viva handoff. | Before/after generation evidence, consuming tests, personal use-case results, completion report and explicit external dependencies. |

Enter the entire **Phase A prompt first**, when starting the implementation stage. Execute B only after checking A's actual outputs, C after B, and D after C. Executing a prompt does not establish that its completion conditions passed. Each prompt instructs Codex to check prior reports, inspect actual files and rerun relevant checks. A defect can be carried forward as a recorded failing test when it does not invalidate independent work. An unresolved oracle, unavailable database or other concrete dependency blocks only the work that depends on it.

These are future implementation prompts. Their creation does not start them. This planning turn created five planning documents and corrected Rayyan's roll number in `TEAM.md` and the Phase 1 audit. No application implementation, dependency installation, commit or push was performed.

## 2. Authoritative sources and current evidence

| Reference | Source | Authority and locator |
|---|---|---|
| B1 | Official **SQE_Final_Project Fall 2026(1).pdf**, seven pages | Assignment obligations. Sections 1-7, rubric on page 6. Read completely for this plan. [Open brief](https://chatgpt.com/library?file_id=libfile_7ca0240df8688191b399f878fa329e4b&account_id=personal) |
| B2 | `docs/team/TEAM.md` | Named ownership, lines 7-9; shared work, line 13; own commits, line 15; naming, line 17. Rayyan's roll number corrected from the user's explicit instruction. |
| B3 | `docs/team/SCOPE.md` | DRAFT warning, lines 3-4; W1/W2/shared records, lines 23-42; FR-01 to FR-10, lines 48-57; BR-01 to BR-04, lines 63-66; roles/assumptions, lines 70-81. |
| B4 | `docs/team/SQE_PHASE_1_PERSONAL_AUDIT.md` | Sections 3-8, responsibility detail, status, candidate defects and unresolved interpretations. Read as an evidence-based audit, with current code rechecked. |
| B5 | `tests/team/README.md`, `scripts/team/seed_team.py`, `reset.ps1`, `smoke_api.py`, `docs/team/SETUP.md` | Area folders, existing synthetic accounts/data, reset behavior and setup commands. |
| B6 | `horilla_api/api_urls/leave/urls.py`, lines 9-55; `horilla_api/apps.py`, lines 22-38; `horilla_api/urls.py`, lines 9-29 | Endpoints, versioned/legacy API mounts and generated Swagger. |
| B7 | `horilla_api/api_serializers/leave/serializers.py`, lines 12-102, 180-215, 258-291, 418-454, 490-514 | Actual input/validation/response contract. |
| B8 | `horilla_api/api_views/leave/views.py`, particularly lines 37-155, 232-348, 729-1014, 1107-1194 | Authentication-dependent workflows, approvals, rejection, cancellation and readback. |
| B9 | `leave/models.py`, lines 157-173, 732-772, 1376-1446, 1980-2000, 2046-2209, 2445-2494; `leave/methods.py`, lines 13-30, 208-310 | Persisted models, dates, effective balances and cancellation state machine. |
| B10 | `.github/workflows/unit-tests.yml`, `quality.yml`, lines 6-11; `docs/team/AI_USE_RECORD.md`, lines 3-8 | Inherited branch filters and unfinished project records. |

The upstream baseline is `6c15617b8297b7a6775daa6c29aefcc48b1eb29f` (Horilla 2.4.0). Local `sqe-team` HEAD is `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0`. The GitHub branch was queried again for this plan and matched. The four post-baseline commits contain scaffold/docs/roster work by Wasay, with no team API/generator implementation. Phase 1's GitHub searches found no issues or PRs. Those search results describe that audit's observation date and should be refreshed during implementation if needed. [B4, contribution table]

No extra implementation plan or handoff was discovered beyond the Phase 1 report and these new planning documents. `tests/team/api/` and `generator/` contain only `.gitkeep`. `.venv`, `.env`, local DB and seed snapshot were absent during the audit. Runtime findings remain unverified. The existing product, upstream tests, schema infrastructure, seed/reset and smoke scripts should be reused where correct. [B4-B5]

## 3. Assignment extraction and ownership boundary

### Functional scope

The brief requires selecting two related workflows in one web MIS, with a value written by one and used by the other. The repository chooses W1 leave allocation and W2 leave consumption. The shared record is `AvailableLeave` for employee plus leave type. The draft has ten requirements, four for W1 and six for W2, satisfying the numeric requirement of at least eight overall and three per workflow, subject to validation of their meaning. [B1, page 1; B3]

| Draft requirements | Required behavior to verify | Rayyan's contribution |
|---|---|---|
| FR-01 through FR-04 | Create allocation, approve to credit days, reject pending allocation without credit, edit only while pending. | API request/response and persisted-state tests with generated inputs. |
| FR-05 through FR-07 | Create leave, reject excessive effective duration, prevent active-date overlap. | Input classes/boundaries and multi-condition validation checks. |
| FR-08 through FR-10 | Approve to debit, reject/refund according to agreed rules, read updated balance. | Role-aware transition and shared-record readback tests. |
| BR-01 through BR-04 | Limit, Boolean decision, state change and authorization. | Spec/test-basis constraints, relevant decision combinations and allowed/invalid transitions, ownership/permission assertions. |

The assignment does not prescribe those HR features itself. Their details come from B3 and must be reconciled with B7-B9. It also does not require Rayyan to build a new HR backend.

### Mandatory quality, technical and submission requirements

| Assignment obligation | Scope and owner | Consequence for Rayyan's plan |
|---|---|---|
| Usable browser, HTTP API, persistent data, source, upstream URL/licence/hash, synthetic local data and reset, repository registration within five days | Shared system/scope, brief page 1 | A verifies reproducibility and records missing registration evidence without claiming it exists. ERPNext example is ineligible. |
| EP on every valid/invalid input group, one invalid value per EP test; BVA just below/at/above each real limit | Area 2, page 2 | A inventories every input, B generates classes/values, C executes all applicable cases. Unbounded fields/enums receive EP and explicit BVA applicability notes. |
| Decision combinations for every scoped rule with two or more conditions; all allowed transitions and one disallowed transition from each state | Cross-level functional duty, page 2 | A defines matrices, C covers applicable API combinations/transitions, with unreachable combinations justified. Wasay retains MCC/MC/DC unit work. |
| Rejections, repeated requests without duplicates, shared-record readback after success/rejection and endpoint weaknesses | Area 2, page 2 | C checks actual records and balances, including duplicate credit/debit and creation behavior. |
| OpenAPI, own generator read from spec, API suite uses output, two changed constraints and regeneration, live updated spec | Area 2, pages 2 and 5 | A contract, B generator/consumer, D two-change evidence and viva rehearsal. |
| 100% statement and branch coverage of scoped server business logic, defend uncovered code, all four rules, complete MCC and MC/DC on critical module | Wasay Area 1, page 2 | Share oracles/defect cases with Wasay. Rayyan's API coverage matrix does not establish this code coverage. |
| Sonar complexity, duplication, smells, bugs, vulnerabilities, coverage, debt and ratings, plus manual CFG complexity comparison | Wasay Area 1, page 2 | Rayyan supplies relevant weaknesses/changes and reuses resulting risk evidence. |
| Mutation score, at least two business-rule custom operators, analysis of at least 15 survivors and killing killable survivors | Wasay Area 1, page 3 | D hands over API/generator execution contract and relevant regression cases. |
| Every-PR Sonar/all tests/mutation, justified gates, blocked merge/deploy, no failure suppression, one fixed PR and one blocked PR | Wasay CI owner and group evidence, page 3 | Rayyan provides meaningful nonzero exit commands and regression evidence. D validates integration if available and records pending group enforcement separately. |
| Two use cases per member, each with at least two alternatives and two exceptions, all flows automated in Playwright with result/postcondition assertions | Personal obligation, Area 3 coordination by Zain, page 2 | A proposes Rayyan's two cases, D implements his attributed flows in Zain's framework or minimal compatible scoped setup if absent. Six member-attributed cases are implied for this group. |
| Two automated workflow usability tasks, one correction-after-error, keyboard order/submission, Lighthouse accessibility/best-practices/SEO plus full axe on key screens, deduplicate findings, one screen fix and before/after tools/reports | Zain Area 3, page 4 | Rayyan coordinates his browser cases and shared data. The specialist assessment remains Zain's responsibility. |
| Two-role access matrix, at least four automated decisions with allow/deny, passive ZAP, at least two corroborated controls, versioned dependency audit | Zain Area 3, page 4 | C's API role assertions support shared evidence. They do not replace the required browser/security assessments. Only local synthetic-data activity. |
| Predeclared p95/failure targets, k6 one VU and at least five VUs, each twice for at least 60 measured seconds after target users reached, same machine/build/start data, p95/RPS/failure results | Zain Area 3, page 5 | Share API operations and clean fixtures. The brief's example 500 ms/1% is illustrative, so Zain must justify actual targets. |
| Controlled state-changing failure/recovery, inspect persisted state, restore/retry with no duplicates | Zain Area 3, page 5 | Share fixtures/readback and defects. Rayyan retains normal repetition tests, while fault injection/recovery ownership stays with Zain. |
| Plan, risk-driven approach, roles/environment/data/schedule, entry/exit/suspend/resume criteria, three-point area estimates versus actuals | Shared, page 2 | A records honest estimates/management contributions; C/D update actual work and evidence. |
| At least eight product/two project risks, likelihood and impact 1-5, 5x5 matrix, risk-depth mapping; three measurable exit criteria, two tied to highest risks | Shared group totals, page 2 | Rayyan supplies API risks, measures and justified targets. Maintain shared records, with pending teammate-owned inputs labelled. |
| Traceability, GitHub defect severity/priority/status/triage, RCA for two major defects using 5 Whys and fishbone with corrective/preventive actions, Pareto | Shared, page 2 | C supplies reproduced API defect entries, D completes available RCA/contribution and links. Never invent two major defects to meet a count. |
| Weekly plan/control/GQM metrics, defect density, requirements coverage, reopen rate; completion/deviations/open defects/residual risk/release decision | Shared, page 2 | Record real dated progress, defined denominators and unavailable data. D supplies Area 2 completion section. |
| One PDF plus repository ZIP including `.git`, public link, all test/tool/evidence/ownership/management records, actual versus target for three release criteria | Shared, page 5 | D supplies a validated Area 2 evidence index and corrected naming. Full group packaging follows integration of all areas. |
| Each member commits own work; explain/rerun tests and changed spec/rule in viva; disclosed checked AI use and retained prompts; free/open-source tools | Individual/shared, pages 5 and 7 | Every phase records honest activity and checked outputs. Commits and external posting occur only with authorization when implementation is executed. |

### Marking scheme

These are group rubric components, not a promised individual mark allocation. [B1, page 6]

| Component | Marks | Primary relationship to Rayyan |
|---|---|---|
| System and scope | 5 | Shared scope/reproduction evidence |
| Static analysis and metrics | 5 | Wasay |
| Test plan, estimation and traceability | 7 | Shared, with Area 2 contributions |
| Risk register and exit criteria | 5 | Shared |
| White-box unit testing | 16 | Wasay |
| API and integration testing | 10 | Rayyan primary |
| Automated test data generation | 7 | Rayyan primary |
| Use case specification | 3 | Personal two cases, coordinated with Zain |
| Use case automation | 6 | Personal flow contributions, coordinated with Zain |
| Mutation and CI | 8 | Wasay primary, Area 2 integration input |
| Usability/accessibility | 5 | Zain |
| Defensive security | 6 | Zain |
| Performance/recovery | 5 | Zain |
| Defect management/RCA | 7 | Shared |
| Monitoring/completion | 5 | Shared |
| Viva/live task/AI-use | 20 | Individual accountability across components |
| **Total** | **120** | Component marks may be reduced in viva if unexplained. |

## 4. Requirement-to-implementation mapping

IDs here are planning references. Preserve existing FR/BR IDs and add case/flow IDs as needed.

| Assignment Requirement | My Responsibility | Required Implementation | Existing Status | Remaining Work |
|---|---|---|---|---|
| R1, scope and local synthetic reset, p1 | Shared foundation for Area 2 | Reproducible test DB/server lifecycle, identity/record discovery and source-based oracles | Partially Completed, scripts/docs exist, runtime unverified | A verify isolated setup twice, improve team-clone commands and data notes. |
| R2, accurate OpenAPI, p2 | Explicit Area 2 | Scope-specific reviewed schema, inputs/responses/constraints/roles | Not Started, dynamic Swagger exists | A inspect/reuse or write contract and schema validation. |
| R3, EP on all selected inputs, p2 | Explicit Area 2 | Valid/invalid classes, omission/null/type/enums/reference and relational cases where relevant | Not Started | A inventory; B generate; C execute each applicable group. |
| R4, three-point BVA, p2 | Explicit Area 2 | Below/at/above real numeric/date/length/collection limits with units | Not Started | B generate and C bind runtime limits, including effective balance/date relationships. |
| R5, own generator consumed by API tests, p2 | Explicit Area 2 | Spec reader, case output, provenance, parametrized HTTP consumer | Not Started | B implement and prove actual consumption; C expand across scoped inputs. |
| R6, decisions and state coverage, p2 | Area 2 contribution to functional techniques | Rule combination matrix and API transition tests | Not Started, draft state list only | A agree graph/oracle, C exercise all allowed and invalid-per-state changes. |
| R7, rejection/repetition/readback, p2 | Explicit Area 2 | Assert status/error and persisted ownership/counts/balances after success/rejection/repetition | Not Started, smoke checks only status | C W1-to-W2 and negative/state/repetition suites. |
| R8, report API weaknesses, pp2/5 | Area 2 plus shared defects | Reproducers, risk/severity/root cause/fix links and retest | Needs Verification, static candidates in audit | C reproduce, minimally fix established in-scope bugs or report blocked fix; D evidence index. |
| R9, two constraint changes/regeneration, p2 | Explicit Area 2 | Baseline/changed specs and output diff, consuming-test effects | Not Started | D perform controlled experiment and restore baseline. |
| R10, two use cases/member, p2 | Personal, Zain coordinates | Two cases, each main plus 2 alternatives and 2 exceptions, Playwright results/postconditions | Not Started | A propose real case allocations; D implement missing Rayyan flows. |
| R11, every-PR all-tests gate, p3 | CI producer/consumer contract, Wasay owns gate | Repeatable commands, nonzero failures, artifacts, evidence of execution/enforcement | Not Started, upstream branch filters differ | C runner/result contract; D integrate if access exists, otherwise report concrete Wasay dependency. |
| R12, shared plan/estimate/risks/exit/traceability, p2 | Shared | Area 2 estimate, risks, techniques/depth, real case links and criteria | Not Started beyond draft scope | A initialize contribution and proposed criteria; C/D update evidence and actual effort. |
| R13, defects/RCA/Pareto, p2 | Shared | Verified entries, lifecycle/triage and RCA contribution | Not Started | C/D populate from actual findings, retain group shortfalls visibly. |
| R14, weekly GQM and completion, p2 | Shared | Dated progress, defined metrics, actual/target, residual risk and release/hold section | Not Started | Each phase records actual work; D completes current Area 2 conclusion. |
| R15, package/evidence/tool versions, p5 | Area 2 contribution to shared package | Runnable spec/generator/tests, reports, evidence paths and corrected roll | Partially Completed, baseline/setup docs only | D inventory and handoff; group PDF/ZIP pending all-area evidence. |
| R16, own commits/viva/AI, pp5/7 | Individual | Checked disclosures/prompts, explainable tests/spec changes, own-account commit history | Partially Completed, existing AI record has Wasay entries | Each phase records AI use; D rehearsal; personal commits remain pending until authorized. |

## 5. Gaps, conflicts and working decisions

| Issue | Evidence | Handling in prompts |
|---|---|---|
| Roll number corrected | User explicitly confirmed 24I-3000; old metadata was incorrect | Correct all current project-document occurrences and filenames. Commit history remains historical evidence. |
| API model and draft balance rules differ | Serializer lines 53-55/93-95 versus model lines 2128-2159 | A records behavior and expected contract separately. Use justified assumptions permitted by brief; obtain clarification only where business meaning cannot be established. Do not redefine a defect as expected behavior solely to pass. |
| Draft cancellation graph includes a requested-to-cancelled path while API requires approved leave and manager decision | B3 BR-03; B8 lines 867-938; B9 methods 208-310 | A resolves API graph, including cancelled/rejected states and repeated/expired cancellation. C covers agreed allowed/invalid paths. |
| Approved allocation can be rejected and debited | B8 lines 985-1013, broader than draft | Record and decide intended reversal behavior, including previously consumed allocation. |
| Rejection appears to select approver's balance | B8 lines 822-853 | C reproduce with distinct employee/approver data, inspect both balances and status. Minimal fix only after established expected behavior and failing test. |
| No positive allocation bound found, reason length/optionality differs, employee-allocation wrong-owner result may fall through | B4 section 5 and B7-B9 | A inventory real constraints. C reproduce targeted findings. The seed's total_days=10 does not establish a maximum allocation request. |
| “All API coverage criteria” lacks enumerated dimensions | Brief p2 | Proposed checklist covers operation/method, request/response, input classes/boundaries, decisions/transitions, roles and shared-state. Record it as interpretation and adopt any instructor checklist later. |
| Upstream schema generated through drf-yasg, new generator needs explicit dialect | B6, schema route `/api/v1/swagger.json/` | Reuse accurate spec in its dialect when practical. Default for a new scoped artifact is OpenAPI 3.0.3, documenting conversion/reconciliation. Supporting every OpenAPI dialect is outside scope. |
| Per-member use cases versus Zain ownership | Brief p2 and B2 line 9 | Rayyan supplies two attributed cases/flows within existing workflows. Reuse Zain's framework and coordinate selection. Missing framework permits minimal compatible personal tests, not transfer of Zain's assessments. |
| Inherited CI runs on upstream branches | B10, current branch sqe-team | Wasay's integration dependency, with Rayyan's command/artifacts supplied. No unrequested branch restructuring. |
| Runtime data absent and reset script overwrites default DB | B4-B5 | A creates isolated disposable test data and verifies paths. Reuse seed logic without deleting an existing unverified user DB. Use HTTP Requests to a live Django test server, with setup/readback assistance isolated to test fixtures. |
| Registration proof, section suffix, group reports and thresholds missing | B2/B10 | Record pending evidence and owners. Continue independent Area 2 work. Preserve `_B` as current proposed naming and flag suffix confirmation. |

The recommended test foundation is pytest with Requests against an actual local Django test server using an isolated test database. Use existing pytest-django infrastructure if a teammate adds it. If absent, introduce only the minimum scoped configuration and dependencies needed. Test-target operations must traverse real HTTP authentication/routes/serializers/persistence. ORM calls may prepare independent data and corroborate readback, while assertions about user-visible outcomes should retrieve through the appropriate role's API. Avoid a new public “test reset” application endpoint.

Generation is scoped to actual selected input constraints. Include body, path, relevant query and authentication input handling, with clear distinction between generated data fields and test-harness headers. Dynamically bound constraints, such as available balance and relative dates, need explicit machine-readable scenario bindings in or alongside the spec, documented as team extensions. BVA does not require arbitrary boundaries for unbounded strings or enums. Case identity/provenance must survive regeneration while stale cases are detectable.

## 6. Phase definitions and acceptance conditions

### Phase A. Foundation, test basis and contract

**Objective.** Make the selected workflows reproducible and define what the generator/tests must verify before implementing them. Covers R1-R4 planning, R6 planning, R10 specification and R12/R16 contributions.

**Tasks.** Inspect current state and prior audit; establish isolated environment and record actual versions; verify seed/reset and employee/approver authentication/readback; inventory methods/fields/media/roles/responses; reconcile scope conflicts with references/justified assumptions; reuse/review or create scoped OpenAPI; define EP/BVA/decision/state coverage and two personal use-case specifications; record Area 2 estimates/risks and AI review.

**Likely files.** Existing `docs/team/SCOPE.md`, `SETUP.md`, `tests/team/README.md`, shared AI record. Proposed `docs/team/AREA2_TEST_BASIS.md`, `API_COVERAGE_MATRIX.md`, `RAYYAN_USE_CASES.md`, `AREA2_MANAGEMENT.md`, `tests/team/generator/openapi.yaml`, minimal `tests/team/requirements-area2.txt` and scoped fixtures/settings if needed. Reuse teammate equivalents in place of duplicate documents.

**Dependencies.** Runtime/dependency access and local synthetic DB, source-derived rules, registration/section confirmation as group follow-ups. Outputs include source-backed contract, fixture/lifecycle instructions, comprehensive input matrix and proposed per-member use cases.

**Verification and completion.** Demonstrate two clean environment runs with identical logical initial state and no stale requests, validate schema and every selected operation against routing/serializers, confirm distinct normal roles, and record every unresolved decision with dependent cases. Write `docs/team/reports/SQE_IMPLEMENTATION_PHASE_A_STATUS.md` with actual checks. A can finish independent outputs while a specific disputed oracle is blocked, but B must not claim those cases implemented until resolved.

### Phase B. Generator and first consuming HTTP tests

**Objective.** Implement real spec-driven generation and prove the API consumer uses it. Covers R3-R5 implementation and R12/R16 updates.

**Tasks.** Revalidate A; implement supported-dialect spec reader and references; produce valid/invalid EP classes and justified three-point boundaries; bind real fixtures/dates without hardcoded database IDs; include deterministic case IDs, source constraints/hash and expected predicates; test the generator against relevant nested/referenced/required/enum/range cases; add minimal parametrized Requests tests and prove case lineage.

**Likely files.** `tests/team/generator/generate.py`, generated JSON and focused generator tests, `tests/team/api/` initial consumer, scoped fixture/config additions, `tests/team/README.md`, coverage/management/AI updates. Exact names may follow newer repository conventions.

**Dependencies.** A contract and isolated environment. Output is a runnable generator plus generated case artifact and a real HTTP consuming slice, not the full C suite.

**Verification and completion.** Same spec/bindings/seed yields equivalent ordered cases apart from explicitly excluded run metadata; one-invalid-input EP cases remain otherwise valid; true below/at/above values respect inclusive/exclusive bounds; unsupported constraints are visible; the minimal consumer traverses HTTP and checks persistence. Record `SQE_IMPLEMENTATION_PHASE_B_STATUS.md` and failures honestly. An implementation defect surfaced by a valid case is evidence, with dependent cases tracked.

### Phase C. Complete API/integration and defect verification

**Objective.** Meet Area 2 functional coverage with independent results and regression evidence. Covers R3-R8, R11 producer command and R12-R14 contributions.

**Tasks.** Revalidate A/B; expand generated consumption across scoped inputs; exercise each decision/transition including invalid-per-state; prove 0-to-5-to-2 shared balance and an independent over-balance rejection leaving 2; test repeated creations/actions and denied roles; inspect persisted records after every relevant success/rejection; reproduce audit candidates and triage; add targeted minimal source fixes only where an existing rule establishes correct behavior; rerun impacted checks; define reliable runner/results for Wasay; update traceability and real findings.

**Likely files.** `tests/team/api/`, generator bindings/fixtures where coverage reveals gaps, `docs/team/API_COVERAGE_MATRIX.md`, reports/evidence and management records. `horilla_api/api_views/leave/views.py` or the existing serializer/model code may need a small defect correction after reproduction, while preserving unrelated behavior. Source fixes are conditional future implementation work.

**Dependencies.** B's consuming harness and all affected oracle decisions. Wasay coordinates shared rule fixes/CI; Zain reuses fixtures/records for security/recovery. Outputs include actual results, complete case ledger, defect reproducers and readback evidence.

**Verification and completion.** Run from fresh data twice and establish order independence; compare counts and balances; confirm generated provenance and finite coverage denominators; count each executable case once at API level even if it covers several techniques; preserve unexpected failures. Do not turn product defects into passing tests, unconditional skips or generic expected failures. Write `SQE_IMPLEMENTATION_PHASE_C_STATUS.md` with covered/missing/failed/blocked criteria and local test command.

### Phase D. Regeneration, personal browser flows and completion evidence

**Objective.** Demonstrate adaptive generation and finalize Rayyan's reproducible contribution. Covers R9-R16 and verifies R1-R8 outputs.

**Tasks.** Revalidate A-C; change two actual contract constraints in a documented variant and regenerate; show generator/input class/BVA/test effects, keeping baseline intact; complete Rayyan's two browser cases and every specified flow; reuse Zain's framework or add only a small compatible scoped setup; integrate/verify Area 2 runner with available Wasay CI, preserving ownership; consolidate actual versions/results, weakness/risk/fix/RCA data, estimates, GQM and residual-risk/hold recommendation; provide evidence inventory and live-spec viva steps.

**Likely files.** Generator variant spec/data/diff under `tests/team/generator/` and `docs/team/evidence/area2/`, Rayyan-attributed tests under `tests/team/e2e/`, `RAYYAN_USE_CASES.md`, `AREA2_CI_HANDOFF.md`, `docs/team/reports/AREA2_COMPLETION_REPORT.md`, shared management/AI records and D status. Edit existing CI only for scoped Area 2 wiring where authorized by the executed prompt and compatible with Wasay's configuration. Full Sonar/mutation gate remains Wasay's deliverable.

**Dependencies.** C suite, a runnable browser application, Zain's test interfaces if present and Wasay's CI/access for remote enforcement. Output includes genuine regeneration and browser evidence plus final Area 2 handoff.

**Verification and completion.** Demonstrate baseline and variant cases consumed by the same API runner with the chosen spec/data; a spec-only change may produce predicted server mismatch and must be described honestly; restore baseline after experiment. Run all Rayyan browser flows with displayed outcomes and record postconditions. Check evidence paths, actual/target criteria, reproducible commands, CI exit propagation and open dependencies. Write D status. Report local Area 2 readiness separately from group integration/release readiness. Missing remote protection/teammate evidence remains Pending or Blocked, with no false group completion claim.

## 7. Evidence contracts between phases

Each status report must identify phase, date, confirmed member/roll, inspected HEAD and uncommitted diff, requirement IDs, actual created/modified files, exact commands/versions, exit/results and evidence paths, failures/skips/blocked work, assumptions and named dependencies, estimates/actual effort where knowable, next phase readiness, and checks required before continuation. Record unavailable effort history as unavailable. Never backfill fictional weekly reports.

Every phase updates shared AI disclosure with tool/purpose/output and checks actually performed. Prompt files are retained. Codex may describe its own verification, but must not claim Rayyan personally reviewed or executed something he has not done. Every phase preserves teammates' work and inspects current status before editing. A later phase may finish a small prerequisite within its assigned scope, but may not silently declare the prior phase successful.

Generated case artifacts should include operation and method, input location/name, requirement/rule references, EP/BVA label, concrete value or dynamic binding, otherwise valid baseline, expected predicate, constraint source and spec fingerprint. HTTP results should carry case ID and spec/data fingerprint so regeneration can be traced. This representation is a recommended implementation design, not a new requirement to build a large test-management platform.

## 8. Final coverage review and unresolved dependencies

| Review question | Planned coverage |
|---|---|
| All explicit Area 2 duties included? | A contract/basis, B generator, C HTTP integration and D regeneration/evidence. |
| Every relevant assignment technique included? | EP/BVA, rule decisions, full agreed transition graph, invalid transitions, repeated calls and persisted readback in A-C. |
| Personal duties included? | Two use-case specifications in A, every Playwright flow in D, shared records and AI/viva evidence throughout. |
| Another member's area transferred? | Wasay retains Sonar/unit/MCC/MC/DC/mutation/gate. Zain retains broad browser/evaluation/security/performance/recovery coordination. |
| Existing work reused? | Upstream application/schema, current seed/reset concepts, teammate framework/configuration and stable FR/BR IDs. |
| No invented feature or threshold? | No new HR feature, artificial allocation maximum, invented performance target or assumption of passing results. Proposed criteria need rationale and group agreement. |
| Phase order and handoffs consistent? | A reports basis/spec, B consumes it, C extends consumer, D consumes suite and demonstrates change. All read prior files and rerun checks. |
| Submission requirements covered within role? | D evidence/tool/version/ownership/result inventory and Area 2 release contribution, with group PDF/ZIP/CI/registration dependencies explicit. |

Outstanding user/team decisions are limited to rules whose oracle cannot be justified, instructor-specific API coverage criteria if any, final per-member use-case allocation, registration evidence, final section suffix and any defect fix that extends beyond selected modules. Use reversible documented interpretations when the brief permits them and continue independent work. Rayyan's roll number is resolved as **24I-3000**.

The full submission remains dependent on Wasay's Area 1 and CI evidence, Zain's Area 3 results, actual own-account commits, shared records and the final PDF/ZIP. Creating or executing the personal prompts alone cannot establish all-group completion. The first implementation prompt is **SQE_IMPLEMENTATION_PHASE_A.md**.

## 9. Planning verification and AI disclosure

ChatGPT/Codex read the supplied seven-page official brief, the Phase 1 audit and relevant current repository documentation, refreshed the source review for API contracts/known conflicts and confirmed GitHub branch HEAD. It created this roadmap and four prompts, and corrected the confirmed roll number in current team/audit documentation. Checks confirmed that each prompt includes context, objective, requirements, investigation, implementation instructions, restrictions, testing and completion reporting; all five files use 24I-3000; Markdown tables are structurally consistent; and the working tree contains documentation changes only. Application behavior, proposed commands and future test results were not executed in this planning phase. Rayyan's personal review remains pending.
