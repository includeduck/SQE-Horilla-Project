# Phase D implementation status

24 November 2026. Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B.

## Current decision

Rayyan's implemented Phase D browser and regeneration contributions are
verified; the local source/report/evidence/viva handoff is supplied. Overall
Area 2 and group release remain **HOLD**. This is not certification that all
A-C scope, human review, group gates or final submission are complete.

Published implementation checkpoint:
`7189656a7b118565f42004770ff9a9f8bbcd3a09` in draft PR #8, with verified
rayyanhasan899 author and committer. It inherits browser correction ac32aaab
and the product fixes 32621b42 / bf44fe6c. The laptop's preserved Git HEAD is
still da76b337 plus working files; no local pull/reset or synchronized .git
archive is claimed.

| Population / requirement | Actual observed result | Interpretation |
|---|---|---|
| Independent generator/catalog/runner/report checks | 49 passed locally, no failures/skips; canonical freshness passed again | Tooling integrity, separate from application execution |
| Controlled two-constraint HTTP regeneration | Current source 7189656a / run 45388276537: baseline 6 passed; variant 4 passed and exactly 2 predicted strict failures, no errors/skips | Both D jobs completed successfully on the same source; variant pytest exit 1 retained |
| Two personal browser use cases / all ten flows | Run 45388276537, job 138424862639 on source 7189656a: **10 passed**, 26 warnings, 340.34 seconds; job and strict HTML completion report succeeded | Actual UI plus visible and persistent assertions; all declared flows executed |
| Blank allocation-amount defect A2-D10 | Unchanged UC-RAY-01-E2 passed after bf44fe6c; all four other allocation flows passed too | Real failing-before/passing-after browser evidence |
| Owner-confirmed duplicate/terminal API fixes | Source 32621b42: 16 focused passes and full first-order 275/275 passes in 45355537962 | Strict 400 and unchanged-state assertions retained; no xfail |
| Separate affected/expanded API populations | Same run: 8 upstream, 177 expanded and 1 preflight passed | Overlapping populations; do not add to the 275 unique-case count |
| Full/reversed API producer | First order passed; reverse cancelled at the 90-minute job limit. 7189656a raises budget to 120 minutes; run 45388276552 is pending | No twice/order-independent or complete-scope acceptance |
| Reports, evidence, risk/GQM/RCA, AI and viva | Supplied and reconciled to actual results; seven-defect Pareto update separately labelled | Contribution delivered; human/group acceptance not inferred |
| Relevant-PR wiring | Area 2 and D jobs actually run for PR #8 targeting sqe-team | Whole Sonar/mutation/required merge/deploy gate remains a separate owner obligation |

Browser artifacts: [run 45388276537](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45388276537),
[artifact 14917252664](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45388276537/artifacts/14917252664).
The artifact retains actual browser.xml, browser.html, browser.txt, ten
screenshots and ten traces. Retained decoded job log:
`../evidence/area2/phase-d/ci-45388276537-browser-passed.log`.
`browser-verified-summary.json` is explicitly derived from that genuine log;
it does not masquerade as downloaded JUnit.

## Prerequisites and repairs

The protected target is 2242c502; PR #8 remains draft/open and unmerged.
Earlier C runs exposed four genuine merged fixes and two failing policy cases.
The owner's published OD-01/OD-02 decisions were retrieved rather than requested
again. This agent implemented pending-duplicate and terminal-cancelled rejection
guards and verified their strict regressions. Sequential API duplicate rejection
is not a claim of concurrent idempotency or a new UI-wide uniqueness policy.

Expanded attachment tests initially used the wrong creator-FK oracle:
LeaveRequest overrides the base HorillaUser field with an optional Employee FK.
The source-backed helper correction preserves owner, identity, count and actual
file-byte checks. The 177-case expanded retest passed. No production change was
made to satisfy that mistaken audit-field expectation.

Browser iterations repaired async Playwright/Django ORM handling, the active
theme's login control, normal-user hidden employee binding, missing-type
interaction and active CBV Create navigation. Active CBV navbars use anchors;
tab toolbars may use buttons. The final selector operates a visible route
control and excludes the theme's hidden floating shortcut. The intermediate
button-only selector was this agent's harness regression; its ten failures are
retained, not counted as ten product defects.

A2-D10 was a genuine product defect: blank requested_days created a pending
allocation with None days. Only the individual form's field requiredness was
corrected, consistent with the API/bulk form. No invented positive minimum,
maximum, model migration, authentication bypass or production password change
was introduced.

## Two-constraint before/after demonstration

| Input in SelfAllocationCreate | Canonical constraint / BVA | Experimental constraint / BVA | Predicted and observed HTTP effect |
|---|---|---|---|
| description after trimming | minLength 1; lengths 0/1/2 | minLength 3; lengths 2/3/4 | Length 2 still accepted by unchanged server; strict variant below-minimum assertion fails |
| attachment filename | Budget 100; lengths 99/100/101 | Budget 80; lengths 79/80/81 | Filename 81 still accepted by unchanged server; strict variant above-maximum assertion fails |

The same generator derives baseline/variant values from separate specs;
18 affected generated IDs and unaffected cases are listed in comparison.json.
Stale canonical output against the variant was genuinely rejected. Canonical
spec/data were never edited and their default freshness command still passes.

Canonical spec SHA-256:
`45e37bfbcd255fc567d5923b13076637f8777bbc4c48bb239f6c2e3fe398f0db`.
Canonical data SHA-256:
`38d69c57a2e33ede9682bb8b6b165d7c1398b578711983ecf05cd3f8e59e3521`.
Variant spec SHA-256:
`769fa6b449a3f8f9970a74c182b80e1db0e95ede2a36342b74d287583d61c16a`.

The strict consumer uses real normal-role HTTP with fresh disposable data.
Only the two predicted failed IDs, baseline exit zero, variant exit one and
zero other failures/errors/skips satisfy the experiment driver. Successful
demonstration does not mean the server implements the hypothetical variant.
Detailed reproducible comparison and logs are in the evidence index and
REGENERATION_DEMONSTRATION.md.

## Personal flow accounting

| Use case | MAIN | A1 | A2 | E1 | E2 |
|---|---|---|---|---|---|
| UC-RAY-01 allocation | Passed | Attachment passed | Correct missing description and resubmit passed | Missing type rejected | Blank amount rejected |
| UC-RAY-02 leave | Three-day request passed | Half-day request passed | Insufficient balance then correction passed | Insufficient balance rejected | Reversed dates rejected |

Each flow asserts displayed outcome plus persisted ownership/count/state/
amount/balance as applicable; file flow also reads actual stored bytes.
HTTP/ORM prepare or corroborate data while the target write uses real forms.
These ten browser cases are separate from 275 API cases and 49 tooling tests.
Zain's broad keyboard/Lighthouse/axe/security/k6/recovery evaluations are not
certified by these personal flows.

## Files and repeatable commands

Created/extended sources: tests/team/e2e fixtures/tests; generator experiment
and strict regeneration consumer; run_phase_d.py; browser_report.py plus
integrity checks; scoped dependency/URL/settings files; Area 2 and D workflows.
Source corrections: leave/forms.py, API leave serializer/view guards, alongside
the earlier refund/carry-forward/storage corrections. Reports/specifications,
risk/GQM/RCA/evidence/viva/disclosure and package inventory are under docs/team.
Canonical spec/data stay unchanged. The final manifest records published Git
blob identities rather than stale laptop newline-dependent byte hashes.

In a complete application environment, install the unchanged root application
requirements with the existing Linux installation helper, then:

```sh
python -m pip install -r tests/team/requirements-phase-d.txt
python -m playwright install --with-deps chromium
python -W error::ResourceWarning -m unittest discover -s tests/team/generator -p 'test_*.py' -v
python tests/team/generator/generate.py --spec tests/team/generator/openapi.json --bindings tests/team/generator/bindings.json --output tests/team/generator/generated_cases.json --check
python tests/team/run_phase_d.py --evidence docs/team/evidence/area2/phase-d/run-UNIQUE-ID
python -m pytest -c tests/team/pytest-area2.ini tests/team/e2e -v -s -o junit_family=xunit1 --junitxml=browser.xml
python tests/team/browser_report.py --junit browser.xml --output browser.html
python tests/team/run_area2.py --evidence docs/team/evidence/area2/run-UNIQUE-ID
```

Use new evidence directories. Set AREA2_BROWSER_EVIDENCE to retain synthetic
screenshots/traces. On Windows use the selected Python executable and install
Chromium without Linux's --with-deps option. The laptop remains dependency/
network constrained; no local Django/API/browser pass is claimed. Real results
above are free isolated GitHub Actions execution, not tests against user data.

Verified runtime: Python 3.12.16, Django 5.2.19, DRF 3.18.3, pytest 9.2.0,
pytest-django 4.14.0, Requests 2.34.2, Playwright 1.65.2, pytest-asyncio 1.5.0.
Local syntax compilation and git diff --check passed; they are not HTTP tests.

## Remaining mandatory execution and readiness

Current inventory is 275 API scenarios, 179/578 generated IDs referenced and
399 unconsumed; accepted FR numerator over ten is not established. Further
live contract/media/normalization/balance/holiday/forecast/reason scope,
complete reversed/full-scope acceptance, product-Issue lifecycle/group triage,
overall every-PR Sonar/all-tests/mutation gates and required merge/deploy
enforcement remain open. Classic protection reads returned 403; no enforcement
or absence of protection is inferred.

The supplied eight-product/two-project risk register and three measurable
criteria remain proposals pending genuine shared acceptance. EC-3's ten-browser
plus controlled-regeneration evidence is now met for this contribution;
EC-1/EC-2 remain unmet due to required scope and repeatability gaps. The updated
seven-defect Pareto and two source-backed major-defect RCAs are contributions,
not fictional human meetings, signoff, hours or passed viva.

Wasay / his agent has Rayyan's explicitly mandatory carryover in
PHASES_A_D_REMAINING_CHECKLIST.md and handoff.md; Zain retains specialist scope.
The final combined PDF/ZIP with synchronized .git and all areas remains shared
work. Confirm the section token before final submission naming. Rayyan's
personal understanding/AI review/viva cannot be delegated or certified by an
agent. Phase D personal execution and handoff are distinct from group release.
