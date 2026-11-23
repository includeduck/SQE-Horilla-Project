# Team tests (SE3002 SQE Final Project)

Everything in this folder is written by our team. Upstream tests (e.g. `leave/tests/`) earn no marks and are not counted.

| Folder | Brief section | Tool | Owner area |
|---|---|---|---|
| `unit/` | White-box unit tests, 100% statement + branch on leave business logic, MCC / MC/DC | pytest, pytest-django, coverage.py | Area 1 |
| `generator/` | OpenAPI spec + EP / 3-point BVA data generator | Python script | Area 2 |
| `api/` | API and integration tests using generator output | pytest + requests | Area 2 |
| `e2e/` | Use-case tests, usability + keyboard tests, axe-core | Playwright (Chromium) | Area 3 |
| `security/` | Access-matrix checks (Playwright), ZAP / pip-audit evidence | Playwright, OWASP ZAP, pip-audit | Area 3 |
| `perf/` | Load scripts (1 VU and ≥5 VU) | Grafana k6 OSS | Area 3 |
| `recovery/` | Failure-and-recovery test for a state-changing operation | pytest + test double | Area 3 |

Test-basis IDs (FR-xx, BR-xx) come from [`docs/team/SCOPE.md`](../../docs/team/SCOPE.md). Reference them in each test's docstring so the traceability matrix can be generated.

## Rayyan Area 2: Phase B generator and HTTP slice

Owner: Syed Muhammad Rayyan Hassan, **24I-3000**, `rayyanhasan899`.
Current acceptance status is **partial / HTTP blocked**, detailed in
[`SQE_IMPLEMENTATION_PHASE_B_STATUS.md`](../../docs/team/reports/SQE_IMPLEMENTATION_PHASE_B_STATUS.md).
The source-reconstructed test basis is
[`AREA2_TEST_BASIS.md`](../../docs/team/AREA2_TEST_BASIS.md).

### Independent generation and regression checks

From the repository root with a supported Python (3.12–3.14), these commands
require only the standard library. On this Windows checkout replace `python`
with `.\.venv\Scripts\python`; on Linux use the activated environment's
`python` or `.venv/bin/python`.

```sh
python -m unittest discover -s tests/team/generator -p test_generate.py -v
python tests/team/generator/generate.py --spec tests/team/generator/openapi.json --bindings tests/team/generator/bindings.json --output tests/team/generator/generated_cases.json
python tests/team/generator/generate.py --spec tests/team/generator/openapi.json --bindings tests/team/generator/bindings.json --output tests/team/generator/generated_cases.json --check
```

The reader supports **OpenAPI 3.0.3 JSON**, local references, body object/nested
leaves, path/query scalar inputs, required versus nullable, enum/type classes,
finite numbers, explicit numeric steps, character/array limits, date formats and
absolute date bounds, and synthetic multipart file descriptors. The scoped
contract also uses `x-binding`, `x-reference`, `x-date-order`,
`x-filename-maxLength`, `x-allow-empty-file` and `x-trim-whitespace`.
`x-wire-coercion` is a disclosure, not an exhaustive DRF coercion model.
Array item validation and one-invalid-item classes are supported; recursive
item-by-item EP/BVA expansion and multipart collection encoding are not claimed.
Unsupported relevant schema/operation constraints fail visibly.

`bindings.json` is synthetic and deterministic; it contains no credentials.
Never substitute real personal data or a production account. Runtime date/ID
bindings must be chosen for the scenario, not copied blindly from placeholders.
The generator never calls an application server.

Each JSON artifact contains operations, input inventory, source exclusions,
case IDs, baseline/mutated request, EP/BVA class, expected predicate/oracle,
FR/BR references, source schema, and BVA limit/unit/step/inclusivity. Canonical
SHA-256 fingerprints cover the spec, logical bindings and generated data.
There is no volatile timestamp in comparison data. `--check` regenerates in
memory and rejects stale/altered output with exit 2, including generator logic
changes that change the expected artifact. Consumers do the same check.

Exit 0 means generation/freshness succeeded for the declared supported subset.
It does **not** mean all-input/API/assignment coverage passed. Current output has
`coverage_complete: false` and explicit exclusions. Add `--require-complete`
when a completion gate must reject unresolved exclusions; it intentionally exits
3 for the current contract. Wasay retains CI design/required-check ownership.

### Real HTTP consumer: requires the complete application environment

Install the unchanged root application requirements, then the scoped tools:

```sh
python -m pip install -r requirements.txt
python -m pip install -r tests/team/requirements-area2.txt
python -c "import json; from openapi_spec_validator import validate; validate(json.load(open('tests/team/generator/openapi.json', encoding='utf-8')))"
python -m pytest -c tests/team/pytest-area2.ini tests/team/api/test_generated_slice.py -v -s --junitxml=docs/team/evidence/area2/phase-b/http-results.xml
python -m ruff check tests/team/generator tests/team/api tests/team/area2_settings.py
```

The explicit config is essential: it uses `area2_settings` and pytest-django's
real loopback server, absolute disposable SQLite files, temporary media,
locmem mail/cache, unchanged authentication/permissions/password hashing and
the existing synthetic `scripts/team/seed_team.py`. No manually running server,
Docker container or reset of `TestDB.sqlite3` is required. Do not run the
destructive normal reset script against an unverified local database.

Five parametrized cases consume generated output: one valid allocation amount,
one nonnumeric amount and filename lengths just below/at/above the declared
100-character bound. The fixture checks that actual serializer defaults agree
before any consumer case proceeds. It verifies the checked-in artifact, binds
the actual employee/type IDs, writes and rereads a fresh runtime JSON artifact,
and selects the same stable case IDs from it. It authenticates normal employee
and approver accounts and never saves JWTs.

Each case asserts real response/error fields, the employee's HTTP list/detail
and unchanged HTTP balance, the approver's independent balance, row counts,
owner, request state, amount and stored file bytes. ORM checks corroborate HTTP
readback. Every case starts from pytest-django's freshly flushed synthetic
state. `-s` exposes nonsecret case/spec/data lineage, also added as JUnit
properties. Use JUnit's default xunit2 with any `record_property` compatibility
warnings visible, or pass `-o junit_family=xunit1` if consuming tools require
those properties in a supported family.

After the full slice passes, rerun its nodes in reverse order explicitly
(without installing an ordering plugin):

```sh
python -m pytest -c tests/team/pytest-area2.ini 'tests/team/api/test_generated_slice.py::test_generated_allocation[self_allocation_create:body:attachment:BVA:x-filename-maxLength-above]' 'tests/team/api/test_generated_slice.py::test_generated_allocation[self_allocation_create:body:attachment:BVA:x-filename-maxLength-at]' 'tests/team/api/test_generated_slice.py::test_generated_allocation[self_allocation_create:body:attachment:BVA:x-filename-maxLength-below]' 'tests/team/api/test_generated_slice.py::test_generated_allocation[self_allocation_create:body:requested_days:EP:nonnumeric]' 'tests/team/api/test_generated_slice.py::test_generated_allocation[self_allocation_create:body:requested_days:EP:valid]' -v -s
```

These commands are provided for reproducibility; consult the status report for
what actually ran. Current HTTP invocation stops at missing pytest, so no HTTP
JUnit result or passing API run is claimed. Full decision/state/balance scenarios
remain Phase C; the two-real-constraint demonstration remains Phase D.

## Phase C producer, case inventory and remote verification

The latest execution is tracked in
[`SQE_IMPLEMENTATION_PHASE_C_STATUS.md`](../../docs/team/reports/SQE_IMPLEMENTATION_PHASE_C_STATUS.md).
The preceding B runtime limitation is historical; an isolated remote verification
workflow now installs the application runtime and runs the same test producer.
Its result must be checked rather than inferred from job startup.

```sh
python tests/team/run_area2.py --evidence docs/team/evidence/area2/run-UNIQUE-ID
```

The runner verifies generator tests, data freshness, formal schema and Django,
then runs all API cases twice in separate processes with reversed second order,
retains actual logs/JUnit/manifest and enforces the incomplete-scope gate. It
refuses to overwrite prior evidence. See
[`AREA2_CI_HANDOFF.md`](../../docs/team/AREA2_CI_HANDOFF.md) for exact prerequisites,
failure semantics and Wasay's remaining complete-gate integration.

`api/case_ledger.json` inventories **178** implemented API cases, counted once:
71 generated self-create inputs, the existing five-case multipart slice, three
generated pagination-clamp boundaries, three generated missing-reference cases,
24 feasible BR-02 combinations, eight BR-04 combinations, 50 state/role
transitions, 11 workflow/regression/repetition cases, two token cases and one
generic non-owner detail case. The eight infeasible rows of the full 32-row
BR-02 table remain documented, not skipped executable tests. This inventory is
not an execution result or full selected-input coverage claim.

`case_catalog.py` and its bookkeeping regressions are independent of Django.
They verify unique scenario accounting, not the application's business logic
or Wasay's statement/branch/MCC/MC/DC coverage.

The C harness reuses B's server/seed/Requests fixtures. It adds a distinct normal
outsider and deliberately different approver balance, so a wrong-user refund
is observable. Non-file input tests bind native JSON and remove the optional
upload baseline, recording the bound-request hash. The API's falsy end-date
normalization is explicitly recorded separately from the raw date schema.
These adaptations must be reconciled with a complete media/normalization
contract; they are not silently called byte-for-byte multipart replay.

Pagination generation uses a source-derived `x-clamp-maximum: 100`, not a
rejecting maximum. Values 99/100/101 are generated with expected normalized
sizes 99/100/100. Other pagination/filter/rejection-reason/dynamic-balance inputs
remain explicitly unfinished. Provisional duplicate/terminal-state assertions
need owner reconciliation; real failures must remain visible.

Blocked unfinished work is assigned by Rayyan to Wasay/his agent in
[`handoff.md`](../../handoff.md) and
[issue #1](https://github.com/includeduck/SQE-Horilla-Project/issues/1).
GitHub author/committer attribution is verified for each published checkpoint.
The original laptop Git metadata remains read-only; do not reset or discard its
uncommitted files to conceal the difference from the published branch.
