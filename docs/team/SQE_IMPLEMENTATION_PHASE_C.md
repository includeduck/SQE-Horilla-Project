# Codex Implementation Prompt C

## A. Context

Execute **only implementation Phase C** for `includeduck/SQE-Horilla-Project`, on behalf of **Syed Muhammad Rayyan Hassan, 24I-3000**, GitHub `rayyanhasan899`, SE-5B.

Rayyan owns Area 2, API/integration tests, OpenAPI and generated EP/three-point BVA data with regeneration. Wasay retains Area 1, Sonar/unit coverage/MCC/MC/DC/mutation and CI gate ownership. Zain retains Area 3 coordination and usability/accessibility/security/performance/recovery. Shared management and Rayyan's two personal use cases remain part of his contribution.

Horilla already implements leave workflows. W1 allocates days and W2 consumes them from `AvailableLeave(employee_id, leave_type_id)`. A created the isolated environment, reviewed API spec/test basis and coverage plan. B should have implemented a spec reader/generator, freshness/provenance and a minimal real HTTP consumer. C must inspect those outputs and extend them into the full Area 2 suite. The baseline is `6c15617b8297b7a6775daa6c29aefcc48b1eb29f`; planning HEAD was `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0`. Recheck current code and preserve teammate work.

Read the [official seven-page brief](https://chatgpt.com/library?file_id=libfile_7ca0240df8688191b399f878fa329e4b&account_id=personal), especially page 2 API/techniques, page 3 CI and page 5 findings/submission; `docs/team/SQE_PHASE_2_IMPLEMENTATION_ROADMAP.md`; Phase 1 audit; `TEAM.md`, `SCOPE.md`; A/B prompts and actual status reports; current Area 2 basis, coverage matrices, spec/generated data and test instructions. If the PDF is unavailable, record that limitation and use the roadmap's page-referenced requirements for independent work, requesting missing authoritative text only where needed.

## B. Objective

Complete generated-data-driven API and integration coverage for both workflows. Prove persisted-state correctness after success/rejection/repetition, reproduce endpoint weaknesses and implement narrowly justified regressions/fixes. Supply a reliable Area 2 test command and evidence for Wasay's CI and the shared report.

## C. Requirements

1. Execute every identified valid/invalid EP group for scoped inputs, with one invalid value per EP case. Execute below/at/above every applicable real limit using generated values and actual runtime bindings. [Brief page 2; roadmap R3-R5]
2. For every scoped multi-condition rule, list condition combinations and cover their outcomes, justifying infeasible combinations. Exercise all agreed allowed state changes and at least one disallowed change from each state. [Brief page 2; R6]
3. Include rule rejection, authorization/ownership, invalid transitions, repeated requests with no duplicate records/credit/debit and readback after success/rejection. [Brief page 2; R7]
4. Demonstrate the connected W1/W2 sequence, with allocation adding five days, approved leave consuming three and a separate three-day request rejected with balance staying two. Ensure dates are non-overlapping so balance causes the intended rejection. [Draft scope W1/W2; R7]
5. Use the actual generated data in HTTP tests. Preserve case/spec provenance, explicit expected assertions and count each executable case once at API level, even when it covers several techniques. [Brief page 2]
6. Report endpoint weaknesses with genuine evidence, root cause, severity, risk and correction linked to shared records. Contribute to GitHub defect/RCA/Pareto obligations without inventing findings or remote artifacts. [Brief pages 2 and 5; R8/R13]
7. Supply an exact repeatable fail-propagating test command for all-tests PR CI. Wasay owns the overall gate; Rayyan owns the Area 2 producer contract and regression evidence. [Brief page 3; R11]
8. Update traceability, risks, progress/GQM, actual effort when knowable and AI-use records. [Brief pages 2 and 7; R12-R14/R16]

## D. Repository investigation and prior-phase verification

Inspect Git status, current tests/specs and all A/B status evidence. Rerun schema/generator tests and a consuming HTTP smoke slice from isolated starting data. Verify data fingerprints and that the server and fixtures use the same database. If reports claim success while actual tests fail, report current facts and repair the prerequisite within scope if possible. Do not assume missing reports mean no code exists.

Inspect current leave routes, API views/serializers, authentication and permission decorators, models, methods, fixture/settings lifecycle and any teammate integration changes. Use upstream tests to understand prior regressions, while writing team cases independently. Preserve FR/BR mappings and accepted A oracle decisions. If scope conflicts remain, resolve through evidence or justified assumptions and ask only for material unresolved meaning. Continue independent tests while dependent ones are blocked.

Audit candidates requiring targeted review include the following.

- `horilla_api/api_views/leave/views.py`, lines 822-853 at planning commit, appears to select the acting approver's balance for rejection refunds.
- `horilla_api/api_serializers/leave/serializers.py`, lines 53-55/93-95, differs from `leave/models.py`, lines 2128-2159, on positive effective days, capped carry-forward and forecast.
- API holiday calculations may omit employee-specific context; zero/negative allocation requests have no visible positive validator; employee allocation detail lookup may return no object for another owner's record.
- Allocation approval and leave approval separately save balances and status; consider surrounding transaction settings before claiming atomicity defects. Zain owns controlled recovery fault injection.
- Cancellation requires an approved unexpired request, a manager decision and only one cancellation attempt, while draft state descriptions differ. Approved allocation reversal and optional rejection reason/length also need the agreed oracle.

All line references must be re-located against current files. None of these static findings is a reproduced result by itself.

## E. Implementation instructions

### 1. Extend the existing consuming suite

Use `tests/team/api/` and B's generator/fixtures rather than a second harness. Keep Requests calls against the actual local Django server with JWT, roles and normal application serialization/persistence. ORM setup or independent corroboration may be used inside test fixtures, while target operations and expected user-visible record readback traverse HTTP.

Cover all selected body/path/query inputs, authentication handling, omission/null/type, enum/format/reference classes and genuine limits. For valid cases, assert exact relevant payload fields, identity, effective days/status and balance changes. For invalid cases, assert the expected rejection class/reason and unchanged persisted requests/balances. Account for actual response shapes, empty success bodies, pagination and distinct generic/self-service status codes established in A. Avoid accepting a wide range of statuses that hides wrong behavior.

Ensure generated cases are consumed in parametrized tests and map back to spec/bindings. Add generator capabilities only where an actual scoped input gap requires them; retain B's interface and provenance. Unsupported relevant constraints remain visible incomplete coverage. Unbounded fields get no invented BVA maximum.

Use separate synthetic employee, approver and non-owner data when required. A setup administrator must not execute tests intended to verify normal-role rule restrictions. Keep fixtures isolated per case or restore baseline between scenarios. Avoid repeatedly overwriting a shared live SQLite file or using ordered-test assumptions.

### 2. Cross-workflow and shared-record assertions

Implement a clear integrated scenario beginning at zero, creating/approving allocation five, reading balance five, creating/approving three effective days, reading two, and rejecting an independent non-overlapping three-day request while confirming balance two and no rejected-create artifact unless the accepted contract persists one.

For every success/rejection/repetition, read back the affected record(s), owner, counts and employee balance, including carry-forward where relevant. Verify both employee and approver balances in refund tests so cross-user corruption is observable. Correlate dynamically created record IDs rather than assuming primary keys. Treat validation rejection separately from a saved request whose status becomes rejected.

### 3. Decisions, transitions and repetition

Implement the agreed decision matrix across assignment, date ordering, matching breakdown, required attachment, overlap, sufficient balance and authorization where applicable. Cover outcomes for each condition combination and document infeasible rows with reasons. EP isolation rules apply to EP tests; a deliberate multi-condition decision row may vary multiple conditions and must be labelled accordingly.

Implement the accepted state graph for allocation and leave, including requested, approved, rejected, cancel_requested and cancelled where scoped. Include valid edit/delete paths if scoped and invalid state changes from each state. Do not weaken terminal-state assertions to match a suspected defect without an oracle decision.

Repeat selected creation and state-changing requests. Confirm no duplicate balance effects or duplicate logical records according to the defined identity. Sequential status guards do not prove concurrency correctness. Keep concurrent/recovery claims limited to tests actually executed and coordinate fault injection with Zain. Missing idempotency support should be reported against the brief's no-duplicates expectation instead of silently excluding repetition.

### 4. Defect reproduction, minimal correction and regression

Reproduce candidate defects using independently isolated data. Capture the pre-state, HTTP operation/response, persisted post-state, build/diff identity and exact failing assertion. Classify static suspicion, reproduced finding and corrected/retested finding separately.

When the intended outcome is established by existing requirements/documentation or accepted A assumptions, implement the smallest correction in the existing selected API/model/service logic and add the regression. Reuse existing permission/balance/cancellation helpers where they preserve callers' behavior. Handle retries/partial saves consistently where the reproduced bug requires it. Preserve unrelated workflows and run impacted existing regression tests in addition to team tests, reporting their results separately.

If a correction would change an unresolved business contract, require unrelated module ownership or introduce new feature semantics, report the precise decision/dependency and continue independent work. Do not mask defects by changing expected outcomes, suppressing failures, broad exception handling, unconditional skip or generic expected-failure markers. An open product defect can leave a genuine failing test and a Hold recommendation.

Use existing shared defect records. If absent, keep structured entries in `docs/team/reports/AREA2_DEFECTS.md` or the existing Area 2 report, including reproducer, expected/observed, severity, priority, status, triage, risk ID, root-cause evidence, proposed/corrective/preventive action and retest. Prepare issue-ready text and real links when available. Do not post externally without execution-session authorization. Preserve evidence for the group's one fails-before/passes-after PR; do not fabricate that a local fix is a published PR.

### 5. Coverage and CI handoff

Update `docs/team/API_COVERAGE_MATRIX.md` using actual case IDs/results and explicit denominators for scoped methods/inputs/classes/boundaries/decision rows/transitions/roles/requirements. Count executable API cases once. A case may link to multiple criteria, while code coverage remains Wasay's measurement. Report missing/blocked/not-applicable coverage separately from passing coverage.

Provide one reproducible command or scoped runner that validates spec/data freshness, runs generator checks and the Area 2 API suite, exits nonzero for failure and writes machine-readable results such as JUnit plus a concise manifest. Reuse project conventions and avoid redundant wrappers. Record dependencies, environment, server/DB startup/teardown and artifact locations for Linux CI as well as local execution.

Use `docs/team/AREA2_CI_HANDOFF.md` if no equivalent exists. State how Wasay wires the command into the team PR target and how failure propagation is tested. Do not replace Sonar/mutation/gate configuration or assume that upstream branch filters cover `sqe-team`.

### 6. Shared progress and disclosure

Update the actual shared risk/traceability/progress documents or Rayyan's contribution record. Include true dated progress/control actions and GQM values with denominator definitions. Requirements coverage is not a test pass rate. Defect density needs a defined size measure, and reopen rate needs a defined count/population. Use unavailable/N/A when evidence is absent, not invented zeros. Preserve group RCA/Pareto needs for Phase D and teammate contributions. Update AI disclosure with checks actually performed and any pending human review.

## F. Restrictions

- Preserve existing working functionality, stable requirement IDs, API compatibility, naming/style and teammate changes.
- Reuse existing logic and tests/tooling where appropriate; avoid restructuring, unrelated features, broad dependency upgrades and duplicated frameworks.
- Source changes are limited to evidence-backed in-scope defect corrections. New business requirements require clarification.
- Leave Wasay's Sonar/white-box/mutation/gate and Zain's specialist evaluations/recovery with their owners. Provide shared data/interfaces instead of reassigning work.
- Use synthetic local disposable data and free/open-source tools. Protect existing unverified DBs and secrets.
- No commit, push, published issue/PR or external message without separate authorization. Keep own-account commit and remote PR evidence pending when absent.
- Execute only C. Do not start D automatically.

## G. Testing and completion conditions

Run generator checks and the full API suite from a clean state twice, demonstrating reset consistency and independent-case order where applicable. Inspect both response and persisted records, failure paths, balances, counts and role isolation. Run affected upstream regression checks after fixes, separating those totals from team results.

Verify the coverage ledger against every agreed FR/BR and selected input/state. Record successful, failed, skipped, missing and blocked cases with reasons. A skipped or failed case does not satisfy the required coverage assertion. Preserve output fingerprints and genuine failing-before/passing-after evidence where available.

C completes only the verified scope it claims. Open defects or external integration may remain explicitly pending, with dependent D work identified. Repair recoverable local problems and continue independent authorized tests before returning a blocker.

## H. Completion report

Write `docs/team/reports/SQE_IMPLEMENTATION_PHASE_C_STATUS.md` with current HEAD/diff, A/B revalidation, created/modified files, tests/features/requirements implemented, exact commands/tool versions, actual test counts/results, coverage denominators, case/spec provenance, defect/fix evidence, unresolved oracles/issues, remaining work and named dependencies on Wasay/Zain/access.

Return a concise self-contained summary. Identify **SQE_IMPLEMENTATION_PHASE_D.md** as the next prompt with its actual prerequisites and any independent portions that can proceed while specific dependencies remain blocked. Wait for the user.
