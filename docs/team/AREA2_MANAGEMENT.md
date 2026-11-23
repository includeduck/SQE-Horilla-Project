# Area 2 activity and management contribution

Syed Muhammad Rayyan Hassan, **24I-3000**, 23 November 2026.

## Current control decision

**Hold Phase B completion.** Independent generator implementation can proceed; missing Phase A recovery and the unavailable application/tool environment prevent accepting HTTP integration or all-input coverage. Do not start Phase C automatically.

The current work follows the supplied B prerequisite-repair provision. No application handler/model/seed, Wasay unit/CI module, or Zain browser/security/performance/recovery module was changed. All implementation code is under `tests/team/`.

## Measurable activity and effort

The B status report and `evidence/area2/phase-b/` record actual test counts, command exits, tool versions and generated fingerprints. Generated case counts measure available data, not API cases executed or requirement coverage. HTTP execution remains zero until the real server tests run.

No reliable start/end time sheet or original A estimate is available locally. Overall actual hours and estimate-versus-actual variance are unknown. Test elapsed seconds in raw logs are tool execution durations, not Rayyan's human effort. No retrospective pre-implementation estimate, weekly report or human review is invented.

For **remaining B verification only**, a provisional forecast after package/runtime access is restored is O=1, M=2, P=4 hours, PERT=(1+4×2+4)/6=2.17 hours. This is an unapproved future-work estimate made after the implementation began, excludes waiting/access delay, and must be revised if runtime failures require more work. Group-wide estimation remains shared.

## Risk-based priorities

| Risk | Likelihood × impact, provisional 1–5 | Control / verification |
|---|---|---|
| Untested contract assumptions produce misleading passing tests | 4×5=20 | Label source-only assumptions, introspect serializers, run real HTTP and inspect state. |
| Missing dynamic business inputs hide balance/ownership defects | 4×5=20 | Preserve incomplete coverage, recover A basis, bind C scenarios and compare both users' state. |
| Environment/access failure prevents reproducible submission | 5×4=20 | Maintain logs, owner handoffs and exact commands; do not claim remote delivery. |
| Accidentally resetting an existing local DB | 2×5=10 | Dedicated settings with absolute temporary SQLite/media paths; fixture asserts the DB parent before seeding. |

These are Area 2 risk contributions, not the assignment's completed group risk register or approved 5×5 matrix. Shared plan, eight product/two project risks, exit criteria and final GQM/completion reporting remain group obligations.

## B entry / exit / suspension / resumption

Generator entry: source-readable spec, explicit supported dialect and deterministic nonsecret bindings. Generator verification exit: focused tests pass, repeated bytes match, unsupported constraints and staleness fail, case lineage remains inspectable.

B completion exit additionally requires formally validated/reviewed contract and the five genuine HTTP consumer cases, correct field errors/state/ownership/balance readback, and a repeat run in a different order. Those acceptance conditions remain unverified. A valid generator run alone does not release this gate.

Suspend dependent HTTP work when packages, engine, schema defaults or an oracle are unavailable. Resume after obtaining a permitted environment, installing unchanged application requirements plus scoped test tools, validating the contract and rechecking A isolation. Keep original failures and record fixes; never replace them with invented results.

## Ownership handoff

Wasay: repository write/access route, available compatible runtime or original A archive, and CI command/required-check coordination. Rayyan retains generator/HTTP fixes and reruns. Zain retains Area 3; the B harness can later be shared without replacing his work. `Communication.md` records delivery state; local notes are not proof that a teammate received them.
