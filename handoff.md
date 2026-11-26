Rayyan will no longer do any further project implementation, testing, integration, documentation, packaging or follow-up execution work. Rayyan's project execution assignment is finished. Every remaining project execution item in the final handoff is now assigned to Muhammad Wasay Tariq / Wasay's agent, and its completion is mandatory for the project. No further technical execution or additional prompt is expected from Rayyan.

# Definitive execution handoff —25 November 2026

**Rayyan assignment CLOSED. Whole-project release HOLD.** Completed contribution:3,433 API cases in each isolated sharded order,713 generated IDs including former399,350 families,10 FR/4 BR explicit assertion sets,10 browser flows and controlled consuming regeneration. [Closeout](docs/team/reports/RAYYAN_FINAL_CLOSEOUT.md), [evidence index](docs/team/AREA2_EVIDENCE_INDEX.md), [PR8](https://github.com/includeduck/SQE-Horilla-Project/pull/8). No future project execution is assigned to Rayyan.

The current backlog below replaces the older handoff, archived at docs/team/history/handoff-before-final-closeout.md. Incomplete requirements remain OPEN and transferred; they are not passes or Wasay acceptance. The mandatory current executor for EVERY row is **Wasay / Wasay's agent — mandatory**. Original authorship remains unchanged.

## F4-REVIEW —P1 —C-D

Original owner: Wasay / repository owner. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: FR-01..FR-10; BR-01..BR-04; PR #8; Issues #14..#31. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Independently review the delivered corrections and contribution, merge only after actual required checks/reviews permit it, and close the 18 proposed-fix product Issues only when warranted.

Actual attempts:

- Published source/fixes and full before/after evidence under rayyanhasan899
- Reconciled all 22 Area 2 defect identities; original four accepted Issues closed, remaining 18 kept open

Why still open: No independent review exists in the accessible PR reviews collection; protected integration cannot be replaced by this agent approving its own contribution.

Next owner action: Independently review the ready PR #8's actual final diff, source-bound evidence and required checks; resolve owner concerns, then perform protected merge/retest and factual Issue lifecycle updates.

Dependency: No independent review exists in the accessible PR reviews collection; protected integration cannot be replaced by this agent approving its own contribution. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Actual independent accepted review + permitted merged commit + actual post-integration checks and warranted Issue states.

Evidence/files: [source](https://github.com/includeduck/SQE-Horilla-Project/pull/8); `docs/team/finish-line/PROMPT03_DEFECT_POPULATION.json`.

## F4-SONAR —P1 —D / Area 1

Original owner: Wasay / Area 1. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Shared CI gate; BR-01..BR-04. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Provide a reachable configured Sonar service/token, run an actual scan of the final implementation and enforce the supplied proposed new-code quality conditions.

Actual attempts:

- Read actual Sonar 26.10 baseline/profile/threshold proposal and raw metrics
- Attempted localhost service and Docker/WSL alternatives
- Implemented exact-revision live server gate, nonempty conditions and no-weaker-than-proposed threshold checks; missing evidence fails

Why still open: The local service refused connection; Docker Linux engine is unavailable and WSL reports access denied. Live CI returned a concrete missing SONAR_HOST_URL/SONAR_TOKEN refusal. Historical Sonar baseline is genuine but is not a current-source CI gate.

Next owner action: Configure SONAR_HOST_URL and SONAR_TOKEN for the existing free service, scan the exact reviewed source using sonar-project.properties, configure the actual proposed conditions and rerun sonar + team-gate.

Dependency: The local service refused connection; Docker Linux engine is unavailable and WSL reports access denied. Live CI returned a concrete missing SONAR_HOST_URL/SONAR_TOKEN refusal. Historical Sonar baseline is genuine but is not a current-source CI gate. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Live analysis revision equals reviewed source; gate OK with explicit duplication <=3%, reliability/security A and zero new blocker/high conditions; immutable raw server responses retained.

Evidence/files: `.github/workflows/team-quality-gate.yml`; `scripts/team/final_quality_gate.py`; [source](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45633245200); `docs/team/reports/SONARQUBE_BASELINE.md`.

## F4-MUTATION —P1 —D / Area 1

Original owner: Wasay / Area 1. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: BR-01..BR-04; Mutation and CI brief section 2. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Supply and execute the actual business-rule mutation runner, two implemented custom operators, >=15 genuine baseline survivor analyses, kill the killable survivors and justify the mutation threshold from actual results.

Actual attempts:

- Audited full tracked tree for mutation tooling and reports
- Implemented a fail-closed invocation/metadata/raw-hash/score/operator/survivor-analysis contract; demonstrated missing-input failure

Why still open: No mutation runner, policy, custom operators or results are present in the published repository; mutation threshold was explicitly deferred in the supplied Sonar report. Those measured results and specialist inputs cannot be invented.

Next owner action: Implement scripts/team/run_mutation.py with --source and --output, add docs/team/mutation_policy.json with measured minimum_score and justification, produce the required raw/hash/source/analysis schema and run the mutation CI job.

Dependency: No mutation runner, policy, custom operators or results are present in the published repository; mutation threshold was explicitly deferred in the supplied Sonar report. Those measured results and specialist inputs cannot be invented. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Actual mutmut/Cosmic Ray outputs on reviewed source; two business-rule operators; >=15 unique analysed baseline survivors; all killable survivors killed; measured justified score passes strict gate.

Evidence/files: `scripts/team/final_quality_gate.py`; `.github/workflows/team-quality-gate.yml`; [source](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45633245200).

## F4-GATE-ADMIN —P1 —D / shared

Original owner: Wasay / repository administrator. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Every-PR CI; Required merge/deployment checks. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Require the actual team-gate check and independent review on sqe-team and enforce equivalent deployment prerequisites; align mandatory producers with every-PR triggering.

Actual attempts:

- Inspected branch/ref/ruleset/workflow and review metadata
- Added every-PR team unit/Sonar/mutation aggregate with exact-source Area 2/browser/contract dependencies
- Retained real red producer/aggregate evidence without claiming remote merge blocking

Why still open: Classic protection access returned HTTP 403 to the integration. An empty ruleset response is not proof of absent protection. Deployment policy/target and administrative authority are not supplied.

Next owner action: As repository administrator, inspect actual protection, require observed team-gate and review conditions, ensure all required producers run or have a legitimate exact-source reuse policy on each PR, and enforce deploy gating; demonstrate blocked and corrected PR outcomes.

Dependency: Classic protection access returned HTTP 403 to the integration. An empty ruleset response is not proof of absent protection. Deployment policy/target and administrative authority are not supplied. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Actual settings and remote blocked merge/deployment evidence, then a genuine successful corrected gate; no continue-on-error, forced exits or self-approval.

Evidence/files: `.github/workflows/team-quality-gate.yml`; `docs/team/AREA2_CI_HANDOFF.md`; [source](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45633245200).

## F4-A1-FINDINGS —P2 —Area 1 / shared

Original owner: Wasay / Area 1. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Issues #11/#12/#13; BR-01/BR-02; Unit scope. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Resolve the three inherited Area 1 findings and reconcile final unit scope/justified gaps and Sonar findings against the accepted final source.

Actual attempts:

- Ran all supplied 127 team units and the existing 15-function feasible coverage gate
- Preserved real known-behavior reproducers/justified gaps and separated them from the clean HTTP input results
- Did not count Area 1 records in the 22-defect Area 2 Pareto

Why still open: These remain actual open Area 1 records: direct model clean with nullable end date, dead month/year code, and invalid stored carry policy. HTTP date normalization and valid choice constraints must be distinguished from a new model-policy decision; no stronger policy or owner triage is invented.

Next owner action: Triage #11-#13 by actual model/form/API reachability; apply source-backed accepted fixes or documented dispositions, adjust justified gaps/critical MCC tables as warranted and retest affected scopes.

Dependency: These remain actual open Area 1 records: direct model clean with nullable end date, dead month/year code, and invalid stored carry policy. HTTP date normalization and valid choice constraints must be distinguished from a new model-policy decision; no stronger policy or owner triage is invented. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Actual accepted dispositions or strict before/after corrections, accurate current 100%-scope argument and source-bound unit/Sonar evidence; no hidden new uncovered business logic.

Evidence/files: [source](https://github.com/includeduck/SQE-Horilla-Project/issues/11); [source](https://github.com/includeduck/SQE-Horilla-Project/issues/12); [source](https://github.com/includeduck/SQE-Horilla-Project/issues/13); `tests/team/unit/coverage_scope.py`.

## F4-MEMBER-USECASES —P1 —D / shared Area 3

Original owner: Wasay and Zain / their member-attributed contributions. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Two use cases per member; W1/W2. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Supply the other members' genuine attributed use-case specifications and Playwright flow evidence; retain Rayyan's two cases and ten verified flows.

Actual attempts:

- Audited tests/team/e2e and use-case documents; completed and reverified Rayyan's two cases/ten flows

Why still open: The accessible e2e collection contains only the ten Rayyan flows. No authentic other-member use-case/flow contributions are supplied; authorship or their review cannot be fabricated.

Next owner action: Coordinate the remaining member-attributed cases and automate each main/at least two alternative/two exception flows with visible and persisted assertions.

Dependency: The accessible e2e collection contains only the ten Rayyan flows. No authentic other-member use-case/flow contributions are supplied; authorship or their review cannot be fabricated. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: At least two genuine cases per member across the agreed workflows, all required flows automated and attributed with actual reports and commits.

Evidence/files: `docs/team/RAYYAN_USE_CASES.md`; `tests/team/e2e/test_rayyan_use_cases.py`; [source](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45627793417).

## F4-ACCESSIBILITY —P1 —Area 3

Original owner: Zain / Area 3, coordinated by Wasay. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Both workflow screens; Accessibility/usability brief section 3. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Supply keyboard task assertions, Lighthouse and full axe-core scans, deduplicate findings and demonstrate one screen correction with actual before/after reports.

Actual attempts:

- Inspected published tests/evidence and preserved the ten passing Rayyan browser flows as completed work

Why still open: No Lighthouse/axe scripts or reports and no Area 3 usability contribution are present in the tracked tree. Rayyan's ordinary visible/persisted flow assertions do not establish these distinct measurements.

Next owner action: Run both workflow tasks including the required correction and keyboard path; scan key screens with Lighthouse and axe, fix one screen and rerun both.

Dependency: No Lighthouse/axe scripts or reports and no Area 3 usability contribution are present in the tracked tree. Rayyan's ordinary visible/persisted flow assertions do not establish these distinct measurements. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Actual scripts, focus/keyboard assertions, issue impact/fix records and original before/after Lighthouse/axe/Playwright reports.

Evidence/files: `tests/team/e2e`; `docs/team/TEAM.md`.

## F4-SECURITY —P1 —Area 3

Original owner: Zain / Area 3, coordinated by Wasay. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: BR-04; W1/W2; Defensive security brief section 4. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Supply the browser access matrix/checks, passive ZAP evidence, at least two corroborated security controls and scoped dependency audit.

Actual attempts:

- Completed API self/manager/permission/nonowner assertions with unchanged-state checks
- Inspected existing upstream dependency workflow, which targets upstream branches rather than proving the required team assessment

Why still open: Security directory is a placeholder and no authentic passive/dependency/browser-matrix reports are supplied. The strict API authorization matrix is useful completed evidence but does not replace the distinct browser/passive tasks.

Next owner action: Coordinate four browser access checks with at least one allowed and denied action, collect passive ZAP observations for both workflows, corroborate controls and run/interpret the dependency audit.

Dependency: Security directory is a placeholder and no authentic passive/dependency/browser-matrix reports are supplied. The strict API authorization matrix is useful completed evidence but does not replace the distinct browser/passive tasks. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Actual role/action expected/observed evidence, passive ZAP and checked package/version findings, risk/root cause/fix records without active attacks or real data.

Evidence/files: `tests/team/security`; `tests/team/api/test_states_and_decisions.py`; `docs/team/TEAM.md`.

## F4-PERFORMANCE —P2 —Area 3

Original owner: Zain / Area 3, coordinated by Wasay. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: W1/W2 selected operation; Performance brief section 5. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Supply justified pre-run thresholds and comparable k6 runs at one and at least five concurrent users, each setup twice for >=60 seconds after reaching load.

Actual attempts:

- Audited available source/evidence; retained test elapsed times only as tool timings

Why still open: Performance directory is a placeholder; no genuine pre-run targets, scripts or measured load outputs are supplied. API pytest elapsed time is not a p95/load result.

Next owner action: Define future p95 and unexpected-error limits before load; execute four controlled comparable k6 runs with the same build/machine/starting data.

Dependency: Performance directory is a placeholder; no genuine pre-run targets, scripts or measured load outputs are supplied. API pytest elapsed time is not a p95/load result. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Original scripts/output/environment plus p95, throughput and unexpected failures per run, interpretation against honestly predeclared targets.

Evidence/files: `tests/team/perf`; `docs/team/TEAM.md`.

## F4-RECOVERY —P1 —Area 3

Original owner: Zain / Area 3, coordinated by Wasay. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: W1/W2 state-changing operation; Recovery brief section 5. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Supply controlled dependency-failure/recovery automation with persisted failure-state readback, restoration, retry and no duplicate final records/effects.

Actual attempts:

- Completed state/refund/repetition/invalid-body atomicity checks and preserved their exact boundaries

Why still open: Recovery directory is a placeholder and no controlled dependency-failure test is supplied. The completed malformed-body refusal/atomicity regression is not relabelled as a dependency outage experiment.

Next owner action: Inject a justified dependency failure before a write, assert persisted state, restore dependency, retry and assert exact successful state/no duplicates.

Dependency: Recovery directory is a placeholder and no controlled dependency-failure test is supplied. The completed malformed-body refusal/atomicity regression is not relabelled as a dependency outage experiment. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Actual deterministic script, failure and recovery observations, source/fixture identity and persisted assertions.

Evidence/files: `tests/team/recovery`; `tests/team/api/test_business_rules.py`; `docs/team/TEAM.md`.

## F4-REGISTRATION —P2 —A / shared administration

Original owner: Team / Wasay. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Brief section 1 registration; SE-5B. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Retain the authentic section-sheet repository registration and resolve final human scope acceptance.

Actual attempts:

- Checked current team/audit/AI records and reused actual OD-01/OD-02 rather than ask already answered policies

Why still open: Repository records still carry an unverified registration TODO and no accessible authoritative sheet entry/link or genuine approval record is supplied. Historical facts cannot be created retroactively.

Next owner action: Locate the actual registration entry/confirmation and record genuine scope review decisions, or honestly report any historical absence.

Dependency: Repository records still carry an unverified registration TODO and no accessible authoritative sheet entry/link or genuine approval record is supplied. Historical facts cannot be created retroactively. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Authentic available registration/scope evidence or explicit truthful unavailable/not-completed disclosure; no invented backdated approval.

Evidence/files: `docs/team/AI_USE_RECORD.md`; `docs/team/SQE_PHASE_1_PERSONAL_AUDIT.md`; `docs/team/SCOPE.md`.

## F4-GROUP-PACKAGE —P1 —D / final submission

Original owner: Shared, coordinated by Wasay. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Brief section 6; All areas; Final PDF/ZIP/.git. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: After genuine missing inputs and accepted integration are available, assemble/verify the combined group PDF and ZIP with synchronized accepted .git history and confirmed section filename token.

Actual attempts:

- Prepared the complete Rayyan contribution, genuine shared unit inputs, actual CI artifacts, PDF, source/evidence whitelist and exact payload/Git-identity manifest
- Excluded active databases, credentials, virtualenvs and unsynchronized .git; did not reset the laptop

Why still open: Area 3/mutation/current shared gate/accepted history are incomplete. The source checkout on the laptop is stale with preserved uncommitted changes and protected metadata. A clearly labelled Rayyan contribution cannot be called the final group submission.

Next owner action: Coordinate all authentic Area 1/3 results, resolve accepted reviews/gates, confirm whether the official suffix is B or SE-5B, obtain accepted history through permitted clone/fetch and verify the final group package.

Dependency: Area 3/mutation/current shared gate/accepted history are incomplete. The source checkout on the laptop is stale with preserved uncommitted changes and protected metadata. A clearly labelled Rayyan contribution cannot be called the final group submission. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Correct three-roll/section naming, complete evidence-backed all-area PDF, public repo link, reproducible source/scripts/tools, synchronized .git, verified ZIP/payload hashes and honest release/HOLD decision.

Evidence/files: `docs/team/AREA2_PACKAGE_MANIFEST.json`; `docs/team/reports/RAYYAN_FINAL_CLOSEOUT.md`; `handoff.md`.

## F4-HUMAN-RECORDS —P2 —Shared management

Original owner: Each human contributor / coordinated by Wasay. **NOW: Wasay / Wasay's agent — mandatory. Requirement OPEN / execution transferred.**

References: Estimation/GQM/AI disclosure; Brief sections 2/7. Tested contribution source: `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`.

Required deliverable: Collect genuine effort, review and progress records if they exist; retain unavailable labels where historical records cannot be substantiated.

Actual attempts:

- Disclosed agent use and exact checks; retained actual CI timings as tool durations and kept unmeasured metrics unavailable

Why still open: No trustworthy original human timesheet/actual-versus-original-estimate history is supplied. Automated runtime cannot prove personal effort, a human RCA meeting, individual review or a passed viva.

Next owner action: Coordinate genuine existing human records and truthful shared AI/review acknowledgement; preserve actual authorship and unavailable facts.

Dependency: No trustworthy original human timesheet/actual-versus-original-estimate history is supplied. Automated runtime cannot prove personal effort, a human RCA meeting, individual review or a passed viva. No additional Rayyan technical prompt or execution is a prerequisite.

Measurable acceptance: Substantiated records or explicit unavailable labels, never fabricated hours, meetings, retroactive estimates, review or assessment outcomes.

Evidence/files: `docs/team/AI_USE_RECORD.md`; `docs/team/AREA2_MANAGEMENT.md`.

## Personal assessment facts

Personal viva, learning and authentic individual human review cannot be impersonated or certified by this execution. They are not project implementation/testing/documentation/packaging backlog for Rayyan. Genuine missing historical effort/review records stay unavailable unless substantiated; automated runtimes never become human hours.

Rayyan will no longer do any further project implementation, testing, integration, documentation, packaging or follow-up execution work. Rayyan's project execution assignment is finished. Every remaining project execution item in the final handoff is now assigned to Muhammad Wasay Tariq / Wasay's agent, and its completion is mandatory for the project. No further technical execution or additional prompt is expected from Rayyan.
