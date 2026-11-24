# Area 2 evidence index

24 November 2026. Relative repository paths below are real retained files or
explicit CI artifact locations; pending runtime output is labelled separately.

| Evidence | Location / source | Establishes |
|---|---|---|
| Baseline contract and generated data | tests/team/generator/openapi.json, bindings.json, generated_cases.json | Current canonical source and provenance, coverage exclusions |
| Generator/catalog/runner/experiment checks | docs/team/evidence/area2/phase-d/independent-tests-20261124.txt | 47 independent passes |
| Independent experiment comparison | docs/team/evidence/area2/phase-d/independent-regeneration-20261124/comparison.json | Two constraint changes, affected/unchanged IDs, hashes, stale-data rejection |
| Original full API failure | docs/team/evidence/area2/phase-c/ci-45183086568-job.log | 169 passed / nine failed before corrections |
| Merged correction retest | docs/team/evidence/area2/phase-c/ci-45197384096-job.log | Separate 14 focused / eight upstream / 176+2 API populations |
| Expanded subset failure | docs/team/evidence/area2/phase-c/ci-45342013246-job.log | 172 passed / five wrong-creator oracle failures; no full-run acceptance |
| Current implementation inventory | tests/team/api/case_ledger.json | 275 unique API cases; 179 generated IDs referenced; 399 remaining |
| Personal use-case definitions and tests | docs/team/RAYYAN_USE_CASES.md; tests/team/e2e/test_rayyan_use_cases.py | Two cases and ten implemented UI flows, not proof of passes |
| Local dependency attempt | docs/team/evidence/area2/phase-d/local-dependency-attempt.txt | Current laptop cannot resolve pytest; no local API/browser pass claimed |
| Actual product correction PR | https://github.com/includeduck/SQE-Horilla-Project/pull/2 | Merged source corrections and attributable commits |
| Proposed C/D continuation | https://github.com/includeduck/SQE-Horilla-Project/pull/8 | Published implementation; draft status pending verification |
| D PR execution | https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45348186865 | Runtime in progress at initial D checkpoint; inspect actual final jobs |
| D push execution | https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45348178607 | Same source; separate run population, not extra unique cases |
| C continuation execution | https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45348178584 | Creator-oracle correction and complete API retest in progress |

The D workflow uploads experiment specs/data/comparison, baseline/variant raw
logs/XML and manifest under phase-d-regeneration-RUN-ATTEMPT; browser XML/logs and
synthetic screenshots/traces under phase-d-browser-RUN-ATTEMPT. These are expected
artifact names until completion is observed, not a claim that every file exists.
Synthetic-only browser traces are retained as CI artifacts, not committed as
public source evidence containing real user data. No production credentials or
database snapshot is required.

Canonical spec SHA-256:
45e37bfbcd255fc567d5923b13076637f8777bbc4c48bb239f6c2e3fe398f0db.
Canonical data SHA-256:
38d69c57a2e33ede9682bb8b6b165d7c1398b578711983ecf05cd3f8e59e3521.
Variant spec SHA-256:
769fa6b449a3f8f9970a74c182b80e1db0e95ede2a36342b74d287583d61c16a.
Runtime-bound data fingerprints differ legitimately from symbolic checked-in
bindings; JUnit case properties identify the actual consumed artifact.
