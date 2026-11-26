## Final execution closeout — 25 November 2026

Rayyan's project execution assignment is finished. **Whole-project release: HOLD.** No further technical execution or additional prompt is expected from Rayyan.

The final application/API verification source is `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`; Actions checked synthetic merge `801351079aada8c399db2212d9c033737e032e0d` with `sqe-team` base `0a5ac6443dadb50ab5fd6ea749f41dd108a19486`. [Run 45627793460](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45627793460) verifies **3,433/3,433 API cases in each of two orders**, with zero failures/errors/skips/missing IDs and strict complete-scope acceptance. Each collection is the exact union of 16 fresh isolated deterministic shards; reversal occurs within each shard, not a claim of one monolithic reversed process.

**713/713 generated IDs, all former 399 missing IDs, 350/350 mandatory input families, FR-01–FR-10 and BR-01–BR-04 are verified** from real source-bound assertions. Ten personal browser flows pass; the consuming regeneration has six baseline passes and exactly two predicted strict variant failures with four passes. Separate overlapping populations and full links are in [RAYYAN_FINAL_CLOSEOUT.md](reports/RAYYAN_FINAL_CLOSEOUT.md), the final evidence index and machine ledger. Never sum them into a fictitious unique-test total.

All remaining project execution is **Wasay / Wasay's agent — mandatory**, with exact attempts, dependencies and acceptance in root [handoff.md](../../handoff.md) and `finish-line/REMAINING_WORK.json`. Current shared gate evidence is genuinely red for missing Sonar service/credentials and mutation runner/policy; supplied units pass. No independent review, merged PR #8, required branch/deploy enforcement, teammate authorship, human effort or passed viva is inferred.

The PDF/ZIP is a **Rayyan contribution, not the final group submission**. Earlier dated results/ownership below are historical and superseded by the final handoff; they do not assign new execution to Rayyan.

---

### Final AI assistance and verification record

The agent inspected current source and genuine CI outputs, wrote/checked CI integration and packaging, reconciled actual identities, and drafted reports/mandatory ownership. Product results are actual pytest/JUnit/Playwright observations; synthetic gate-control fixtures are labeled and excluded from product/mutation results. Human timesheets, independent review, meetings and passed viva were not generated as facts. Raw run/code/commit provenance permits verification. Unavailable local execution was replaced by permitted free Actions.

---

## Historical dated appendix (not current ownership or pending work)

# AI-Use Record

Required by brief §7: tool, purpose, output, and what we checked or changed. Keep prompts.

| # | Date | Member | Tool | Purpose / prompt (summary) | Output | What we checked / changed |
|---|---|---|---|---|---|---|
| 1 | 2026-11-18 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Examine the project brief and say what it's about"; "Search for an appropriate MIS" (InvenTree, frappe/helpdesk, akaunting already taken) | Summary of brief; shortlist: Horilla, NetBox, pretix | _TODO: confirm repo is free in section sheet_ |
| 2 | 2026-11-18 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Check if horilla_api has leave endpoints, then set up the base of the project" | Cloned upstream at baseline commit; confirmed `/api/leave/*` endpoints; local venv + SQLite setup; `tests/team/` scaffold; draft `SCOPE.md`, `SETUP.md`; seed/reset scripts | _TODO: each member reviews SCOPE.md rules against the code and running app; edit before use_ |
| 3 | 2026-11-23 | Syed Muhammad Rayyan Hassan (24I-3000) | ChatGPT / Codex coding assistance | Execute supplied `SQE_IMPLEMENTATION_PHASE_B.md`; preserve scope and document blockers | Source-reconstructed scoped OpenAPI JSON, deterministic EP/BVA generator, focused independent regressions, five-case real-HTTP consumer and disposable settings, coverage/status/communication records | Automated checks and source inspection are reported in `reports/SQE_IMPLEMENTATION_PHASE_B_STATUS.md`; a source-inspection test initially failed because it omitted inherited handlers and was corrected. HTTP, Django, formal schema validation and Ruff were attempted but dependencies were unavailable. No live API pass, recovered A evidence, personal human review or completed viva is claimed. Prompt retained in `docs/team/SQE_IMPLEMENTATION_PHASE_B.md`; exact supplied attachment was read in full. |
| 4 | 2026-11-23 | Syed Muhammad Rayyan Hassan (24I-3000) | ChatGPT / Codex coding assistance | Execute supplied C prompt, verify commit/push/pull, and transfer blocked remaining execution to Wasay as explicitly requested | Real GitHub checkpoint commits under verified rayyanhasan899 author/committer; delivered owner issue/handoff; generated-input, decision/state/auth/integration/regression sources; producer and isolated GitHub Actions verification | Independent checks, actual local failures, remote-run results and any later source fixes/retests are separated in `reports/SQE_IMPLEMENTATION_PHASE_C_STATUS.md`. Source candidates are not called reproduced defects until actual results establish them. Scope gaps, provisional oracles and personal human review/viva remain explicit. No D implementation is authorized by this entry. |
| 5 | 2026-11-25 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start Sonar" on local SonarQube 26.10: write scanner config, run baseline scan, report metrics, hand-calculate cyclomatic complexity for one business-rule function | `sonar-project.properties`; baseline scan + raw evidence in `docs/team/evidence/sonar/`; `reports/SONARQUBE_BASELINE.md` incl. CFG for `calculate_requested_days` (hand V(G)=6 vs SonarQube 6) | Token created and stored by me (not seen by the tool). Checked the two leave-module findings in source: S5644 judged a likely false positive, S1763 confirmed. _TODO (Wasay): re-count CFG edges/nodes by hand before the viva._ |
| 6 | 2026-11-25 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start unit tests": white-box tests for leave business logic, 100% statement+branch, MCC and MC/DC for the critical module | `tests/team/unit/` (126 tests + 1 xfail), `coverage_scope.py` gate, `mcc_tables.py` generator, `reports/WHITEBOX_UNIT_TESTING.md`, `reports/MCC_MCDC_TABLES.md`, Sonar rescan with coverage | Reviewed scope list and each justified gap against the source; MCC rows executed against real code (all outcomes matched). _TODO (Wasay): re-derive one MCC table (C1 or C3) and the C5 MC/DC pairs by hand before the viva._ |
| 7 | 2026-11-24 | Syed Muhammad Rayyan Hassan (24I-3000) | ChatGPT / Codex | Execute attached Phase D, maximize independent work before new owner handoffs | Controlled two-constraint generator/HTTP experiment, two personal use-case specs and ten Playwright flows, test-only static serving, workflow/report/evidence/risk/criteria/viva contributions | Read attachment and official brief; 49 independent checks pass; real C run exposed wrong creator-FK assertion and source-backed correction; first browser runtime exposed event-loop setup errors, corrected to async Playwright plus sync_to_async without disabling Django safety. Verified regeneration HTTP baseline 6 pass / variant 4 pass + exactly 2 strict predicted failures. Browser runs exposed harness issues and then a genuine blank-amount form defect; narrow product correction and unchanged UI regression supplied. Retrieved owner OD-01/OD-02 and implemented two strict API fixes rather than xfail. Final browser/product retests require actual CI evidence. Human review, effort and viva are not inferred. |

24 November 2026 continuation: Codex read the current Phase C attachment and
GitHub merge/run evidence, retained actual 14/8/176+2 result populations, added
generated update/file/pagination consumers and strict runner result handling.
Independent subprocess checks exercise failure retention/reversed execution;
new API assertions require real runtime verification. No disputed duplicate or
terminal-state oracle was changed. Incomplete mandatory execution is assigned
to Wasay/his agent in handoff.md; human review/viva remains unverified.

24 November 2026 later continuation: Codex retrieved the completed raw logs,
retained source/build identity and exact separate 16/8/177/1/275 passing
populations from 45355537962, and kept its cancelled reverse result explicit.
It increased the measured-too-short job budget from 90 to 120 minutes without
changing assertions or the complete-scope gate. It corrected its own Create
selector regression after inspecting the active CBV URL mappings, nav classes
and theme templates: visible route controls can be anchors or buttons. Genuine
failed logs are retained; no failure was relabelled as a product pass. It added
the separate seven-defect Pareto population after owner-confirmed D04/D05 strict
API retests and D10's unchanged browser regression passed. Personal human
review, timesheets, owner acceptance, Issue closure and viva remain unverified.

Final observed personal-browser result: source 7189656a, run 45388276537,
job 138424862639 passed all ten declared flows and the strict HTML completion
report. Artifact 14917252664 retains genuine XML/log/screenshots/traces; the
decoded job log and explicitly derived summary are saved. This verifies the
agent's automated checks, not Rayyan's personal review or viva. The final package
inventory uses published Git blob identities/byte sizes instead of stale laptop
newline-dependent hashes; group PDF/ZIP/.git and required scope remain open.


## Final same-source Phase D verification - 24 November 2026

Source 7189656a / run 45388276537 completed both D jobs successfully. Browser:
all ten flows passed, strict HTML completion report passed, artifact 14917252664.
Regeneration: job 138424862957 retained baseline six passes, variant four passes
and exactly two predicted strict failures, zero errors/skips and genuine variant
exit one; experiment_demonstrated true. Current raw log and labelled summary are
ci-45388276537-regeneration-passed.log and regeneration-current-verified-summary.json
under docs/team/evidence/area2/phase-d/. These results complete this personal
contribution's EC-3 evidence; overall required scope and group release remain HOLD.

## Prompt 1 execution disclosure — 24 November 2026

Rayyan instructed Codex to execute PROMPT_01_CONTRACT_AND_SCOPE.md completely. Codex inspected live remote scope/owner decisions, source and current evidence; created isolated CI foundation/schema/introspection probes; reconciled canonical operations/media/fields; regenerated data with preserved identity lineage; audited every old 399 and all 713 current IDs; produced a 329-family required-input plan; updated handoff/test basis/status and published meaningful commits with the connected Rayyan identity. The local execution environment became unavailable; no interrupted local write/test is counted as complete.

Verification used actual normal-role HTTP/state/ORM assertions, production Swagger HTTP 200, two fresh databases, formal OpenAPI validation, 49 existing and four new reader checks, deterministic freshness, ID-partition assertions and real consumer smoke (exact final results in RAYYAN_FINISH_01_STATUS.md). A strict reader-extension candidate failure was retained and corrected; it is not a product defect. Evidence summaries are derived, never fabricated JUnit. No production source or required assertion was weakened, no xfail/required skip was added, no new policy or human acceptance was invented. Prompts 2–4 remain actual work; whole-project coverage stays incomplete. Human members must truthfully review/understand their assessed contributions.

## Prompt 3 execution - 25 November 2026

Codex is implementing the supplied business-rule and strict correction stage.
It reconciled current CI failures and the single AI-record merge conflict,
preserving Wasay's Sonar/unit records and Rayyan's existing disclosures. The
new HTTP baseline and source-bound workflow are published before product fixes;
actual before/after results and limitations belong to RAYYAN_FINISH_03_STATUS.md.
Rayyan explicitly approved this stage's public repository publication. No
teammate review, human effort or viva is inferred.


## Prompt 3 verified completion — 25 November 2026

Codex implemented/reviewed the business catalog, real HTTP/state consumers,
strict baseline reproductions, seven narrow product corrections, generated/wire
carryover, requirement evidence selectors, source-bound coverage reconciliation
and defect/RCA/management/handoff records. Rayyan explicitly approved publication.
Actual output checks: all 3,433 API cases passed in BOTH orders on fecac354c9b5d8ea47ac732a2b089ed3cc148620,
all 350 input families and 713 generated IDs verified, and all 14 FR/BR selectors
passed; exact separate populations and run/artifact links are in the Prompt 3
status. No required test was skipped, xfailed or weakened.

Corrections to the agent's own work are disclosed: object versus page parsing,
a valid nonmatching self-list fixture, the mistaken TextField.clean length oracle,
and the positive-duration fix's date-order error precedence. The latter was
repaired by 4a719a17 without changing the strict end_date assertion. The optional
reason helper's 1000 limit, model's declared 255 and observed SQLite behavior
remain distinct. A stale original-team strict xfail marker was removed after its
unchanged 400 assertion passed. The report-retrieval helper's redirected-download
401 was repaired and its five readers passed independently in run 45625562265;
it is a harness failure, not a product defect.

The connected account authored repository commits and necessary factual Issues/
PR updates. No unrelated messages, paid services, invented historical JUnit,
human review, effort, RCA meeting, teammate approval or viva were claimed.
The disconnected local workspace and its uncommitted files were preserved.
Prompt 4 remains unexecuted; final integrated verification/packaging/assignment
closeout and genuine owner/shared dependencies are precisely retained.
| 7 | 2026-11-26 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start mutation testing": mutmut 3 in WSL on the scoped business-rule functions, 2+ custom operators, analyse survivors, kill killable | `setup.cfg`, `tests/team/mutation/` (runner, 3 custom operators, analyser), `test_mutation_killers.py` (+32 tests), `reports/MUTATION_TESTING.md`, evidence runs 1 and 2 | Ran both mutation runs myself in WSL; every survivor diff is in evidence. _TODO (Wasay): be able to explain each custom operator, 3 equivalent mutants (incl. the `>` vs `>=` one) and 3 killed survivors in the viva._ |
| 8 | 2026-11-26 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start with the risk register and test plan" | `RISK_REGISTER.md` (11 product + 5 project risks, 5x5 matrix, technique/depth by level, 5 exit criteria incl. 3 release criteria), `TEST_PLAN.md` (scope, approach by risk, roles, environment, data, schedule, entry/exit/suspension/resumption, three-point estimates) | Scores are evidence-based from logged defects (#4-#31). _TODO (whole team): review L/I scores together; each member fills the Actual effort column for their own areas._ |
| 12 | 2026-11-26 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start the traceability matrix and defect analysis" | Triage labels (severity, priority, triage, category, status) on all 33 defects; `scripts/team/traceability.py` and `TRACEABILITY_MATRIX.md` (14/14 requirements covered); `scripts/team/defect_pareto.py` (defect log CSV + Pareto by count and by severity); `scripts/team/fishbone.py`; `reports/DEFECT_ANALYSIS.md` with 5 Whys + fishbone for #4 and #46 | Checked every RCA "because" against the code/git history (commit 932930913, web vs API refund code, atomic only in leave_assign/leave_request_import); removed fishbone causes I could not evidence. _TODO (team): review severity/priority of Area 2 issues #14-#31; decide whether to close the fixed-verified issues._ |
| 11 | 2026-11-26 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start the accessibility testing" (Area 3 work taken over by team agreement) | `tests/team/a11y/` (2 Playwright task tests incl. keyboard navigation and reject-then-correct, axe-core scan of 4 screens, logged-in Lighthouse), baseline and after-fix evidence, fix of the My Leave Requests screen in Horilla templates (`a11y_fixes.html`, header, sidebar, index), `reports/ACCESSIBILITY_TESTING.md`; also fixed `reset.ps1` (stale SQLite WAL files corrupted the restored DB) | Ran both phases myself; checked the fixed page visually and that the task tests still pass. _TODO (Wasay): explain the contrast calculation and why Lighthouse and axe issues are counted once._ |
| 10 | 2026-11-26 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start the performance testing" (Area 3 work taken over by team agreement) | k6 script `tests/team/perf/available_leave.js` (limits set before runs), 4 runs (1 VU x2, 5 VU x2) with raw output and environment; failure-and-recovery test `tests/team/recovery/` with a DB-failure test double; `reports/PERFORMANCE_TESTING.md`; recovery test added to the CI unit job | Ran all k6 runs and the recovery test myself; the recovery test exposed REC-01 (non-atomic approval, double credit 5 to 8 to 11). _TODO (Wasay): explain the p95 limit choice and REC-01 in the viva._ |
| 15 | 2026-11-26 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Fix #46": make approve/reject decisions atomic | Test-only commit first (recovery tests red: allocation 5->8, leave 5->3); then `@transaction.atomic` + `select_for_update` on the four API approve/reject `put` methods and the web allocation approval; performance report updated with before/after | Ran recovery (5 passed), unit (159, 100% scoped coverage) and the mutation gate (97.9%, 0 unexplained) after the fix. _TODO (Wasay): explain why the 2nd-write failure left a partial commit and how atomic + row lock prevent it._ |
| 9 | 2026-11-26 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Start the security testing" (Area 3 work taken over by team agreement) | Routes/data inventory, access matrix, `tests/team/security/test_access_matrix.py` (6 Playwright decisions incl. state read-back), ZAP 2.17 passive scan of 397 requests, controls review (cookies, role checks, CSRF), pip-audit of 178 packages, `reports/SECURITY_ASSESSMENT.md` | Ran every test and scan myself against the local seeded app; triaged each ZAP alert against `settings/security.py` and the view source (several are development-only). _TODO (Wasay): be able to show SEC-01 (GET approval) and explain why AD-2 is a denial despite HTTP 200._ |
