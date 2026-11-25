## Verified Prompt 3 result — 25 November 2026

This source-specific result supersedes historical incomplete-input, pending-retest
and unanswered OD-01/OD-02 labels below. On `fecac354c9b5d8ea47ac732a2b089ed3cc148620`,
[run 45609322121](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322121) passed **3,433/3,433 API
cases in EACH independent order**, with no failures, errors, required skips or
missing IDs. The strict complete-scope guard accepted both orders.
**713/713 canonical generated IDs, all former 399 missing IDs, and 350/350
mandatory input families are verified.** Explicit requirement assertion selectors
verify FR-01–FR-10 and BR-01–BR-04; tags or mappings alone are not the evidence.

The authoritative source-bound summaries and individual rows are in
`docs/team/finish-line/PROMPT03_EXECUTION_SUMMARY.json`,
`PROMPT03_REQUIREMENT_EVIDENCE.json`, `PROMPT03_INPUT_LEDGER.json` and
`REMAINING_WORK.json`. The derived complete coverage, case-execution and generated-ID
ledgers remain in [artifact 15024156843](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45609322121/artifacts/15024156843).

Separate overlapping populations on the same source passed: 482 business/state/
role/workflow cases; 82 affected upstream tests; 24 original team units; 16
focused regressions; eight focused upstream tests; 182 expanded cases; 238 wire
validation cases; seven advanced-filter cases; 27 further upstream tests plus
two subtests; all ten personal browser flows; two fresh foundations with five
smoke cases each; 68 tooling and four media-reader checks. Regeneration passed
six baseline cases and retained exactly two predicted strict variant failures
with four passes, in its separate controlled experiment. These totals are not
added into a larger unique-case count.

Prompt 3's scoped technical work is complete. **Whole-project release remains
HOLD** pending accepted integration, owner/shared quality gates and Prompt 4's
final integrated/report/package/ownership closeout. PR #8 remains draft/open;
no owner approval, merge, human effort, review or viva is inferred.

---

Historical dated records and implementation detail follow.

# Area 2 completion contribution

24 November 2026. Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B.

## Recommendation and scope

**HOLD.** This is the Area 2 contribution to the shared report, not a completed
group submission or acceptance of A-D. W1 allocation and W2 leave consumption
share AvailableLeave. Upstream Horilla 2.4.0 baseline:
`6c15617b8297b7a6775daa6c29aefcc48b1eb29f`, LGPL-2.1. Scope/FR-01 through FR-10
and BR-01 through BR-04 remain in SCOPE.md; actual acceptance limitations are explicit.

## Tested and implemented scope

| Population / build | Actual observed result | Meaning and limitation |
|---|---|---|
| Independent tooling after D implementation | 49 passed, no failures/skips | Generator, ledger, producer failure handling and experiment integrity; not product API execution |
| Merged build 2242c502 / run 45197384096 | 14 focused passes; eight separate upstream passes; full API 176 passed / two failed / 178 | Four reproduced corrections retested; two strict failures on that historical build; owner decisions/fixes now supplied |
| Expanded build b848025 / run 45342013246 | 14 focused passes; eight upstream passes; expanded subset 172 passed / five failed / 177 | Five attachment assertions used the wrong creator-field type; source-backed test correction now proposed |
| Owner-rule fixes / source 32621b42 / run 45355537962 | 16 focused, 8 upstream, 177 expanded, 1 preflight and 275/275 full first-order passes | Separate overlapping populations; reversed collection cancelled at the 90-minute job limit, so twice/order acceptance remains incomplete |
| D independent controlled generation | Two existing constraints changed; new fingerprints; stale output rejected; canonical files unchanged | Real generated output, not yet proof of consuming HTTP results |
| D baseline/variant HTTP / run 45348178607 | Six baseline passed; variant four passed / exactly two predicted strict failures; zero errors/skips | Verified controlled regeneration/consumption demonstration; variant pytest exit 1 is retained |
| Personal browser use cases / source 7189656a / run 45388276537 | All 10 passed, zero failures/errors/skips; strict completion report succeeded | Two personal use cases, five declared flows each; visible result plus persistent assertions verified; artifact 14917252664 |

Do not add focused/upstream/preflight counts to the unique API denominator.
Current API source inventory: 275 executable cases; 179 distinct generated IDs
referenced out of 578; 399 explicitly unconsumed. Contract: OpenAPI 3.0.3 JSON,
27 operations, 71 operation/input entries. Each test-level case is counted once.
Generated-ID reference rate is 30.97%; it is not requirement coverage or pass rate.
Full FR coverage numerator is not yet established over the ten selected FRs.

## Requirement traceability and remaining verification

| Requirement | Implemented assertion families | Acceptance limitation |
|---|---|---|
| FR-01 | Generated allocation creation/update/file inputs and W1 HTTP/browser cases | Remaining generic/input categories and new-build results |
| FR-02 | Allocation approval state/role cases and W1-to-W2 integration | Full accepted scope/repetition evidence |
| FR-03 | Allocation rejection and approved reversal state cases | Final reversal oracle and complete matrix review |
| FR-04 | Requested-only updates/deletes and generated self-update cases | New-build complete execution and remaining generic updates |
| FR-05 | Generated leave create/update/file inputs and UC-RAY-02 flows | Browser results and remaining generic/input categories |
| FR-06 | Insufficient balance, carry cap and connected workflow readback | Positive effective duration, employee holidays, forecast and complete boundary combinations |
| FR-07 | Overlap rejection, duplicate leave and BR-02 table | Full remaining combinations/reference/state binding |
| FR-08 | Approval truth table, transition/repetition and persistent debit | Full scope/current-build results |
| FR-09 | Rejection/refund and cancellation decisions | Owner-confirmed terminal guard passed focused/full-first retests; complete-scope and reversed acceptance remain open |
| FR-10 | HTTP balance readback throughout, separate user balances | Complete current-build API/browser evidence |

## Defects, corrections and residual risks

Reproduced A2-D01 wrong-requester refund, A2-D02 foreign-owner allocation
PUT/DELETE crash, A2-D03 uncapped carry-forward and A2-D09 extensionless upload
storage failure were corrected in merged PR #2 and retested. Source-backed RCA
for two major defects and a four-defect Pareto are in AREA2_RCA_CONTRIBUTION.md.
Product-Issue lifecycle/triage integration remains unverified.

Wasay's published SCOPE OD-01/OD-02 and issue #1 comment confirm 400 for
identical pending allocation and cancelled-to-rejected refusal. Both narrow
product fixes are implemented here with unchanged strict regressions. Focused
and full 275-case first-order collections passed in run 45355537962; the reversed
collection was cancelled at the 90-minute job limit. Source 7189656a increases
that limit to 120 minutes without suppressing failures. Their earlier
unresolved-decision labels are historical. A2-D06 positive allocation
policy, A2-D07 positive effective duration/employee holiday/forecast and A2-D08
reason normalization/persistence are questions/candidates requiring further
evidence, not fabricated corrected defects. Retained failing evidence is linked
in AREA2_DEFECTS.md. The five expanded attachment failures are a separate test
oracle mistake, not five product defects.

Risk scores, proposed criteria and per-risk residual status are in
../AREA2_MANAGEMENT.md. Current missing input coverage, remaining balance-rule candidates
and incomplete repeatability/group gate evidence prevent overall release. Personal
browser/regeneration contribution is verified. Test elapsed times
are not human effort; retrospective hours, estimates and team signoff are not
invented. Density/reopen metrics remain unavailable without defined populations.

## Reproduction and evidence

Install unchanged application requirements, then tests/team/requirements-phase-d.txt.
Use the existing Linux installation helper for the spaCy wheel. Run:

```sh
python -W error::ResourceWarning -m unittest discover -s tests/team/generator -p 'test_*.py' -v
python tests/team/run_area2.py --evidence docs/team/evidence/area2/run-UNIQUE-ID
python tests/team/run_phase_d.py --evidence docs/team/evidence/area2/phase-d/run-UNIQUE-ID
python -m playwright install --with-deps chromium
python -m pytest -c tests/team/pytest-area2.ini tests/team/e2e -v -s -o junit_family=xunit1 --junitxml=browser.xml
```

On Windows use the chosen Python executable (the laptop currently has 3.14.7
without test/application dependencies). The working free remote runtime uses
Python 3.12 and installs requirements unchanged; exact versions belong to each
job log, not an assumed global environment. Every evidence directory must be
new; temporary DB/media do not reset the user's existing database.

See AREA2_EVIDENCE_INDEX.md, RAYYAN_USE_CASES.md, AREA2_VIVA_REHEARSAL.md,
AREA2_CI_HANDOFF.md and SQE_IMPLEMENTATION_PHASE_D_STATUS.md. PR #8 is draft/open;
new CI jobs were launched on 8a9ca964. The overall every-PR Sonar/all-tests/mutation
merge/deployment gate is Wasay's group integration, not certified by scoped jobs.

## Shared submission contribution

Supply these reports, source, generated baseline data, experiment script,
specifications, actual run artifacts and disclosure to the shared PDF/ZIP.
Proposed group names remain Project_24I-3071_24I-3000_24I-3130_B.pdf/.zip, pending
section-token confirmation. Include .git from a synchronized final checkout;
the laptop's outdated Git HEAD must not be packaged as complete remote history.
Do not fabricate Wasay's Sonar/mutation, Zain's specialist evaluations or missing
results. Full group packaging depends on those actual contributions.

## Verified real HTTP regeneration result - 24 November 2026

Run 45348178607, regeneration job 138287747685 on source 8a9ca964, completed
successfully. Six strict baseline HTTP cases passed. The variant produced four
passes and exactly two genuine failed strict assertions, with pytest exit one:
`self_allocation_create:body:description:BVA:minLength-below` and
`self_allocation_create:body:attachment:BVA:x-filename-maxLength-above`.
The driver inspected exact failed IDs and zero errors/skips and recorded
experiment_demonstrated true. This is the predicted spec/server mismatch, not
an assertion that production enforces the hypothetical stricter spec.
Raw job output: docs/team/evidence/area2/phase-d/ci-45348178607-regeneration.log.
The canonical spec/data remain unchanged. This independently completes the
controlled regeneration/consumption demonstration; browser verification and
whole Area 2 acceptance remain separate.


## Final same-source Phase D verification - 24 November 2026

Source 7189656a / run 45388276537 completed both D jobs successfully. Browser:
all ten flows passed, strict HTML completion report passed, artifact 14917252664.
Regeneration: job 138424862957 retained baseline six passes, variant four passes
and exactly two predicted strict failures, zero errors/skips and genuine variant
exit one; experiment_demonstrated true. Current raw log and labelled summary are
ci-45388276537-regeneration-passed.log and regeneration-current-verified-summary.json
under docs/team/evidence/area2/phase-d/. These results complete this personal
contribution's EC-3 evidence; overall required scope and group release remain HOLD.
