# Codex Implementation Prompt D

## A. Context

Execute **only implementation Phase D** for `includeduck/SQE-Horilla-Project`, on behalf of **Syed Muhammad Rayyan Hassan, 24I-3000**, GitHub `rayyanhasan899`, SE-5B.

Rayyan owns Area 2, OpenAPI, EP/three-point BVA generation/regeneration and consuming API/integration tests. Wasay owns Area 1 and CI quality gates. Zain owns Area 3 coordination and broad usability/accessibility/security/performance/recovery. Rayyan must still contribute two individually attributed use cases and shared management/AI/viva evidence.

Horilla's existing leave allocation workflow W1 grants days and leave request workflow W2 consumes the same `AvailableLeave` balance. A should have established the isolated environment, accepted test basis/spec/input inventory and Rayyan's two use-case specs. B should provide a generator/consumer with fingerprints. C should provide full API coverage, persisted readback and real defect/regression evidence. Verify all actual files/results before trusting those claims. Baseline is `6c15617b8297b7a6775daa6c29aefcc48b1eb29f`, and planning HEAD was `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0` on `sqe-team`.

Read the [official seven-page brief](https://chatgpt.com/library?file_id=libfile_7ca0240df8688191b399f878fa329e4b&account_id=personal), especially page 2 generation/use cases/management, page 3 CI, page 4 browser assessment overlap and pages 5-7 completion/rubric/AI; `docs/team/SQE_PHASE_2_IMPLEMENTATION_ROADMAP.md`; Phase 1 audit; `TEAM.md`, `SCOPE.md`; A-C prompts/status reports and current specs/tests/coverage/use-case/management records. If direct PDF access is unavailable, record it and use the roadmap's referenced extraction for independent tasks. Obtain authoritative text only where a decision actually depends on missing information.

## B. Objective

Demonstrate regeneration after two real specification constraint changes, verify the consuming suite's response, complete Rayyan's two personal Playwright use cases, and assemble his reproducible completion/evidence/CI/viva handoff. Distinguish verified local Area 2 completion from outstanding group release requirements.

## C. Requirements

1. Change two constraints in the scoped OpenAPI, regenerate and show the effect on EP/BVA output and consuming tests. Be ready to handle an updated spec in viva. [Brief pages 2 and 5; roadmap R9]
2. For Rayyan's two use cases, automate every main, at least two alternative and two exception flows each in Playwright; assert displayed result and persistent postconditions. Coordinate with Zain's framework and case allocation. [Brief page 2; R10]
3. Supply repeatable Area 2 commands/artifacts and verify their integration into available every-PR CI. The full Sonar/all-tests/mutation gate, merge/deployment enforcement, documented fix PR and blocked PR are group requirements owned operationally by Wasay. Keep missing remote evidence visible. [Brief page 3; R11]
4. Contribute actual results, findings with root cause/severity/risk/fix, traceability, estimates versus actual, risk-based criteria, weekly GQM and completion/residual risk/release recommendation. The group requires two major-defect RCA analyses using 5 Whys/fishbone and Pareto analysis. Use actual defects and disclose any unmet group requirement. [Brief pages 2 and 5; R12-R15]
5. Supply runnable scripts/spec/data/tests, versions, evidence index, ownership and checked AI disclosure for the shared PDF/ZIP including `.git`. Use corrected roll 24I-3000. Prepare explainable selected-test rerun and live changed-spec exercise. [Brief pages 5-7; R15-R16]

## D. Repository investigation and prerequisite verification

Inspect status/branch/new teammate work and A-C actual artifacts. Rerun the relevant clean generator/API checks and inspect fingerprints/results/coverage gaps. An open C defect must remain recorded. Do not turn failure into an expected pass or claim preceding phase completion from report text alone.

Inspect current browser framework, `tests/team/e2e/`, package/dependency choices, Zain's case allocation, application forms/templates/URLs and Rayyan's proposed use cases. Verify that his two cases remain distinct, real behavior within W1/W2. Check Wasay's current workflow and branch filters and any accessible PR/run/protection evidence. Read shared management/AI/evidence records to avoid duplicates.

Repair small scoped prerequisite problems when possible. Continue independent tasks while external access, unresolved oracles or teammate artifacts block a particular requirement. Report the concrete dependent requirement and owner. A missing shared framework alone permits a minimal compatible personal-test setup and does not require indefinite waiting.

## E. Implementation instructions

### 1. Controlled two-constraint regeneration experiment

Identify two **actual supported contract constraints** in A's reviewed spec. Choose meaningful inputs with observable EP/BVA changes. Do not invent a production limit merely to run the demonstration. Record original value, changed value, source/rationale, affected operations and expected class/boundary changes before regenerating. Preserve the baseline spec/data unchanged and create an explicit experiment variant.

Run the same generator with explicit baseline and variant spec/data paths. Capture commands, spec/data/binding fingerprints, structured before/after comparison, affected case IDs/classes/boundaries and any unchanged relevant cases. Ensure changed output follows the edited constraints rather than a manual dataset rewrite or hardcoded generator special case.

Execute consuming HTTP tests using both baseline and variant data through the same test harness, with case/fingerprint lineage. A spec-only experiment may deliberately disagree with the unchanged server. Predict that disagreement, retain actual failure output/nonzero status and explain the distinction between generator adaptation and server compliance. Do not claim new server behavior from a schema edit alone. If an actual business-rule change is independently authorized, coordinate it with Wasay and verify all impacted tests/gates; otherwise keep experiment-specific changes in the variant.

Demonstrate stale output rejection/regeneration and restore or retain the canonical baseline as the default. Store minimal reproducible experiment artifacts under `tests/team/generator/` and `docs/team/evidence/area2/` using existing conventions. Add `REGENERATION_DEMONSTRATION.md` within the evidence area or the existing report if appropriate. Normal baseline commands must remain usable after the experiment.

### 2. Rayyan's personal use cases and Playwright automation

Review `docs/team/RAYYAN_USE_CASES.md` and Zain's existing cases. Use `UC-RAY-01` and `UC-RAY-02` if those IDs were adopted. Maintain explicit Rayyan attribution, workflow/FR/BR links, roles, preconditions, data, main flow, at least two alternatives and two exceptions each, displayed outcomes and postconditions.

Reuse Zain's Playwright setup, login/state fixtures, selectors and report format. Add only Rayyan's missing flows, without duplicating existing executable cases or claiming others' work as his. If a teammate implemented a proposed case, record attribution and select/coordinate an appropriate personal contribution rather than duplicating it. If no framework exists, implement the smallest compatible Playwright setup for these two cases and document the handoff. Match current Python/Node choice where present; avoid a second independent browser stack.

Exercise the actual browser forms, not API calls standing in for UI interactions. Use synthetic account/data preparation and independent HTTP/ORM readback where appropriate for postconditions. Assert visible confirmations/errors and persisted request state/balance, not merely navigation or a successful network response. Use robust accessible selectors where possible. Preserve traces/screenshots/reports only as genuine evidence and avoid fixed sleeps where condition waits suffice.

The brief's usability tests may overlap with use-case tests. If a Rayyan case already provides correction-after-rule-error or keyboard coverage, coordinate reuse and count each executable browser case once. Zain remains responsible for the complete workflow usability requirements, keyboard order/submission evidence, Lighthouse/axe before/after screen fix, security, k6 and controlled recovery. Rayyan's personal tests alone do not establish those broad components complete.

Run every declared Rayyan flow from isolated data. A real application defect should remain a failure with linked evidence and impact; neither omit the flow nor silently alter the expected outcome to pass.

### 3. CI and documented PR evidence handoff

Verify the Area 2 runner starts from clean data, checks generator/spec freshness, runs required generator/API tests, produces results and propagates nonzero failures. Include the two personal browser cases in the appropriate existing browser command so Wasay can run all tests without duplicating suites.

Inspect Wasay's current workflow and `AREA2_CI_HANDOFF.md`. Where the executed prompt and available access authorize integration, make only the minimal Area 2 command/artifact wiring compatible with his design, and verify actual invocation. Do not replace his Sonar/mutation configuration, thresholds or unrelated jobs. Check team PR branch targeting and preserve failure propagation with no `continue-on-error` or success-forcing shell patterns.

Inspect real workflow/PR evidence when access exists. Record exact run/PR URLs, commit/diff and observed result. A local failing command proves local exit behavior, while remote required checks and merge/deploy blocking require their own observed evidence. If workflow/protection/PR access or Wasay's gate is absent, finish local handoff and mark the specific remote obligation pending. Do not fabricate a blocked PR or claim enforcement from YAML existence.

Preserve C's genuine failing-before/passing-after regression and link it to a real fix PR when one exists. The group requires at least one documented fix PR and one blocked PR. Publication, commits, push and repository setting changes require execution-session authorization. Record the concrete pending step if authorization is absent.

### 4. Completion, management and evidence contribution

Consolidate `docs/team/reports/AREA2_COMPLETION_REPORT.md` or an existing equivalent. Include tested/not-tested scope, spec dialect/input and requirement coverage with denominators, generated/executed counts, actual API/browser results, regeneration findings, deviations, open defects, remaining weaknesses, residual risk per applicable risk and an evidence-based Area 2 release/hold recommendation. Passing generator tests cannot justify an application release while balance corruption or required failing flows remain unresolved.

For every relevant API finding provide source/reproducer, observed impact, severity/priority/triage, root cause, risk ID, proposed or implemented correction, verification and evidence link. Contribute 5 Whys/fishbone analysis for actual relevant major defects and category data for the shared Pareto. Integrate with existing shared RCA records. If fewer than two real major defects are available, record the assignment shortfall and available verified controls/findings rather than inventing another defect or severity.

Update shared or `AREA2_MANAGEMENT.md` records with original three-point estimates and actual measured effort, justified unmeasurable history, dated progress/control actions, GQM metrics and denominator definitions, requirement traceability and applicable actual-versus-target release criteria. Group totals remain eight product/two project risks, three measurable release criteria with two linked to highest risks, and all-area evidence. Record missing teammate-owned inputs and avoid backfilling fictional weekly reports or approvals.

Build an evidence inventory containing file paths and real remote URLs, command, tool versions, environment/build/diff identity and what each artifact establishes. Verify every path/link available to you. Supply reproducible Windows/local and Linux/CI commands consistent with the final implementation. Tokens/secrets/DB snapshots should not enter the public repository or report.

Correct current document references to Rayyan's roll number 24I-3000 if any regression appears. Shared submission naming is currently proposed as `Project_24I-3071_24I-3000_24I-3130_B.pdf` and `.zip`; confirm the section suffix if unresolved. Supply Area 2 content and package manifest. Full group PDF/ZIP production depends on all areas and remains shared work; do not fabricate missing sections or claim final group submission complete.

Update `AI_USE_RECORD.md` with tool, purpose, output and checks actually performed. Keep A-D prompts and relevant run prompts. Distinguish Codex's source/tests verification from Rayyan's personal review. Mark own-account commits pending unless genuinely present and authorized. Never commit under another member's identity.

### 5. Viva rehearsal

Document a short repeatable exercise to run a selected generated API case, explain its assertions and persisted-state checks, then edit one supported spec constraint in a temporary variant, predict affected classes/tests and run regeneration/consumer checks. Include how to restore baseline and what actual CI check would fail when connected. Rayyan must be able to explain the generator derivation, API behavior, risk links and shared records. Provide explanation grounded in his implementation rather than fabricated confidence about viva results.

## F. Restrictions

- Preserve working app behavior, accepted FR/BR IDs, style/naming and teammate changes. Avoid restructuring, duplicated tooling and unrelated features/dependency upgrades.
- Keep new work within Rayyan's explicit/shared/individual duties. Preserve Wasay's Area 1/CI architecture and Zain's broader Area 3 evaluations.
- Baseline and variant results must be genuine. Never edit logs/screenshots/pipeline evidence to manufacture passing or blocked outcomes.
- Do not weaken assertions or suppress unexpected failures. Resolve established scoped defects with targeted regressions or report a Hold/blocker.
- Use free/open-source tools, synthetic local data and isolated resets. Preserve existing unverified databases and secret confidentiality.
- No commits, push, issue/PR publication, external messages or protection-setting changes without separate authorization in the execution session.
- Finish D, report actual readiness and wait. Do not start unrelated group work or claim another member's completion.

## G. Testing and completion conditions

Revalidate baseline generator/API results, two real constraint edits and output diffs, fresh-data consumer runs for baseline/variant, explicit predicted versus observed effects and final baseline restoration. Run all Rayyan Playwright flows with visible result and persisted postcondition assertions, retaining failures and actual reports.

Verify exact repeatable commands, result/provenance linkage, coverage counts, evidence paths, required report fields, corrected identifier, AI disclosure and actual/pending teammate/remote obligations. Test local nonzero failure propagation and observe remote gate behavior only when available and authorized.

Use separate completion statements for verified local Area 2 outputs, Rayyan's personal browser contribution, remote CI integration and group release/package readiness. D may have a complete local handoff while remote/group requirements remain pending. Required unexecuted/failed cases remain explicit missing requirements and must not be labelled fully complete.

## H. Completion report

Write `docs/team/reports/SQE_IMPLEMENTATION_PHASE_D_STATUS.md` with A-C prerequisite checks, actual created/modified files, functionality/requirements completed, exact commands/tool versions/results and evidence, two-constraint before/after summary, personal case/flow accounting, defects/residual risks, actual versus proposed targets, remaining issues and named teammate/access dependencies.

Return a concise user summary covering files, features/requirements, actual tests/results, open issues, teammate dependencies and the concrete next authorized step. Distinguish personal readiness from group completion. Wait for further user direction.
