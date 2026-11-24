# Area 2 CI producer and owner handoff

## Latest observed runtime - 24 November 2026

This section supersedes historical unresolved-oracle/new-suite-pending labels.
Run 45355537962 on source 32621b42 (tested PR merge 42f0b233) completed:
16 focused regressions, eight upstream tests, 177 expanded input/file/query
cases, one W1/W2 preflight and the full first-order 275-case collection, all
passing in their separate populations. No skips/errors/failures are reported
by those completed collection summaries. Raw job log and derived summary:
`docs/team/evidence/area2/phase-c/ci-45355537962-job.log` and
`ci-45355537962-summary.json`; actual CI artifact 14907648168.

The reversed 275-case collection was cancelled at the 90-minute job limit;
its partial progress is not accepted as a completed second run. The final
complete-scope stage was not reached. Source 7189656a increases only the job
budget to 120 minutes. Current retest: run 45388276552. The preserved complete
scope remains false: 179/578 generated IDs referenced, 399 unconsumed, further
balance/media/contract coverage and group acceptance still required. Phase C
is partial/HOLD despite the clean 275-case first-order result. Owner-confirmed
duplicate/terminal fixes passed strict retests; no xfail was used.


Owner of the implemented producer: Syed Muhammad Rayyan Hassan, **24I-3000**.
Wasay owns the complete PR/Sonar/mutation gate and is assigned the blocked
completion work in root `handoff.md` and [issue #1](https://github.com/includeduck/SQE-Horilla-Project/issues/1).

## Exact command

From a complete supported Horilla environment, on Linux or Windows:

```sh
python -m pip install -r requirements.txt
python -m pip install -r tests/team/requirements-area2.txt
python tests/team/run_area2.py --evidence docs/team/evidence/area2/run-UNIQUE-ID
```

Use a **new** evidence directory for each invocation; the runner refuses to
overwrite earlier output or reuse an old passing JUnit XML. On this laptop use
`.\.venv\Scripts\python`; that environment still lacks the application tools.
The repository-owned `.github/scripts/install-requirements.sh` is reused by the
isolated Ubuntu workflow to install the unchanged application dependency set.

## Stage order and real failure propagation

1. Run generator/catalog/producer independent regressions with `unittest`.
2. Regenerate in memory and verify canonical spec/binding/data freshness.
3. Formally validate OpenAPI with `openapi-spec-validator`.
4. Run Django system checks with `area2_settings`.
5. Preflight the integrated W1/W2 case to catch fixture/runtime failures before
   an expensive complete collection. Retain its own XML; a repeated preflight
   does not inflate the number of unique API cases.
6. Run all `tests/team/api/` cases against pytest-django's real local server,
   writing `api-first.xml` with case/spec/binding properties.
7. Start a second fresh pytest process, reverse collection with the explicit
   `area2_order` plugin and write `api-reversed.xml`.
8. Enforce complete declared scope with `--require-complete`.

Any failed child exits nonzero and blocks dependent stages. Missing/empty XML
or skipped API cases also fail. `run-manifest.json` distinguishes passed,
failed and blocked stages, actual XML counts, fingerprints and final acceptance.
The known scope exclusions currently cause the final completeness gate to exit
3 even if a selected API subset eventually passes. Do not remove that gate to
claim assignment completion. A generator check is not an API pass.

The runner uses absolute repository/fixture paths, temporary SQLite/media,
normal seeded roles and unchanged auth/permissions. Each API scenario has a
fresh transactional fixture; each API pass uses a new process/test database.
No default local database reset, production credential or mock HTTP endpoint is
used. Native JSON cases intentionally omit the optional upload baseline and
record a bound-request hash; file cases use actual multipart uploads.

Failure propagation is independently exercised by a child that exits 7, a
retained real transcript/exit, missing XML, XML error/skip totals and refusal to
overwrite evidence. These utility checks do not prove branch protection.

## Isolated remote verification

`.github/workflows/area2-verification.yml` runs the producer on relevant pushes
to `sqe-team` and relevant pull requests targeting `sqe-team`, on an ordinary Ubuntu runner with read-only repository permission
and synthetic data. It preserves actual artifacts with `if: always()` after a
failure; that upload condition does not suppress the failing test step. It
does not modify Wasay's existing workflows, configure a paid runner or claim a
complete all-tests/Sonar/mutation gate.

First observed execution:
[run 45179588790](https://github.com/includeduck/SQE-Horilla-Project/actions/runs/45179588790),
build `5a5df40ededb132653b33d0547a60e3e5225e9b9`. Application/system/test dependencies
installed successfully. OpenAPI validation and Django checks passed, but all
171 collected API cases errored in the fixture before their test bodies, on a
settings-module metadata assertion. The correction in commit
`1948e0fdf85ec3824e5f472176688e994307928a` uses an explicit positive isolation marker,
environment and actual database-path/engine checks, adds the preflight and streams
partial logs without suppressing failures. Runtime retest is run 45183086568;
consult the C status for its latest actual result. No product failure is inferred
from the first run's setup errors.

## Mandatory remaining integration for Wasay / his agent

Wire the same fail-propagating producer into **every relevant PR** alongside
Sonar, all other tests and mutation. Confirm the intended PR target, required
check names, justified thresholds, blocked merge/deployment behavior, fixed PR
and blocked PR evidence. Existing upstream workflows target `dev/v2.0` and
`2.0`; their presence alone does not cover `sqe-team`.

Preserve and reconcile source changes from both members before integration.
Connected GitHub writes work under Rayyan's verified identity; local `.git`
remains protected. Do not force-push or reset the laptop's uncommitted files to
make its outdated local HEAD look synchronized.

## Focused attachment correction retest

PR #2 adds a targeted step before the producer: four real storage cases plus
the existing five generated HTTP slice cases. Pipefail retains pytest failures
through tee; actual XML/logs are always uploaded. This nine-case targeted
collection is separate from the 178-case API ledger and repeats five existing
API cases; do not add nine to the unique API denominator. Proposed correction
build: a1cfb4ab81c993684f6917c4db4d43d4d7e1fd83. Actual result remains pending.

## Continuation producer contract - 24 November 2026

The runner now collects reversed-order evidence even if api-first fails, and
checks completeness independently after API failures. It retains the first
failure exit; it never converts two failing runs into acceptance. Failed
schema/runtime/preflight still blocks dependent stages. Missing, malformed,
empty, skipped, failed or errored JUnit with child exit zero also fails.

Current inventory: 275 distinct API cases / 179 of 578 generated IDs; full
coverage is still false. New-build runtime evidence must be inspected. The
focused expansion step writes `expanded.xml` before the full producer. The
old merged-build results are 14 focused passes, 8 upstream passes and 176/178
API passes; these are separate populations.

Synthetic disposable users use MD5PasswordHasher only in area2_settings to
reduce fixture/authentication time. Password checks, JWT issuance and actual
role/permission handling remain enabled. Production settings are untouched.

## Phase D integration actually supplied

The relevant-PR source wiring is implemented, not an outstanding task for Wasay:
Area 2 runs on relevant changes targeting sqe-team; Phase D has separate strict
regeneration and browser jobs. Regeneration run 45348178607 is verified successful
with exact baseline 6/6 and variant 4 pass / 2 predicted strict fail populations.
The first expanded C step after creator-oracle correction passed in run
45348178584; full/reversed producer results remain a separate acceptance check.

Wasay's remaining H-05 is the complete all-tests/Sonar/mutation integration,
required-check policy and real blocked/fixed merge/deploy evidence. Reading
classic protection returned 403 (integration lacks administration access); an
empty accessible ruleset list does not prove protection absent. No branch
protection was changed or bypassed. Keep any failed C/completeness checks red.
