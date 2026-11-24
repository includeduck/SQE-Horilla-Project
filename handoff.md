# SQE owner handoff

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

Updated 23 November 2026. Requested by **Syed Muhammad Rayyan Hassan, 24I-3000**,
GitHub `rayyanhasan899`. Repository owner: **Muhammad Wasay Tariq**, `includeduck`.

## Execution reassignment

Rayyan explicitly assigns the blocked, unfinished work below to **Wasay / his
agent**, with completion mandatory for the project. This is Rayyan's requested
execution allocation; acceptance by Wasay has not yet been observed. Preserve
actual authorship and test results. This does not retroactively attribute
Rayyan's implemented generator/tests to Wasay or certify any course requirement.

| ID | Mandatory work now assigned to Wasay / his agent | Completion evidence | Current state |
|---|---|---|---|
| H-01 | Supply/use a permitted complete Horilla runtime; install unchanged root requirements and scoped Area 2 test tools | Actual Python/Django/DRF/tool versions, successful setup/schema checks and disposable DB/server verification | Remote setup resolved: unchanged application/test dependencies installed in CI; laptop runtime remains unavailable |
| H-02 | Recover the original Phase A archive if available, or finish and reconcile its missing live foundation/oracles | Verified original archive or fresh two-initialization/authentication/balance/schema evidence, one reconciled contract | Open; archive details are in Communication.md; no historical logs may be fabricated |
| H-03 | Execute and finish all blocked B/C API coverage, including generated input classes and dynamic balance/filter/reason gaps | Clean full suite twice, reverse/order independence, real HTTP plus persisted-state assertions, complete coverage denominators | In progress: current remote run reaches HTTP assertions; full/reversed acceptance and remaining scope are open |
| H-04 | Reproduce candidate defects, apply only source-backed minimal fixes, rerun affected team/upstream tests and produce actual defect/PR evidence | Genuine failing-before/passing-after logs, Issue/PR links, triage/RCA and retest | Attachment storage failure reproduced; narrow source fix and focused retest proposed in PR #2; other candidates need actual results |
| H-05 | Integrate the Area 2 producer command with the group's all-tests/PR gate | Required-check names, actual failed gate and successful retest; no failure suppression | Open; Wasay retains overall CI ownership |
| H-06 | Resolve laptop Git metadata/network restrictions or provide an approved synchronized checkout | Working fetch/pull and identity-safe local commits/push, preserving uncommitted files and concurrent history | Open locally; GitHub connected-app object/ref writes now work under Rayyan's identity |

## Current publication and contribution evidence

The GitHub connection recovered during the Phase C access check. These commits
were published to `sqe-team` and author/committer login verified as
`rayyanhasan899`:

- `44384b129156059d63647f6d9b8324813b668ae0`: audit, roadmap, prompts and roll correction.
- `cbe4b74282213732b176ae5e3b4519044b7b6a1e`: OpenAPI/EP/BVA generator and source basis.
- `905f08909a6b8bb3bda70a94a28c42bc8c1a7455`: initial generated HTTP slice and isolated fixtures.

These are meaningful published checkpoints, not proof of passing API tests.
Local `.git` remains read-only; `git pull --ff-only` failed on FETCH_HEAD and
the CLI push dry-run failed with a connection reset. No destructive Git action
or force push was used.

## Continuation

Use `Communication.md`, `docs/team/reports/SQE_IMPLEMENTATION_PHASE_B_STATUS.md`
and the subsequent C status report for exact files, commands and evidence.
Update this handoff as tasks are accepted, implemented, tested and published.
Do not mark a task complete because code or a report exists. Rayyan's two
personal use-case/Phase D implementation has not automatically started.

## Phase C verification checkpoint â€” 23 November 2026

Remote runtime installation is now successful. Runs 45179588790 and 45181052750
stopped at a fixture guard (171/178 setup errors), before product assertions.
Commit `1948e0fdf85ec3824e5f472176688e994307928a` repaired that guard while
retaining the explicit isolated-settings marker and exact temporary SQLite
path checks. Run 45183086568 is executing real generated-input HTTP assertions;
passing cases were observed live. Final and reversed-run results are pending.
Do not treat this in-progress observation as full acceptance.

There are 178 unique API scenarios, with 82 of 578 generated IDs referenced and
496 unconsumed. Scope completeness remains false. All 41 independent generator,
catalog and runner checks passed locally with ResourceWarning treated as an
error; these are distinct from product API tests. Application source is unchanged.
See `docs/team/reports/SQE_IMPLEMENTATION_PHASE_C_STATUS.md` for evidence.

Published checkpoints after the initial three: `aa600a2` B evidence/handoff,
`5a5df40` C suite/producer/workflow, `7fba8ee` pagination/unique ledger,
`1948e0f` fixture guard and streaming preflight. Verified Rayyan author and
committer throughout; local Git staging/pull restrictions remain unresolved.

Wasay/his agent: H-01 remote installation is resolved, but H-02â€“H-06 still require
completion where blocked, including final result evaluation, coverage/oracle
reconciliation, genuine product fixes/retests and group CI integration. Owner
issue #1 was delivered and assigned to includeduck; acceptance is unobserved.
This is Rayyan's explicit mandatory execution reassignment, preserving actual
contribution history. Phase D has not started.


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

## Phase D maximum independent execution - 24 November 2026

Rayyan requested that this agent do the maximum before assigning more work to
Wasay. This supersedes any interpretation that all new implementation/debugging
is automatically an owner handoff. This agent has implemented the two-constraint
regeneration demonstration, all ten personal browser flows and use-case specs,
report/evidence/viva contributions, eight-product/two-project risk register and
three measurable proposed criteria. It is actively fixing its own test-harness
issues and running real CI before deciding any unavoidable remaining handoff.

The C expanded subset actually returned 172 passed / five failed / 177 on run
45342013246. Those five failures used the wrong optional creator-FK oracle for
LeaveRequest; that source-backed test correction is now in 8a9ca964. D's first
browser run hit ten setup errors, not product assertions; async Playwright plus
sync_to_async ORM correction is being retested. Raw logs remain genuine.

H-02 now has Rayyan's previously missing use-case specifications supplied.
H-08 now has concrete risk/criteria/GQM/traceability/report and RCA contributions;
Wasay should integrate actual group results rather than redo these documents.
H-03/H-04 known implementation/debugging is being advanced here where possible.
Existing unresolved policy/complete-scope/overall gate/archival dependencies
remain open; none is marked complete solely because a script/report exists.
No new D task is assigned to Wasay at this in-progress checkpoint.
