# Rayyan finish 01 status — contract foundation and input audit
24 November 2026. Syed Muhammad Rayyan Hassan, 24I-3000, SE-5B; connected identity rayyanhasan899.

**Prompt 1 status: COMPLETE — all required stage prerequisites verified.** This stage reconciles the foundation and produces the exact remaining execution plan. It does not claim full Area 2 input/FR acceptance or final project completion. Prompts 2–4 are not executed by this stage; overall release HOLD.

## Delivered coverage
| Item | Result |
|---|---|
| Fresh W1/W2 foundation | Two separate isolated normal-role initializations, schema/system checks, actual JWT HTTP grant/consume/refusal and persisted/ORM readback. |
| Live schema | Production Swagger HTTP 200, Swagger 2.0, 684 paths / 112 normalized leave records including aliases. Separate scoped schema HTTP 200. |
| Source/runtime reconciliation | Active resolver, 19 serializers, model identities/defaults, parsers/renderers, 96 runtime filter dimensions and real reference/routing/permission probes. |
| Canonical scope | 27 → 34 operations; 71 → 88 generated inputs; 578 → 713 generated IDs. Added assignment CRUD and type-reference reads, optional allocation is_active, rejection reasons and explicit media. |
| Identity lineage | All 578 old IDs preserved, 135 added, none retired; all old 399 unconsumed IDs individually accounted for. |
| Current consumer collection | 184 referenced IDs, 529 unconsumed IDs; 280 parametrized scenarios. Neither references nor collection constitute an execution pass. |
| Full required-input inventory | 329 mandatory families, 241 without generated IDs; 314 planned for Prompt 2, 15 for Prompt 3. Includes seven additional manager selectors beyond the 96 Filter fields. |
| Plans | Generated EP/BVA/provenance/binding/wire/context ledger, route scope, 32 decision rows with explicit feasibility, eight authorization rows and full state/refusal plan. |
| Independence | No production code changed, no paid resource, required skip/xfail, invented policy/signoff, threshold reduction or destructive Git/local reset. |

Detailed resolution: ../finish-line/CONTRACT_RECONCILIATION.md. Machine records:
CONTRACT_LINEAGE.json, GENERATED_CASE_AUDIT.json, OPERATION_INPUT_INVENTORY.json and REMAINING_WORK.json in ../finish-line/. Each mandatory input has stable identity, phase, FR/BR/operation/input links, original owner, current executor, actual planned status, evidence, dependencies and acceptance.

## Actual evidence and commands
The unchanged application requirements and scoped tools were installed in free Ubuntu/Python 3.12.16 CI with .github/scripts/install-requirements.sh and tests/team/requirements-area2.txt. Observed runtime versions: Django 5.2.19, DRF 3.18.3, drf-yasg 1.21.15, pytest 9.2.0, pytest-django 4.14.0, requests 2.34.2. Browser run additionally used Playwright 1.65.2. Exact installed output remains in actual logs.

| Source / actual run | Observed result / evidence |
|---|---|
| e9ecebc94d0597edded70c61fedd209023eaf1ea; run 45410463931 | Fresh-a job 138502509889: 1 passed, 307.98 s, artifact 14927033644. Fresh-b job 138502509509: 1 passed, 245.18 s, artifact 14928611352. Distinct temporary SQLite DBs. |
| d3511224ce763f33bfdceeb7bde72ad7f540e9d9; run 45413420091 | Candidate formal schema, 49 prior + four new reader checks, generation freshness and ID partition passed; artifact 14930586301. Exact emitted generated file bytes were published. |
| eb203f7e685379d937460cb7bd7300946de1ad65; run 45414664717 | Published canonical integrity passed. |
| eb203f7e; actual checkout 15d3810; run 45414665978 | Both reconciled-build foundations passed. Both five-case smoke collections retained 4 passes / one failure: the harness incorrectly treated inactive list filtering as record deletion. Failed raw logs and artifacts 14930319940 / 14933265438 retained; not a product defect. |
| 0ce4478b2d21a4f5be04d00b75e0cb34566feb76; checkout 93d40f4; run 45416915816 / job 138525521452 | Formal schema, 49 + four reader checks, deterministic freshness and strict inventory validation all passed; artifact 14932238527. All 713 IDs unique/present, every old 399 accounted, no unjustified N/A, no role binding mismatch; exact 96 runtime Filter fields preserved across shared method routes. |
| 0ce4478b; actual checkout 93d40f46fddd669b9ae000b35b89c24caa132708; run 45416915820 | Fresh-a job 138525522511: foundation 1 pass (258.00 s), smoke 5/5 pass (269.17 s), artifact 14933137449. Fresh-b job 138525523026: foundation 1 pass (274.47 s), smoke 5/5 pass (255.78 s), artifact 14932868040. Both jobs success, no smoke failures/errors/required skips. Five unique cases, not ten unique cases. |
| eb203f7e; checkout 15d3810; run 45414664482 | All ten browser flows passed (299.24 s, artifact 14932497628); strict regeneration baseline six passed, variant four passed with exactly two predicted strict failures, zero errors/skips (artifact 14933045078). Both jobs succeeded. These preserve functionality on the reconciled canonical build, not full input completeness. |
| Historical source 7189656a; run 45388276552 | Old 275 first-order AND 275 reversed-order passed. Complete-scope exited 3, accepted=false. Keep this evidence; do not describe that old reverse pass as pending. |

Representative exact commands (full shell/environment retained in workflow and logs):

```text
python -c "import json; from openapi_spec_validator import validate; validate(json.load(open('tests/team/generator/openapi.json')))"
python -W error::ResourceWarning -m unittest discover -s tests/team/generator -p 'test_*.py' -v
PYTHONPATH=tests/team/generator python -W error::ResourceWarning -m unittest discover -s tests/team/contract -p 'test_media_reader.py' -v
python tests/team/generator/generate.py --spec tests/team/generator/openapi.json --bindings tests/team/generator/bindings.json --output tests/team/generator/generated_cases.json --check
python tests/team/contract/inventory.py --output docs/team/evidence/area2/finish-01/inventory-RUN --emit
python -m pytest -c tests/team/pytest-area2.ini tests/team/contract/test_foundation.py -v -s -o junit_family=xunit1 --junitxml=FOUNDATION_XML
python -m pytest -c tests/team/pytest-area2.ini tests/team/api/test_generated_inputs.py -k "self_allocation_update and is_active" -v -s --junitxml=SMOKE_XML
```

New workflows finish01-contract.yml and finish01-reconcile.yml retain actual schema/runtime/log/XML/inventory artifacts. Foundation fixtures bind independent normal users and real IDs; each initial balance is 0/7/9 and W1→W2 employee balance is 0→5→2, with a rejected follow-up leaving all role balances unchanged. The seed asserts no existing leave/allocation rows; transactional cleanup resets synthetic data between cases. No production DB or user data was reset.

Canonical SHA-256: spec a9685a28c60f2b4484cff36fe0e0d11e723a222fa92fc20483d069d70fe20ae7; bindings f352c832b5299e41007351185e9a1cdcdf673c3d02054f3139c701f4ae8a8a07; data 1520883464d23872d139d0817a926ef49d345651579c072da1c1e3b3e947e0a4. Compare CONTRACT_LINEAGE.json for old fingerprints and exact ID sets. The final publication adds evidence/docs/generated inventory to the tested implementation, not an untested production change. Final inventory source 3caa7741 / tested merge 651707776fcd71e9eaf323ed3708a36044ce010b passed run 45419333975, job 138534203584, artifact 14933018094: formal schema, all 49+4 checks, freshness and reproducible audit with exactly five smoke-verified JSON contexts. The other 708 generated IDs remain pending on the reconciled contract. This verifies evidence ingestion and explicit per-field coercion plans without repeating unchanged application tests.

## Corrections retained honestly
The first candidate run 45412578317 failed because the strict reader rejected a newly declared metadata extension; the explicit extension whitelist and four media-selection regression checks fixed it. Unknown constraints and unsupported alternatives still fail.

A late audit found route-only metadata mapping could overwrite GET filters with POST metadata. The completeness assertion rejected intermediate run 45416612883. The final method+path mapping and validator/static-choice partitions account for all 96 filter dimensions; 273 and 322 were intermediate denominators, superseded by 329. The unmodified failed log is retained. This is an inventory/harness correction, not a product defect.

The is_active=false smoke failure was corrected by asserting unchanged complete persisted IDs, explicit inactive-list HTTP readback, normal detail fields/status/identity and unchanged balances/other requests. The active-list assertion now follows actual manager semantics; no case was removed or marked expected failure.

Original console capture masking damaged quoting inside two Swagger security-definition descriptions. The first derived runtime JSON explicitly omits those descriptive blocks and labels why; full original Swagger JSON remains in the real artifact, raw logs are unchanged. Later capture retains only safe security metadata, produces valid JSON and includes actual validators/renderers. Current runtime-contract-current.json is a provenance-labelled introspection snapshot from run 45414665978; its failed smoke is not mislabeled successful. Final smoke evidence is separate.

## Files, publication and limits
Created tests/team/contract/{conftest.py,contract_urls.py,test_foundation.py,prepare_contract.py,test_media_reader.py,inventory.py}, the two finish01 workflows, lineage/audit/input/remaining-work JSON and reconciliation report, plus actual/derived evidence under docs/team/evidence/area2/finish-01/. Modified generator reader/canonical spec/bindings/data/regressions, API case ledger/consumer, test basis/SCOPE supplement/matrix, handoff/checklist/evidence/AI/A-status and package manifest. prepare_contract.py is historical one-shot migration tooling and is not rerun against the migrated canonical.

Meaningful checkpoints e9ecebc9 → 009a8090 → d3511224 → 3e158c5d → eb203f7e → 8b4f0289 → d187be07 → 0ce4478b → 3caa7741 were pushed on rayyan/phase-c-evidence, PR #8 targeting sqe-team. Connected Git commit author and committer were verified as Rayyan; expected-head leases preserved concurrent history. No merge/protection bypass is claimed. The final evidence/manifest publication is a descendant of these checkpoints; the manifest records its exact pre-manifest Git tree and byte/blob identities.

The workspace execution connection became unavailable mid-stage. Connected GitHub publication and full free CI runtime continued successfully. No local pull, local complete runtime pass or synchronized laptop .git history is claimed. The missing historical Phase A archive remains missing; fresh evidence closes the technical runtime foundation, not its archival recovery or human review.

## Remaining mandatory execution
Prompt 2: implement actual applicable generated/filter/query/header/auth/media/whole-body/collection consumers for the 314 planned families, enforce completeness without hiding the broader denominator. Prompt 3: finish 15 reason/date/relational families and all existing duration/holiday/forecast/state/action/reference/balance gaps; reproduce candidates before minimal fixes and strict retests. Prompt 4: finish feasible carryover, final changed-build/full-scope verification, FR/BR coverage/reporting/packaging and final mandatory Wasay handoff. All remain Codex-for-Rayyan work in this sequence, not transferred merely because this stage inventories them.

Genuine shared dependencies: Wasay's overall Sonar/mutation/merge/deployment gate administration; authentic Area 1/3 evidence and group PDF/ZIP/history coordination with Zain; unavailable local checkout synchronization if still needed. Personal viva and human signoff cannot be performed by an agent. Rayyan's definitive no-further-execution assignment statement belongs after Prompt 4's real attempts.

**Next exact prompt: docs/team/finish-line/PROMPT_02_GENERATED_COVERAGE.md.**
