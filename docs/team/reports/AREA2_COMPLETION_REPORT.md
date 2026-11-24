# Area 2 completion contribution

24 November 2026. Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B.

## Recommendation and scope

**HOLD.** This is the Area 2 contribution to the shared report, not a completed
group submission or acceptance of A-D. W1 allocation and W2 leave consumption
share AvailableLeave. Upstream Horilla 2.4.0 baseline:
`6c15617b8297b7a6775daa6c29aefcc48b1eb29f`, LGPL-2.1. Scope/FR-01 through FR-10
and BR-01 through BR-04 remain in SCOPE.md; unresolved oracles are explicit.

## Tested and implemented scope

| Population / build | Actual observed result | Meaning and limitation |
|---|---|---|
| Independent tooling after D implementation | 47 passed, no failures/skips | Generator, ledger, producer failure handling and experiment integrity; not product API execution |
| Merged build 2242c502 / run 45197384096 | 14 focused passes; eight separate upstream passes; full API 176 passed / two failed / 178 | Four reproduced corrections retested; duplicate and cancelled-to-rejected oracles unresolved |
| Expanded build b848025 / run 45342013246 | 14 focused passes; eight upstream passes; expanded subset 172 passed / five failed / 177 | Five attachment assertions used the wrong creator-field type; source-backed test correction now proposed |
| D independent controlled generation | Two existing constraints changed; new fingerprints; stale output rejected; canonical files unchanged | Real generated output, not yet proof of consuming HTTP results |
| D baseline/variant HTTP | Implemented, runtime pending | Predict six baseline passes and exactly two strict variant failures caused by spec-only disagreement |
| Personal browser use cases | Two specifications, ten implemented flows, runtime pending | Main + two alternatives + two exceptions each; UI and persistent assertions need actual verification |

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
| FR-09 | Rejection/refund and cancellation decisions | Terminal-state oracle remains unresolved |
| FR-10 | HTTP balance readback throughout, separate user balances | Complete current-build API/browser evidence |

## Defects, corrections and residual risks

Reproduced A2-D01 wrong-requester refund, A2-D02 foreign-owner allocation
PUT/DELETE crash, A2-D03 uncapped carry-forward and A2-D09 extensionless upload
storage failure were corrected in merged PR #2 and retested. Source-backed RCA
for two major defects and a four-defect Pareto are in AREA2_RCA_CONTRIBUTION.md.
Product-Issue lifecycle/triage integration remains unverified.

A2-D04 allocation duplicate identity/response and A2-D05 cancelled-to-rejected
terminal policy still require business reconciliation. A2-D06 positive allocation
policy, A2-D07 positive effective duration/employee holiday/forecast and A2-D08
reason normalization/persistence are questions/candidates requiring further
evidence, not fabricated corrected defects. Retained failing evidence is linked
in AREA2_DEFECTS.md. The five expanded attachment failures are a separate test
oracle mistake, not five product defects.

Risk scores, proposed criteria and per-risk residual status are in
../AREA2_MANAGEMENT.md. Current missing input coverage, unresolved money-like
balance rules and unverified browser flows prevent release. Test elapsed times
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
