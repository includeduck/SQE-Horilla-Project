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
47 generator/catalog/runner/experiment integrity checks passed independently.

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

Actual HTTP outcomes remain pending until the linked runtime jobs complete.
The manifest/raw logs/XML must be inspected before replacing this statement.
No baseline restore mutation is needed because canonical files were never edited;
normal freshness/default commands still target canonical openapi.json/data.
