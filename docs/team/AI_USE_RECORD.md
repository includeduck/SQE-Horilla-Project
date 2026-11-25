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
