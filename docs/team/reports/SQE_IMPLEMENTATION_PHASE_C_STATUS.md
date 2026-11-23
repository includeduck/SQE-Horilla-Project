# SQE implementation Phase C status

Owner of implemented work: **Syed Muhammad Rayyan Hassan, 24I-3000**,
GitHub **rayyanhasan899**, SE-5B. Date: **23 November 2026**.

## Current decision

**Partially Completed / Hold.** Phase C implementation and actual remote
verification have started. The complete input scope, real product regression
results and two clean full API passes are not yet accepted. Do not call this
phase complete or start D automatically.

Rayyan explicitly assigned blocked unfinished execution to **Wasay / his agent**
for mandatory project completion. Root `handoff.md` H-01–H-06 and the delivered
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
5. **Integration and repetitions:** zero → allocation five → approved three-day
   leave → balance two; a separate non-overlapping three-day request must reject
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
| Remote build `5a5df40…`, run [45179588790](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45179588790) | Dependencies installed; 40 independent checks passed; formal OpenAPI and Django check passed. **171 collected API cases had setup errors**, zero API test bodies reached. No product defect was established | `ci-45179588790-job.log`, `ci-first-summary.json`; remote artifact 14822725028 |
| Remote build `7fba8ee…`, run [45181052750](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45181052750) | Same fixture guard failed on expanded collection: **178 setup errors**. Reverse run blocked. No API pass inferred | `ci-45181052750-job.log` |
| Corrected fixture build `1948e0f…`, run [45183086568](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45183086568) | Runtime retest in progress at this checkpoint. Preflight precedes the expensive complete suite | Pending final observation; do not infer a pass |

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
| R3–R5 | Spec-driven EP/BVA, native/multipart/page/reference consumers and lineage | Remaining selected input/normalization/media/generic/action/update coverage and actual current-build results |
| R6 | Decision/role vectors and 50 state/actor scenarios | Full remaining multi-condition balance rules and accepted state/duplicate oracle reconciliation |
| R7 | Shared 5→3→2 sequence, rejection/repetition and persistent readback sources | Actual assertion execution, fixes where justified, complete clean and reversed passes |
| R8/R13 | Structured candidate ledger with expected/source/reproducer/severity/risk/triage | Genuine product reproduction, Issues, correction/retest, RCA/Pareto and fixed/blocked PR evidence |
| R11 | Fail-propagating Area 2 producer and isolated runtime workflow | Wasay's complete every-PR gate and required merge/deploy enforcement |
| R12–R14/R16 | Actual logs, contribution/management/disclosure and verified commits | Final accepted results, GQM/risk review and truthful personal viva/human review |

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

Wasay/his agent is assigned H-01–H-06 completion: finish/reconcile the foundation
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
## Latest live checkpoint — 23 November 2026

Run 45183086568 at commit `1948e0f` has passed the fixture guard and is executing
real generated-input HTTP tests; passing assertions were observed live. The
full-suite and reversed-run outcomes remain pending. This supersedes earlier
wording that no current remote application assertion has executed, without
converting observed individual passes into a completed phase.

Final local independent recheck: `python -W error::ResourceWarning -m unittest
discover -s tests/team/generator -p 'test_*.py' -v` returned exit 0: **41 passed**.
Exact output: `docs/team/evidence/area2/phase-c/local-final-independent.txt`.
This rerun follows the streaming pipe cleanup and reports no ResourceWarning.


## Attachment failure and protected-branch update — 23 November 2026

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

