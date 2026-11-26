# Controlled two-constraint regeneration demonstration

This experiment changes two existing constraints in a variant only. It does
not propose or implement new production rules. Owner: Syed Muhammad Rayyan
Hassan, 24I-3000. Date: 24 November 2026.

| Input | Actual baseline constraint | Experimental value | Baseline BVA | Variant BVA |
|---|---|---|---|---|
| Self-allocation description | minLength 1 after trimming, from DRF nonblank text | minLength 3 | 0 / 1 / 2 characters | 2 / 3 / 4 characters |
| Self-allocation attachment | inherited FileField filename budget 100, introspected in fixture | budget 80 | 99 / 100 / 101 characters | 79 / 80 / 81 characters |

The generator reads each spec and produces its data without a hardcoded case
rewrite. Case IDs stay stable; comparison.json records changed request values,
boundary units/limits, provenance, predicates and unaffected cases. Only the
self_allocation_create operation should change. Baseline and variant spec/data
fingerprints differ; the same logical bindings are used independently of the
runtime-bound employee/type IDs recorded in JUnit.

Independent command actually executed:

```sh
python tests/team/generator/demonstrate_regeneration.py --output docs/team/evidence/area2/phase-d/independent-regeneration-20261124
```

It returned exit zero and actually rejected old generated data against the
variant spec. It also verified the canonical baseline remains unchanged.
49 generator/catalog/runner/experiment/report integrity checks passed independently.

Real HTTP consumption command:

```sh
python tests/team/run_phase_d.py --evidence docs/team/evidence/area2/phase-d/run-UNIQUE-ID
```

The existing normal-role Requests/live-server fixtures bind each spec's values
to a fresh disposable database. Six strict tests run against baseline, then six
against variant. Expected baseline: six passes. Expected variant: four passes
and two real failures: description below-minimum length two and above-maximum
filename 81. The unchanged server accepts both, proving that editing the spec
changes generated expectations without changing server behavior.

The variant pytest command retains exit one and its failed assertions. The
experiment driver accepts only the exact two predicted case IDs with six cases,
zero setup errors/skips and baseline exit zero. An unexpected failure makes the
demonstration fail. This is not xfail, a disabled test, a green application gate
or evidence that production now enforces the hypothetical limits.

The verified real HTTP outcomes are recorded below from completed job logs;
current reruns have their own source identity and must be assessed separately.
No baseline restore mutation is needed because canonical files were never edited;
normal freshness/default commands still target canonical openapi.json/data.

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
