# Prompt 2 of 4: complete generated-input and API consumer coverage

Execute this stage completely for Rayyan. Read docs/team/finish-line/README.md
and Prompt 1's actual report, reconciled inventory and REMAINING_WORK.json.
If Prompt 1 left a feasible prerequisite, repair it here rather than assuming
it is Wasay-only. Do not execute Prompts 3/4 automatically in this turn.

## Goal

Implement and execute every feasible missing consumer/reader/binding for the
accepted Area 2 input scope. Resolve the old 399-ID gap with genuine execution
or defensible non-applicability; also cover required inputs missing from that
old generated denominator. Do not substitute counters or renamed exclusions for
application testing.

## Work to complete

1. Refresh refs/teammate changes and actual contract/hash/test baseline. Start
   from Prompt 1's reconciled operation/input inventory, not historical B-only
   reports. Inspect existing generator, case catalog, ledger, runtime artifacts,
   HTTP fixtures, API modules and failure-propagating producer. Reuse the stack.

2. Implement safe runtime scenario bindings and otherwise-valid baselines for all
   applicable operations, generic/self creation/updates, valid/missing/foreign/
   malformed references, routing classes and action identifiers. A symbolic ID
   that matches a schema is not proof that the record exists, is owned, has the
   correct status or has enough balance. Create prerequisite records through real
   HTTP where feasible and corroborate persisted state; isolate lower-level setup.

3. Extend the deterministic spec reader/generator only for actual required,
   source-backed supported constraints. Cover missing classes in the reconciled
   inventory: required/nullable/omitted/wrong-type/coercion/normalization, numeric
   and three-point BVA with justified units, dates/enums/strings/filenames,
   references/actions, query pagination/filter/search/grouping/order semantics,
   generic bodies/updates, whole-body cases and actual media/collection encodings.
   Do not invent numeric limits or binary-size requirements. If a required format
   cannot yet be read, implement it where feasible; do not delete that input.

4. Add actual HTTP consumers for each required generated class and runtime-bound
   baseline. Cover malformed query fallback versus explicit rejection, capped
   pagination, missing/out-of-range/noninteger identifiers, authentication and
   owner/approver/outsider behavior with exact accepted oracles. For file inputs
   send genuine multipart bytes and assert stored bytes/path/identity; distinguish
   JSON null, omission, invalid JSON descriptors and multipart representations.
   Correct response codes come from the reconciled wire contract, not a blanket
   assumption that every schema-invalid value must return 400.

5. Preserve one-mutated-dimension provenance where applicable. Explicitly record
   justified transformations for fixture IDs, omitted optional uploads, media
   encoding and server normalization. Do not call a transformed request byte-
   identical replay. Bind relational inputs to sound contexts; cases whose main
   business oracle needs Prompt 3 must remain explicitly planned, not N/A.

6. Every relevant acceptance/rejection must assert response plus persisted owner,
   record identity/count/state, expected normalized fields and all affected
   balances. Rejected writes must preserve pre-state. Use distinct requester/
   approver/outsider records so wrong-user mutations are observable. No mocks or
   mocked responses may stand in for required API execution.

7. Reconcile every old/new generated ID and every selected input in a machine-
   readable ledger. Maintain separate applicability, implementation and execution
   statuses with tested SHA, actual JUnit identity and consumer mapping. Record
   retired/changed IDs if contract corrections changed the population. A decorator
   or source reference alone is not an executed consumer. Multiple tests consuming
   one ID do not increase the generated denominator.

8. Make complete-scope enforcement reflect actual accepted input coverage,
   required reader support, bindings, consumer mappings and justified N/A decisions.
   Removing old coarse x-exclusions solely to make coverage_complete true is
   prohibited. If the existing gate only checks an empty exclusions list, add a
   narrowly scoped, tested ledger validation so unresolved mandatory inputs,
   missing/malformed results or invented N/A still fail. Genuine external blockers
   keep the gate nonzero and appear in the mandatory Wasay ledger.

9. Execute added/affected consumers in the permitted real application runtime and
   retain raw logs/JUnit. Diagnose feasible harness mistakes and source-backed
   product defects rather than hand off ordinary debugging. Preserve genuine
   failing-before evidence. Fix narrowly when the accepted oracle is clear; if a
   business defect is being completed in Prompt 3, record its exact reproducer
   and carry it there without weakening the assertion.

## Required outputs and checks

- Extend existing generator/API modules rather than duplicate frameworks.
- Verify deterministic output, formal schema validity, stale-output rejection,
  canonical freshness, binding lineage and substantive reader/consumer changes.
- Produce exact generated total, applicable/N/A/blocked/planned partitions,
  implemented distinct API cases and actual executed/pass/fail/error/skip counts.
  Report input coverage separately from generated-ID reference rate and FR
  acceptance. No aggregate percentages from mixed populations.
- Update case_ledger, matrix, test basis, evidence index, AI record, remaining
  ledger and RAYYAN_FINISH_02_STATUS.md. Link every unresolved item to Prompt 3,
  Prompt 4 or a genuinely external Wasay dependency.
- Run the appropriate existing and new focused regressions; preserve baseline
  behavior and all previous source fixes. Do not force a green full-scope claim.
- Commit/push meaningful checkpoints; observe real CI outcomes. Use free isolated
  jobs and adequate measured job budgets, not shortened test collections or
  suppressed errors.

Finish with actual coverage achieved and the remaining concrete business cases
for Prompt 3. Do not stop at an inventory, ask for a fifth prompt, or transfer
feasible implementation merely because the old handoff named Wasay.
