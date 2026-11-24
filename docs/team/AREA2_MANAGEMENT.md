# Area 2 activity and management contribution

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

Syed Muhammad Rayyan Hassan, **24I-3000**, 23 November 2026.

## Current control decision

**Hold full Area 2 completion.** Phase C is explicitly authorized by the user. Independent generator/catalog/producer checks pass and the remote verification workflow installed the application runtime. Local runtime/Git limits and missing A recovery remain recorded. Accept API results only after retrieving the corresponding build evidence. All-input scope remains incomplete; Phase D has not started.

Phase C continues the B prerequisite repair. A real HTTP attachment failure now justifies a narrow correction to `horilla/models.py::upload_path`, proposed in PR #2. Other application source, teammate modules and seed logic remain unchanged. Focused storage/HTTP retest is pending.

## Measurable activity and effort

The B status report and `evidence/area2/phase-b/` record actual test counts, command exits, tool versions and generated fingerprints. Generated case counts measure available data, not API cases executed or requirement coverage. Local HTTP attempts stopped before collection. Remote API runs are now in progress; actual executed/pass/fail counts must come from build-specific JUnit/logs, not source inventory.

No reliable start/end time sheet or original A estimate is available locally. Overall actual hours and estimate-versus-actual variance are unknown. Test elapsed seconds in raw logs are tool execution durations, not Rayyan's human effort. No retrospective pre-implementation estimate, weekly report or human review is invented.

For **remaining B verification only**, a provisional forecast after package/runtime access is restored is O=1, M=2, P=4 hours, PERT=(1+4Ã—2+4)/6=2.17 hours. This is an unapproved future-work estimate made after the implementation began, excludes waiting/access delay, and must be revised if runtime failures require more work. Group-wide estimation remains shared.

## Risk-based priorities

| Risk | Likelihood Ã— impact, provisional 1â€“5 | Control / verification |
|---|---|---|
| Untested contract assumptions produce misleading passing tests | 4Ã—5=20 | Label source-only assumptions, introspect serializers, run real HTTP and inspect state. |
| Missing dynamic business inputs hide balance/ownership defects | 4Ã—5=20 | Preserve incomplete coverage, recover A basis, bind C scenarios and compare both users' state. |
| Environment/access failure prevents reproducible submission | 5Ã—4=20 | Maintain logs, owner handoffs and exact commands; distinguish verified publication from blocked local Git operations. |
| Accidentally resetting an existing local DB | 2Ã—5=10 | Dedicated settings with absolute temporary SQLite/media paths; fixture asserts the DB parent before seeding. |

These are Area 2 risk contributions, not the assignment's completed group risk register or approved 5Ã—5 matrix. Shared plan, eight product/two project risks, exit criteria and final GQM/completion reporting remain group obligations.

## B entry / exit / suspension / resumption

Generator entry: source-readable spec, explicit supported dialect and deterministic nonsecret bindings. Generator verification exit: focused tests pass, repeated bytes match, unsupported constraints and staleness fail, case lineage remains inspectable.

B completion exit additionally requires formally validated/reviewed contract and the five genuine HTTP consumer cases, correct field errors/state/ownership/balance readback, and a repeat run in a different order. Those acceptance conditions remain unverified. A valid generator run alone does not release this gate.

Suspend dependent HTTP work when packages, engine, schema defaults or an oracle are unavailable. Resume after obtaining a permitted environment, installing unchanged application requirements plus scoped test tools, validating the contract and rechecking A isolation. Keep original failures and record fixes; never replace them with invented results.

## Ownership handoff

Wasay: repository write/access route, available compatible runtime or original A archive, and CI command/required-check coordination. Rayyan retains generator/HTTP fixes and reruns. Zain retains Area 3; the B harness can later be shared without replacing his work. `Communication.md` records delivery state; local notes are not proof that a teammate received them.

## Phase C control actions and ownership update

Rayyan explicitly requested transfer of blocked unfinished execution to Wasay/his agent, with completion mandatory. Root handoff.md H-01 through H-06 and GitHub issue #1 record this allocation and delivered notification. Acceptance is not assumed. Original authored work and the official per-member area/viva requirements are not retroactively rewritten.

Frequent meaningful checkpoints are now actually published under Rayyan author/committer identity; the connected-app write restriction was resolved. Local Git metadata remains read-only. The isolated remote workflow supplies a test environment without changing Wasay's complete PR gate.

Proposed GQM populations: functional requirement coverage is verified FR IDs / the ten selected FR IDs (not API case pass rate); API result rate is passed executable cases / executed cases for one build/run; defect density needs confirmed defects / an explicitly measured size, currently unavailable; reopen rate needs reopened confirmed defects / closed confirmed defects, currently unavailable. A coordination issue is not counted as a product defect. No unavailable metric is reported as an invented zero.

Current implementation accounting: 178 API scenarios, 82 distinct generated IDs referenced out of 578 generated labels, 24 feasible of 32 BR-02 rows, eight BR-04 rows, 50 state/actor cases. These are implementation denominators. Result evidence and remaining scope must be reviewed before any release decision. No human effort or team signoff is inferred from automated execution time.

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
