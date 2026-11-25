## Prompt 3 current management and traceability — 25 November 2026

This dated section supersedes older inventory, unfinished-oracle and pending
publication statements below. Technical results are source-bound, with final
run IDs/counts in reports/RAYYAN_FINISH_03_STATUS.md. Inventory is 3,433 unique
API scenarios, 713 canonical generated IDs, 2,256 supplementary wire cases and
350 mandatory input families. The 399 historical missing IDs are preserved
individually; all passed both orders even in the retained 13200cd9 baseline.
That baseline still failed two strict date-order assertions per order and
cannot establish full-scope acceptance.

The highest-priority controls now include positive duration, target-specific
holidays, capped/no-carry/forecast/expiry boundaries, current-policy approval,
body refusal before mutation, changed-target authorization and exact requester/
actor debit/refund. Reasons and model/helper limits are documented separately.
FR acceptance is derived from explicit assertion selectors, actual source/spec
lineage and every selected result in both orders; tags/counts alone are excluded.

| Risk | Control now implemented | Residual dependency |
|---|---|---|
| A2-R01, score 20 | Independent duration/funds boundaries, correct holiday target, forecast/expiry lifecycle and current approval caps | Owner acceptance/integration of the retested corrections |
| A2-R02, score 15 | Distinct requester/actor/outsider funds, nonowner denial, new-target permission checks | Protected review/merge; no concurrent authorization guarantee claimed |
| A2-R03, score 12 | OD-02 sequential pending-duplicate refusal and repeated grant/approve/refund checks | Concurrency/idempotency is outside accepted scope |
| A2-R04, score 12 | OD-01 terminal refusal, complete state/role table and refusal atomicity | Owner state-graph review; no skip/xfail substitution |
| A2-R05, score 16 | All canonical IDs retained; freshness, unsupported-reader negative controls and source-bound full guard | Final Prompt 4 package/contract reconciliation |
| A2-R06, score 9 | Filename boundaries, real storage and uploaded-byte readback | Original fix merged; retain regression in final build |
| A2-R07, score 16 | Ten visible/persisted browser flows including blank-amount refusal | Human review/viva remains an authentic personal obligation |
| A2-R08, score 12 | Date/order/breakdown/reference/filter/media/decision cases with unchanged-state refusals | Whole-group acceptance is separate |
| A2-J01, score 20 | Free isolated Actions and connected identity-safe publication | Local workspace remains disconnected; preserve its working files |
| A2-J02, score 16 | Existing OD-01/02 reused; 22-defect/Issue mapping, dated evidence and precise remaining ownership | Owner-only review/gates and genuine Area 1/3 package inputs |

The prior likelihood/impact scores remain provisional; test passes do not create
measured new probabilities or justify arbitrarily lowering them. Technical
EC-1/EC-2 results depend on the final source-bound full guard; EC-1's accepted
integration/no-unresolved-high-defect criterion remains HOLD while review is
pending. EC-3 browser/regeneration is measured separately. Release remains
HOLD for shared gates, integration and final Prompt 4; no automated metric is
called team approval.

GQM uses verified FR selectors/10 and BR selectors/4, API passes/3,433 per order,
verified generated IDs/713 and mandatory families/350 on one recorded source.
These populations overlap and are never added into a larger unique total.
The current confirmed-defect population is 22 across dated builds, with four
merged/closed originals and eighteen retested proposals awaiting integration.
Density needs a defined measured size; human effort/estimate variance, a human
RCA meeting and unobserved reopen history remain unavailable, not invented zeroes.

---

Historical dated records follow. Current source-specific results above supersede their older pending/count labels.

# Area 2 activity and management contribution

## Latest verified progress - 24 November 2026

Run 45355537962 on source 32621b42 verified 275/275 full first-order API cases
with zero failures/errors/skips in the completed summary, plus separate 16
focused, eight upstream, 177 expanded and one preflight passes. Reversed order
was incomplete when the 90-minute job limit expired. This is a current-build
100% first-order pass rate for the implemented inventory, not full scope,
requirement coverage or twice/order-independent acceptance. Source 7189656a
raises the job budget to 120 minutes; strict assertions/completeness stay intact.

Owner-confirmed A2-D04/D05 API corrections passed strict regressions, and
A2-D10's unchanged blank-amount browser test passed in 45355537997. Seven
distinct corrected/retested defects now have evidence across the identified
merged/draft builds; see the separately labelled seven-defect Pareto update.
Browser harness errors are not product defects. Source 7189656a / run
45388276537 verified all ten browser flows and the strict HTML report;
artifact 14917252664 retains actual XML/log/screenshots/traces. Human review/viva/effort and
team acceptance are not inferred. EC-1/EC-2 and group release remain HOLD due
to remaining balance/input scope and group gate/package requirements.

## Historical continuation - 24 November 2026

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

For **remaining B verification only**, a provisional forecast after package/runtime access is restored is O=1, M=2, P=4 hours, PERT=(1+4A-2+4)/6=2.17 hours. This is an unapproved future-work estimate made after the implementation began, excludes waiting/access delay, and must be revised if runtime failures require more work. Group-wide estimation remains shared.

## Risk-based priorities

| Risk | Likelihood A- impact, provisional 1�?"5 | Control / verification |
|---|---|---|
| Untested contract assumptions produce misleading passing tests | 4A-5=20 | Label source-only assumptions, introspect serializers, run real HTTP and inspect state. |
| Missing dynamic business inputs hide balance/ownership defects | 4A-5=20 | Preserve incomplete coverage, recover A basis, bind C scenarios and compare both users' state. |
| Environment/access failure prevents reproducible submission | 5A-4=20 | Maintain logs, owner handoffs and exact commands; distinguish verified publication from blocked local Git operations. |
| Accidentally resetting an existing local DB | 2A-5=10 | Dedicated settings with absolute temporary SQLite/media paths; fixture asserts the DB parent before seeding. |

These are Area 2 risk contributions, not the assignment's completed group risk register or approved 5A-5 matrix. Shared plan, eight product/two project risks, exit criteria and final GQM/completion reporting remain group obligations.

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

## Phase D test-plan and management contribution - 24 November 2026

This current section supersedes earlier inventory/pending-publication statements.
Scope: selected W1/W2 HTTP contract/generation, real persisted balances/ownership,
and Rayyan's two personal browser cases. New browser scaffolding and test-oracle
errors are being repaired by this agent before any owner handoff. Wasay retains
Area 1 and complete CI enforcement; Zain retains broad Area 3 evaluations.

Approach: highest balance/ownership risks receive separate normal-user balances,
rejection/repetition/readback, state and authorization matrices. Contract inputs
receive generated one-dimension EP and real-limit BVA with fingerprints. Browser
flows use the actual login/list/modal/form and independent HTTP/ORM readback.
Synthetic fixture setup is disposable; no production DB or credential is used.

Entry: supported runtime, unchanged application dependencies, guarded isolated
SQLite/media, fresh canonical generated data and source-backed expected result.
Suspend a dependent check on failed setup, stale data or unresolved contract;
retain raw output and continue independent tasks. Resume after a targeted fix
and fresh execution. Failed required assertions/exclusions prevent completion.

### Risk register contribution: eight product and two project risks

Likelihood and impact are provisional 1-5 assessment scores, not measured failure
probabilities or team-approved ratings. Score = likelihood * impact. Priorities:
15-25 high, 8-14 medium, 1-7 low. Residual statuses reflect observed evidence.

| ID | Type / risk | L | I | Score | Technique / control | Residual status |
|---|---|---:|---:|---:|---|---|
| A2-R01 | Product: incorrect effective balance grants excess leave | 4 | 5 | 20 | Cap/forecast/positive-duration BVA and connected state readback | Cap corrected; forecast/employee-holiday/positive-effective gaps remain |
| A2-R02 | Product: refund or access affects another employee | 3 | 5 | 15 | Distinct owner/approver/outsider, authorization table and non-owner assertions | Refund/foreign allocation fixes retested; full scope incomplete |
| A2-R03 | Product: repeated creation/approval duplicates records or effects | 4 | 3 | 12 | Repeated HTTP creation/approval plus count/balance readback | Approval guards tested; identical-pending rejection confirmed by Wasay, product correction pending |
| A2-R04 | Product: invalid terminal transition corrupts history/balance | 4 | 3 | 12 | All scoped state transitions and invalid actions per state | Wasay confirmed terminal rejection must return 400; product correction pending |
| A2-R05 | Product: stale/incomplete spec produces misleading test data | 4 | 4 | 16 | Regeneration/fingerprint checks; explicit exclusions; changed-spec experiment | Freshness passes; 399 generated IDs unconsumed |
| A2-R06 | Product: attachment boundaries cause storage failure/data loss | 3 | 3 | 9 | Generated filename BVA, file bytes, real FileSystemStorage regressions | Upload fix retested; expanded creator test correction passed its CI step |
| A2-R07 | Product: browser error/success display disagrees with stored state | 4 | 4 | 16 | Ten Playwright flows with visible and persistent assertions | Implemented; real UI verification ongoing |
| A2-R08 | Product: date/breakdown/overlap/reference inputs bypass validation | 3 | 4 | 12 | Generated EP/date BVA, 32-row BR-02 table, invalid references | Implemented subset; full contract scope incomplete |
| A2-J01 | Project: unavailable runtime/Git prevents reproduction | 4 | 5 | 20 | Free isolated CI, raw artifacts, own-account commit verification | Remote execution available; laptop dependencies/Git remain constrained |
| A2-J02 | Project: unclear oracles/ownership delays accepted evidence | 4 | 4 | 16 | Explicit oracle ledger, stable IDs, dated contribution and owner records | Two policy decisions received; strict failures and remaining team review remain |

Five-by-five matrix positions (row impact / column likelihood):

| Impact / Likelihood | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 5 | - | - | R02 | R01, J01 | - |
| 4 | - | - | R08 | R05, R07, J02 | - |
| 3 | - | - | R06 | R03, R04 | - |
| 2 | - | - | - | - | - |
| 1 | - | - | - | - | - |

IDs Rnn/Jnn abbreviate the A2- prefix. These controls contribute the required
risk population; shared acceptance and other areas' risks still need team review.

### Three measurable proposed release criteria

| Criterion | Risk link | Target | Current actual / decision |
|---|---|---|---|
| EC-1 balance correctness | R01/R02, highest product risks | Every scoped balance/refund/decision case passes twice with exact owner/readback; zero unresolved high-severity balance defects | Four corrections retested on old build; full scope/forecast/positive-duration incomplete: FAIL/HOLD |
| EC-2 contract and repeatability | R05/J01, high reproduction risk | Canonical freshness passes; all required generated input classes consumed or justified N/A; two isolated full API runs with zero failures/errors/skips | Freshness passes; 179/578 IDs referenced, 399 remaining; complete runs pending: FAIL/HOLD |
| EC-3 personal browser/regeneration | R07/R05 | Ten of ten UI flows pass visible/persistent checks; six baseline HTTP cases pass; variant yields exactly two predicted strict mismatches with zero other failures/errors/skips | Regeneration verified in 45355537997; all ten browser flows and strict report passed in 45388276537: MET for this contribution; shared acceptance and other criteria remain separate |

These are measurable proposals, not retrospective team-approved targets. Two
criteria explicitly address highest-scored risks. Other areas' release thresholds
must come from their own measured work, not these Area 2 results.

### Dated progress, GQM and effort

| Date / build | Actual progress / control action |
|---|---|
| 23 November / 2242c502 | Four reproduced corrections merged; full collection improved to 176/178, two disputed oracles retained |
| 24 November / b848025 | Expanded subset 172/177; diagnosed all five new failures as an incorrect optional creator-FK assertion |
| 24 November / 8a9ca964 | Corrected creator oracle, implemented regeneration and ten UI flows, published actual sources and independent evidence |
| 24 November / first D browser | Ten setup errors exposed a sync Playwright/Django event-loop conflict; converted browser lifecycle to async API plus sync_to_async ORM reads, preserving safety guards |

GQM goal: expose and reduce balance/ownership/contract risk using reproducible
assertions. Questions: does each owned transition preserve the right balances;
does generated output follow supported spec edits; do UI outcomes match state?
Metrics: accepted FRs/10 remains undetermined, not 10/10 inferred from test tags;
implemented generated references 179/578=30.97% (inventory only); old full-build
API pass fraction 176/178=98.88% (run-specific, not release readiness); current
independent checks 49/49; browser verified pass fraction awaits actual results.
Confirmed-defect Pareto population is four; density needs a measured size and
reopen rate needs real closed/reopened lifecycle counts, both unavailable.

No original D pre-implementation estimate or trustworthy human timesheet is
available. Do not invent either or replace them with CI duration. For remaining
runtime debugging/report finalization only, current provisional forecast is
O=1, M=3, P=6 hours, PERT=(1+4*3+6)/6=3.17 hours; this is a forecast made after
implementation began, excludes queue/access delays and requires revision after
new evidence. Human actual-vs-original-estimate variance remains unavailable.
No fictional weekly history or team signoff is backfilled.

Existing defect-risk aliases are preserved: A2-R-BALANCE maps to A2-R01,
A2-R-OWNERSHIP to A2-R02, A2-R-DUPLICATE to A2-R03, A2-R-STATE to A2-R04 and
A2-R-CONTRACT to A2-R05. Earlier evidence remains linked; no FR/BR ID changes.


## Final same-source Phase D verification - 24 November 2026

Source 7189656a / run 45388276537 completed both D jobs successfully. Browser:
all ten flows passed, strict HTML completion report passed, artifact 14917252664.
Regeneration: job 138424862957 retained baseline six passes, variant four passes
and exactly two predicted strict failures, zero errors/skips and genuine variant
exit one; experiment_demonstrated true. Current raw log and labelled summary are
ci-45388276537-regeneration-passed.log and regeneration-current-verified-summary.json
under docs/team/evidence/area2/phase-d/. These results complete this personal
contribution's EC-3 evidence; overall required scope and group release remain HOLD.
