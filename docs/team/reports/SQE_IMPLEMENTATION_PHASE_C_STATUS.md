# SQE implementation Phase C status

## Current continuation - 24 November 2026

This section supersedes earlier pending-result statements below. Phase C is
**partially implemented; Hold remains in effect**. Wasay merged
[PR #2](https://github.com/includeduck/SQE-Horilla-Project/pull/2) on 23 November.
Remote `sqe-team` build is `2242c502090c81031e20df912b49809a03a1f523`;
local Git HEAD is still `da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0` with preserved
uncommitted files. No local pull/reset is claimed.

[Run 45197384096](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45197384096)
completed on the merged build: **14 focused regressions passed**, **8 affected
upstream tests passed**, **41 independent tooling tests passed**, W1/W2 preflight
**1 passed**, full API collection **176 passed / 2 failed / 178 total**.
The focused collection includes four storage-only tests and repeated API tests;
these counts are separate populations and must not be added together.
Reversed execution and completeness were blocked by the old fail-fast runner.
Raw evidence: `docs/team/evidence/area2/phase-c/ci-45197384096-job.log`.

The two genuine remaining failures are
`STATE-LEAVE-cancelled-reject` (expected 400, observed 200) and
`GAP-ALLOCATION-DUPLICATE-001` (proposed 400, observed 200 plus another row).
Their business-rule oracles remain unresolved; neither assertion was weakened.
Requester refund, foreign-owner allocation PUT/DELETE, capped carry-forward and
extensionless attachment corrections now have actual passing-after evidence.

This continuation adds **97 executable API cases**: 73 generated self-service
update body cases, 15 additional attachment classes/boundaries, and nine further
pagination classes/minimum boundaries. Inventory is now **275 unique API cases**,
referencing **179/578 generated IDs**, with **399 unconsumed IDs** explicitly
listed in `tests/team/api/case_ledger.json`. New cases are pending runtime
verification; the 176/178 result belongs to the older merged build only.
Spec/data fingerprints are unchanged. Dynamic record IDs are bound after real
HTTP creation; update tests assert identity/count preservation and unchanged
balances on rejection. Files use real multipart bytes; null/omission/invalid
file JSON bindings are recorded. Pagination expectations explicitly model DRF's
fallback/clamp rather than pretending every schema-invalid query is rejected.

The producer now attempts the independent reversed API pass and completeness
check after an API collection failure, preserving the first nonzero exit.
Prerequisite/preflight failures still block dependent execution. Zero child exit
cannot hide missing/malformed/empty/failed/errored/skipped JUnit. New subprocess
regressions exercise these cases. Disposable test settings use Django's fast
MD5 test hasher for synthetic users, retaining password verification/JWT over
HTTP; this is no production hashing or password-security claim.

Local dependency installation was retried on 24 November and failed to resolve
pytest; Django/pytest remain absent and Docker's Linux engine is unavailable.
No local HTTP pass is claimed. The complete free remote runtime remains the
verification route. See the final continuation evidence below for this build's
actual checks/publication and any new runtime outcome.

Owner of implemented work: **Syed Muhammad Rayyan Hassan, 24I-3000**,
GitHub **rayyanhasan899**, SE-5B. Date: **23 November 2026**.

## Current decision

**Partially Completed / Hold.** Phase C implementation and actual remote
verification have started. The complete input scope, real product regression
results and two clean full API passes are not yet accepted. Do not call this
phase complete or start D automatically.

Rayyan explicitly assigned blocked unfinished execution to **Wasay / his agent**
for mandatory project completion. Root `handoff.md` H-01â€“H-06 and the delivered
[owner issue #1](https://github.com/includeduck/SQE-Horilla-Project/issues/1)
record that requested allocation. Acceptance by Wasay has not been observed.
Actual authorship and the official area/viva obligations remain truthful; prior
implemented work is not retroactively reassigned or fabricated.

## Git access check and actual publication

**Commit creation and branch publication work through the connected GitHub
account.** Every commit below was checked for author and committer login
`rayyanhasan899` before a non-forced branch update. No assistant coauthor was
added. Local staging and pull remain blocked by read-only `.git/index.lock` and
`.git/FETCH_HEAD`; the CLI push dry-run had a connection reset. Local HEAD still
shows the older scaffold because protected metadata was not overwritten.

| Published checkpoint | Commit |
|---|---|
| Audit, roadmap, prompts and corrected roll | `44384b129156059d63647f6d9b8324813b668ae0` |
| B generator, contract and source basis | `cbe4b74282213732b176ae5e3b4519044b7b6a1e` |
| B HTTP slice and disposable fixtures | `905f08909a6b8bb3bda70a94a28c42bc8c1a7455` |
| B evidence and mandatory owner handoff | `aa600a22e42abd3ec17fbb6cd5121354aec69003` |
| C workflow, decisions/states/auth/integration/regressions and producer | `5a5df40ededb132653b33d0547a60e3e5225e9b9` |
| Pagination clamp generation and unique case ledger | `7fba8ee3fc3e36bf8c3920a9116654174abd0241` |
| Fixture-guard repair, streaming logs and integrated preflight | `1948e0fdf85ec3824e5f472176688e994307928a` |

The starting local/remote HEAD was
`da76b337190ceb67f1a7c43ee4d5f8eca4ddc8a0`; upstream baseline remains
`6c15617b8297b7a6775daa6c29aefcc48b1eb29f`. Existing uncommitted roll/planning
changes were preserved. Branch updates use an expected-head check and reject
concurrent changes rather than force-pushing. Working files remain available
locally; reconcile them safely in a permitted checkout before a future pull.

## Prerequisites and source investigation

The attached C prompt was read completely: 114 extracted lines, 15786 bytes.
The official brief's API/technique, CI and submission requirements were read
directly, alongside the retained audit/roadmap/prompts, actual A/B status,
source-reconstructed test basis, contract/data, existing fixtures and team scope.

The original A archive is still unavailable. Its historical Linux result was
not recreated or called Windows evidence. B's current independent artifacts
existed and were revalidated; its missing local runtime was rechecked. A scoped
GitHub Actions job supplied an alternative complete application runtime using
the unchanged root dependency installer. It does not replace Wasay's complete
Sonar/mutation/all-tests PR gate.

Current routes, serializers, validation/permission helpers, leave/available-leave
models, cancellation methods, fixture lifecycle, pagination and relevant
upstream regression sources were inspected. Upstream cases are reference
material and are never included in team API-case totals. No application source
correction is claimed without actual reproduction and retest.

## Implemented C functionality

1. **Generated self-create input consumption:** 71 additional non-file body
   cases, reusing B's actual JSON artifact and fixture-bound IDs. Two numeric
   IDs already exercised by B were excluded from this consumer to avoid double
   counting. File boundaries remain in B's five-case multipart consumer.
2. **Actual pagination semantics:** the spec/generator uses
   `x-clamp-maximum: 100` from the existing paginator. Generated requests
   99/100/101 expect normalized sizes 99/100/100, with 101 synthetic rows proving
   the clamp. This is not a fictitious rejecting maximum.
3. **Decisions:** all 32 BR-02 condition vectors are retained, with 24 executable
   rows and eight explicitly infeasible reversed-date/same-day-mismatch rows.
   All eight owner/permission/reporting-manager combinations implement the
   source-backed `not owner AND (permission OR manager)` approval oracle.
4. **Transitions:** 50 allocation/leave state-and-role cases, including edits,
   deletes, cancellation decisions, terminal assertions and owner refusal. The
   requested-allocation refusal is explicitly actor-conditioned self-approval;
   it is not presented as a nonexistent pure-state command.
5. **Integration and repetitions:** zero â†’ allocation five â†’ approved three-day
   leave â†’ balance two; a separate non-overlapping three-day request must reject
   without a new row or balance change. Approval/cancellation repetitions,
   duplicate leave creation and a visible provisional allocation-duplicate
   oracle are implemented.
6. **Distinct users and defect reproducers:** ordinary employee/approver/outsider
   accounts and balances 0/7/9 reveal cross-user refunds. Targeted refund,
   non-owner PUT/DELETE and carry-forward-cap regression assertions remain
   strict. Missing/invalid JWT, authorized missing IDs and generic non-owner
   detail checks are also present.
7. **Producer and evidence:** one command validates generator/data/schema/Django,
   preflights W1/W2, runs the full API collection and reverses the second clean
   process, writes real transcripts/JUnit/manifest and fails on errors, empty or
   skipped results and incomplete scope. Output is streamed and preserved even
   if a remote run is interrupted; evidence directories cannot be overwritten.

Every targeted success/rejection includes relevant HTTP state/balance/count
readback; fixtures assert the actual disposable database path. ORM setup and
corroboration do not replace the Requests operations under test. Normal-role
auth/permissions/password hashing remain unchanged.

### Explicit binding and oracle limitations

Non-file JSON consumers omit the optional upload baseline and record the bound
request hash. Falsy end-date normalization is a handler oracle distinct from
the raw DateField predicate. The full media/normalization/filter/reason/dynamic
balance inventory still needs completion. Provisional duplicate-allocation and
terminal-state assertions require owner reconciliation before a business-policy
change. `coverage_complete` remains false; an eventual selected-suite pass would
not prove all-input completion.

## Verification results, by build

| Check / build | Actual observed result | Evidence |
|---|---|---|
| Local generator/catalog/producer checks after pagination | **41 passed**, zero test failures | `../evidence/area2/phase-c/independent-tests-after-pagination.txt` |
| Streaming-output correction | Initial run passed but exposed an unclosed-pipe ResourceWarning; pipe is now closed by a context manager | `independent-tests-streaming-warning.txt` |
| Focused final producer checks with ResourceWarning treated as error | **5 passed**, no warnings | `runner-tests-final.txt` |
| Local syntax compilation | Passed; does not execute application imports | `compile-final.txt` |
| Local full producer attempt | Generator/freshness passed, then validator import failed; dependent application stages blocked | `local-run-1/run-manifest.json` |
| Two direct local API attempts | Both stopped at missing pytest; zero test bodies executed locally | `local-api-1.txt`, `local-api-2.txt` |
| Remote build `5a5df40â€¦`, run [45179588790](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45179588790) | Dependencies installed; 40 independent checks passed; formal OpenAPI and Django check passed. **171 collected API cases had setup errors**, zero API test bodies reached. No product defect was established | `ci-45179588790-job.log`, `ci-first-summary.json`; remote artifact 14822725028 |
| Remote build `7fba8eeâ€¦`, run [45181052750](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45181052750) | Same fixture guard failed on expanded collection: **178 setup errors**. Reverse run blocked. No API pass inferred | `ci-45181052750-job.log` |
| Corrected fixture build `1948e0fâ€¦`, run [45183086568](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45183086568) | Runtime retest in progress at this checkpoint. Preflight precedes the expensive complete suite | Pending final observation; do not infer a pass |

Bare evidence names in the table are relative to
`docs/team/evidence/area2/phase-c/`. Raw failed runs are preserved. The remote
artifact ZIP exists at GitHub; a direct local download was reset, so no extracted
ZIP/JUnit copy is fabricated. The full decoded job log was retrieved through the
working GitHub connection and saved locally.

The remote runtime actually observed is Python **3.12.16**, Django **5.2.19**,
DRF **3.18.3**, pytest **9.2.0**, pytest-django **4.14.0** and Requests **2.34.2**.
The local interpreter remains Python **3.14.7**, pip **26.2.1**, without Django
or pytest. These are different environments; their results are not combined.

### Reproduced harness issue and narrow correction

`area2_seed` asserted `settings.SETTINGS_MODULE == "area2_settings"`.
The remote pytest header selected `area2_settings`, but the metadata attribute
was observed as None under the test settings/live-server context. All cases
failed at that guard before seed/API assertions.

The correction does not simply remove isolation validation. It checks the
selected environment module, a positive marker defined only in the isolated
settings, the SQLite engine and the exact test database parent under the owned
temporary root. The integrated preflight prevents this class of setup error
from needlessly repeating across the complete collection. Its actual runtime
retest is the named run above, not an assumed success.

## Coverage and acceptance

Current contract/data: **578 generated cases**, **27 operations**, **71
operation/input entries**. **178 distinct executable API cases** reference 82
distinct generated IDs; 496 generated labels remain unconsumed. The complete
ledger lists them, the infeasible rows and case IDs. These are implementation
denominators, not verified pass percentages. Requirements coverage is not test
pass rate. Wasay's unit statement/branch/MCC/MC/DC and Zain's specialist results
are not inferred from these API/catalog checks.

| Requirement | Current contribution | Acceptance gap / mandatory owner completion |
|---|---|---|
| R3â€“R5 | Spec-driven EP/BVA, native/multipart/page/reference consumers and lineage | Remaining selected input/normalization/media/generic/action/update coverage and actual current-build results |
| R6 | Decision/role vectors and 50 state/actor scenarios | Full remaining multi-condition balance rules and accepted state/duplicate oracle reconciliation |
| R7 | Shared 5â†’3â†’2 sequence, rejection/repetition and persistent readback sources | Actual assertion execution, fixes where justified, complete clean and reversed passes |
| R8/R13 | Structured candidate ledger with expected/source/reproducer/severity/risk/triage | Genuine product reproduction, Issues, correction/retest, RCA/Pareto and fixed/blocked PR evidence |
| R11 | Fail-propagating Area 2 producer and isolated runtime workflow | Wasay's complete every-PR gate and required merge/deploy enforcement |
| R12â€“R14/R16 | Actual logs, contribution/management/disclosure and verified commits | Final accepted results, GQM/risk review and truthful personal viva/human review |

Spec canonical SHA-256:
`45e37bfbcd255fc567d5923b13076637f8777bbc4c48bb239f6c2e3fe398f0db`.
Generated data SHA-256:
`38d69c57a2e33ede9682bb8b6b165d7c1398b578711983ecf05cd3f8e59e3521`.
Earlier B/first-C hashes belong to their recorded builds and remain historical.

## Files and change boundaries

New C implementation: `tests/team/api/case_catalog.py`, `http_support.py`,
`test_generated_inputs.py`, `test_states_and_decisions.py`, `test_workflows.py`,
`test_queries_and_auth.py`, `case_ledger.json`; `tests/team/run_area2.py`,
`area2_order.py`; generator bookkeeping/runner regressions;
`.github/workflows/area2-verification.yml`.

Modified existing test components: scoped conftest/settings/pytest config,
generator/verification code, OpenAPI and generated data. Relevant README,
test-basis/coverage/management/disclosure/status/communication/handoff documents
and real evidence are updated. New handoff/defect/CI/C-status files support
review. Prior planning files, roll correction and teammate source are preserved.

**Application source is unchanged at this checkpoint.** Static endpoint
candidates are not called reproduced or corrected because the failed fixture
prevented their HTTP assertions. No upstream regression pass is claimed; run
affected upstream checks separately after an actual product fix.

## Mandatory unfinished work and next prompt

Wasay/his agent is assigned H-01â€“H-06 completion: finish/reconcile the foundation
and scope, evaluate actual remote results, reproduce and narrowly fix genuine
defects, finish coverage, rerun clean/reversed suites and integrate the group
gate. Owner notification was delivered in issue #1, with progress comment
7102270422; acceptance is still unknown. Zain's specialist area is unchanged.

Overall actual human hours/estimate variance remain unavailable. Test durations
are not human effort. Defect density/reopen rate are unavailable without defined
measured populations; no fictional zeros, retrospective weekly history or team
approval is invented.

**`SQE_IMPLEMENTATION_PHASE_D.md` is not ready for dependent execution.** Its
regeneration demonstration, browser cases and final reporting need verified C
results/oracles. Independent document review may proceed, but D implementation
was not started. Keep the project on Hold until the outstanding evidence and
mandatory completion tasks are satisfied.
## Latest live checkpoint â€” 23 November 2026

Run 45183086568 at commit `1948e0f` has passed the fixture guard and is executing
real generated-input HTTP tests; passing assertions were observed live. The
full-suite and reversed-run outcomes remain pending. This supersedes earlier
wording that no current remote application assertion has executed, without
converting observed individual passes into a completed phase.

Final local independent recheck: `python -W error::ResourceWarning -m unittest
discover -s tests/team/generator -p 'test_*.py' -v` returned exit 0: **41 passed**.
Exact output: `docs/team/evidence/area2/phase-c/local-final-independent.txt`.
This rerun follows the streaming pipe cleanup and reports no ResourceWarning.


## Attachment failure and protected-branch update â€” 23 November 2026

Remote run 45183086568 reproduced storage exceptions for generated allocation
attachment filename boundaries 99 and 100 (log lines 1720/1816). The original
`horilla.models.upload_path` treated a filename without a dot as an extension,
leaving storage no basename to shorten within the FileField path budget.
A narrow correction now retains extensionless input as the basename; dotted
names retain their suffix. Four real FileSystemStorage regressions and the
existing five HTTP slice cases are configured as a targeted remote retest.
The source fix is proposed, not verified until those tests actually finish.
This supersedes earlier statements that application source is unchanged.

Branch protection now requires PRs. Evidence commit `b6e298ae646738e1122528b2835d7aa08f1f7015`
was published on `rayyan/phase-c-evidence` in PR #2, after its direct update to
`sqe-team` was rejected. Do not bypass protection. Wasay was notified through
issue #1 comment 7102792706. Further proposed corrections/evidence use the same
review branch; owner review/merge and group gate remain required.


## Final first-pass evidence and corrective proposals â€” 23 November 2026

Build `1948e0f`, run 45183086568 completed: W1/W2 preflight **1 passed**;
full collection **169 passed, 9 failed**, 184 warnings, 1038.66 seconds.
There were no setup errors in this collection. Reverse and completeness stages
were blocked by the failing first pass. Raw log: `ci-45183086568-job.log`;
summary: `ci-third-summary.json`; remote artifact 14824755317. Preflight repeats
one API scenario and does not increase the 178 unique-case denominator.

Confirmed failures: A2-D01 refund leaves requester balance at 2 instead of 5;
A2-D02 non-owner PUT/DELETE return 500 instead of controlled 403; A2-D03 raw
carry-forward accepts three days (201) despite effective cap one; A2-D09 valid
99/100 extensionless attachments trigger storage failure. Proposed narrow fixes
restore the requester, explicitly deny a foreign owner, apply existing model
carry-forward cap/policy in the serializer, and correctly split upload names.
Forecast/employee-holiday scope remains unfinished; this cap correction does
not claim to implement those separate gaps.

A2-D04 duplicate allocation and A2-D05 cancelled-to-rejected behavior also fail
the provisional tests. Their oracles conflict with current behavior and require
Wasay's explicit business-rule reconciliation. They are not silently fixed or
marked as successful. The targeted corrective retest additionally runs affected
upstream balance/carry-forward/file-display tests separately. Actual passing-after
results and full clean/reversed acceptance remain pending.


## Mandatory remaining execution assigned to Wasay / his agent - 24 November

Rayyan reaffirms that all unfinished work he cannot complete is assigned to
Wasay / his agent and is mandatory. It is no longer Rayyan's remaining execution
assignment. Preserve the authorship of completed contributions; do not infer
Wasay's acceptance or rewrite the course's per-member assessment rules.

| ID | Mandatory action and acceptance evidence | State |
|---|---|---|
| H-02 | Recover A archive or create fresh reproducible foundation; reconcile live Swagger, scope and complete accepted oracles | Open; historical archive unavailable |
| H-03 | Execute new 275-case suite twice from disposable starting state, inspect both orders/JUnit, finish all remaining 399 generated IDs and input/media/reference/action/filter/reason/relational gaps | New consumers implemented; actual new-build results pending |
| H-04 | Complete positive-effective-day, employee-specific holiday and forecast reproductions/fixes; retain fails-before/passes-after team and impacted upstream evidence; finish genuine Issues/RCA/Pareto | Four earlier corrections verified; remaining candidates open |
| H-05 | Wire producer plus Sonar/all tests/mutation into every PR and enforce justified required merge/deploy gates; retain a genuinely blocked PR and corrected PR | Group gate remains Wasay's ownership; push workflow is insufficient |
| H-06 | Provide a synchronized working checkout with permitted Git metadata/network access; preserve this checkout's existing files | CLI DNS/thread and Docker failures persist; connected publication is available |
| H-07 | Decide duplicate allocation identity/rejection-versus-idempotency and cancelled-to-rejected terminal policy, document rationale in SCOPE/basis, implement accepted rule and rerun both failing assertions | Mandatory unresolved business decisions; do not mask failures |
| H-08 | Finish shared risk/traceability/GQM/effort and final report using actual populations, plus required two major RCA and Pareto; use unavailable for unknown effort/density/reopen metrics | Evidence contribution supplied; no invented hours or approvals |

**Next prompt:** `docs/team/SQE_IMPLEMENTATION_PHASE_D.md`, after C's actual
coverage/oracle results are reconciled. D has not started. Independent document
review can proceed; regeneration/browser/final acceptance dependent on C remain
pending. Zain retains his specialist work and recovery evaluation.

## Final local continuation verification - 24 November 2026

- `python -W error::ResourceWarning -m unittest discover -s tests/team/generator -p 'test_*.py' -v`: **45 passed**, no failures or skips; raw output `docs/team/evidence/area2/phase-c/continuation-independent-20261124.txt`.
- `python -m compileall -q tests/team/api tests/team/generator tests/team/run_area2.py tests/team/area2_settings.py`: exit zero; compilation only, not application imports.
- `git diff --check`: exit zero (line-ending conversion notices only).
- `python tests/team/run_area2.py --evidence docs/team/evidence/area2/phase-c/continuation-local-20261124`: 45 independent checks and freshness passed; formal schema stage failed because `openapi_spec_validator` is absent; dependent Django/API stages blocked, no API XML or local HTTP pass. Actual manifest/logs are preserved in that new directory.
- A remote publication attempt was rejected by automatic approval review: it did not recognize authorization to upload this source/log/document set to the repository. No remote commit/ref update/PR or new CI run succeeded in this continuation. Explicit publication approval was requested; until granted, verification of the 97 new API cases is blocked. Do not treat prior write access or PR #2 as new publication evidence.

The source-backed two-major-defect 5 Whys/cause diagrams and four-defect Pareto
contribution is in `docs/team/reports/AREA2_RCA_CONTRIBUTION.md`. It uses real
before/after build populations, marks causal inferences and leaves Wasay's
human triage, product-Issue reconciliation and group final reporting pending.

## Publication authorization - 24 November 2026

Rayyan explicitly approved publishing the prepared Phase C changes to
`includeduck/SQE-Horilla-Project`, branch `rayyan/phase-c-evidence`, opening a
continuation PR and triggering its free GitHub Actions tests. This supersedes
the earlier authorization blocker. Publication and runtime results will be
recorded after they are actually observed; no completion is inferred here.

## Published continuation - 24 November 2026

Publication succeeded after Rayyan's explicit approval. Commit
`b8480253e6fd4f7679e39eac14395296a269a9a0` is pushed to
`rayyan/phase-c-evidence`; GitHub author and committer are both verified as
`rayyanhasan899`. [Draft PR #8](https://github.com/includeduck/SQE-Horilla-Project/pull/8)
targets protected `sqe-team`; it has not been merged.

[Area 2 run 45342013246](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45342013246)
started on that exact source commit. At this observation, application dependency
installation is in progress; no new API pass or phase completion is inferred.
The previous automatic approval rejection is historical and is now resolved.
Mandatory Wasay handoffs H-02 through H-08 remain in force until their required
evidence is completed. Local Git metadata/HEAD remain unchanged; no pull or
local commit is claimed. Phase D remains unstarted.
