## Final execution closeout — 25 November 2026

Rayyan's project execution assignment is finished. **Whole-project release: HOLD.** No further technical execution or additional prompt is expected from Rayyan.

The final application/API verification source is `aeed7b7ba049a79589b8e9ac0b4abb52bec28d0e`; Actions checked synthetic merge `801351079aada8c399db2212d9c033737e032e0d` with `sqe-team` base `0a5ac6443dadb50ab5fd6ea749f41dd108a19486`. [Run 45627793460](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45627793460) verifies **3,433/3,433 API cases in each of two orders**, with zero failures/errors/skips/missing IDs and strict complete-scope acceptance. Each collection is the exact union of 16 fresh isolated deterministic shards; reversal occurs within each shard, not a claim of one monolithic reversed process.

**713/713 generated IDs, all former 399 missing IDs, 350/350 mandatory input families, FR-01–FR-10 and BR-01–BR-04 are verified** from real source-bound assertions. Ten personal browser flows pass; the consuming regeneration has six baseline passes and exactly two predicted strict variant failures with four passes. Separate overlapping populations and full links are in [RAYYAN_FINAL_CLOSEOUT.md](reports/RAYYAN_FINAL_CLOSEOUT.md), the final evidence index and machine ledger. Never sum them into a fictitious unique-test total.

All remaining project execution is **Wasay / Wasay's agent — mandatory**, with exact attempts, dependencies and acceptance in root [handoff.md](../../handoff.md) and `finish-line/REMAINING_WORK.json`. Current shared gate evidence is genuinely red for missing Sonar service/credentials and mutation runner/policy; supplied units pass. No independent review, merged PR #8, required branch/deploy enforcement, teammate authorship, human effort or passed viva is inferred.

The PDF/ZIP is a **Rayyan contribution, not the final group submission**. Earlier dated results/ownership below are historical and superseded by the final handoff; they do not assign new execution to Rayyan.

---

### Evidence to explain personally

Explain distinct requester/actor fixtures, refund split/current cap, dates/holiday/breakdown/reason oracles, generated identity versus executed case, complete guards, isolated shard reversal, and why two predicted variant failures establish real consumer disagreement rather than app compliance. Show actual source/fix/run/XML/screenshots. This is preparation, not evidence of a human review or passed viva; personal assessment cannot be delegated or certified by an agent.

---

## Historical dated appendix (not current ownership or pending work)

# Area 2 viva rehearsal

Syed Muhammad Rayyan Hassan, 24I-3000. This is a practice script, not a claim that
Rayyan has completed a human review or passed the viva.

## Explain the shared record and selected test

W1 allocation approval adds five days to AvailableLeave(employee, leave_type).
W2 creates three-day leave, approval deducts three, and another non-overlapping
three-day request is rejected while balance remains two. Requested leave has
not consumed balance until approval. Explain why checking only HTTP 200 cannot
prove the right employee received a credit/refund.

```sh
python -m pytest -c tests/team/pytest-area2.ini tests/team/api/test_workflows.py::test_w1_to_w2_shared_balance -v -s
```

Identify the generated valid baseline, runtime-bound employee/type IDs, real JWT
roles, allocation/leave record IDs and HTTP list/detail/balance assertions.
`area2_settings` owns a unique temporary SQLite/media directory; fixtures guard
the module marker/engine/path and reset each case. Three distinct normal users
expose wrong-owner changes. Setup admin is not the rule-test actor.

## Predict a supported spec change before running it

The canonical contract has a nonblank trimmed description minimum one and
filename maximum 100. The experiment tightens only SelfAllocationCreate's
description minimum to three and filename maximum to 80. Its boundaries become
2/3/4 description characters and 79/80/81 filename characters. The unchanged
server still accepts description two and filename 81, so two strict variant
assertions must fail. A schema edit does not alter the application.

```sh
python tests/team/generator/demonstrate_regeneration.py --output docs/team/evidence/area2/viva-UNIQUE-ID
python tests/team/run_phase_d.py --evidence docs/team/evidence/area2/viva-http-UNIQUE-ID
```

The second command creates its own experiment directory. Inspect comparison.json,
baseline.xml, variant.xml and experiment-manifest.json. Explain all three
fingerprints: spec identifies the contract, bindings identify synthetic runtime
inputs, data identifies the entire deterministic generated artifact. `verify_fresh`
regenerates and compares, so changing the spec while keeping old data is rejected.

The demonstration runner succeeds only if baseline is 6/6 and variant produces
exactly the two predicted failures, no errors/skips, and actual pytest exit one.
That success certifies the experiment, not application compliance with the
hypothetical stricter spec. Any different failure must remain a failing check.

## Rehearse an instructor-provided edit

Copy the spec into a fresh temporary experiment folder; edit a supported existing
constraint; predict affected operation/input IDs, EP acceptance and below/at/above
values. Run `generate.py` with explicit --spec/--bindings/--output arguments.
Run --check against the old output first and explain its nonzero stale-data exit;
regenerate, then --check the new output. Unsupported constraints must fail visibly,
not be ignored. Never invent a production amount maximum or silently delete
coverage exclusions to turn the complete-scope gate green.

Canonical commands must still pass freshness afterward:

```sh
python tests/team/generator/generate.py --spec tests/team/generator/openapi.json --bindings tests/team/generator/bindings.json --output tests/team/generator/generated_cases.json --check
```

## Explain defects, coverage and limits

- A2-D01: the actor and record owner differ. Refund belongs to the requester;
  assertions compare requester, approver and outsider balances.
- A2-D03: stored carry-forward is not always the usable amount. Policy/cap can
  make raw stored five mean effective one. Forecast/holiday gaps remain separate.
- Explain the LeaveRequest optional Employee created_by override versus the
  allocation/base HorillaUser audit field; do not confuse either with owner FK.
- 275 API scenarios and ten browser flows are different test-level populations.
  179/578 generated IDs referenced is implementation inventory, not requirements
  coverage, application code coverage or pass rate.
- Owner-confirmed duplicate/terminal fixes passed strict focused/full-first
  retests in run 45355537962; reversed order was cancelled at the job limit;
  required unexecuted coverage still means Hold.
  An enabled failing test is evidence, not a reason to weaken its assertion.
- Wasay owns the complete Sonar/unit/mutation gate. A scoped workflow or draft
  failing PR does not alone prove protected merge/deployment enforcement.

Human practice: explain one test without reading its code, predict one changed
constraint, locate genuine evidence and explain the residual risks. Record actual
review/checks in AI_USE_RECORD.md; no other agent can provide that human evidence.
