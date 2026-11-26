# Prompt 3 of 4: finish business-rule scenarios and genuine defect corrections

Execute this stage completely for Rayyan. Read docs/team/finish-line/README.md,
the actual Prompt 1/2 results, current accepted contract/SCOPE and remaining
ledger. Repair feasible carryover from those prompts. Do not automatically run
Prompt 4 in this turn.

## Goal

Complete the remaining scoped W1/W2 API/integration business behavior and
accepted-rule traceability, reproduce genuine defects, apply narrow authorized
corrections and obtain real failing-before/passing-after evidence. Preserve
the distinction between a product defect, an incorrect test oracle, a harness
failure and an unanswered business decision.

## Work to complete

1. Refresh the source/remote state, owner decisions and current runtime evidence.
   Read the active API implementations, model validation, forms/services/helpers,
   permissions, existing decision/state catalogs and impacted upstream tests.
   Retain OD-01/OD-02 and all seven established corrections. Ordinary pending-
   duplicate refusal is sequential; do not invent a new concurrent/idempotency
   feature or database uniqueness policy without an accepted requirement.

2. Complete effective-duration and balance scenarios using independent expected
   calculations grounded in the accepted rule:
   - positive effective requested duration; zero/negative effective duration;
   - same-day full/first/second-half and matching/mismatching breakdowns;
   - holiday/company-leave exclusion individually and in combination, avoiding
     double subtraction for overlapping exclusions;
   - employee-specific holidays for the target employee versus another employee,
     with the correct employee context supplied;
   - available balance, allowed/disallowed/expiring/capped carry-forward and
     forecasted entitlement, including stale stored amounts above the policy cap;
   - meaningful below/at/above effective balance boundaries and no overdrawing.
   Do not transplant a positive-duration rule onto allocation amounts or invent
   forecast/expiry policy. Read source and existing owner decisions first; transfer
   only a genuinely unresolved policy with exact competing interpretations.

3. Complete required rejection/cancellation reason behavior: omission, null,
   nonstring, blank/whitespace, meaningful strings, normalization/truncation and
   persistence against actual helper/model bounds. Explicitly reconcile the
   helper's 1000 limit and model's different declared limit; do not silently call
   them consistent. Derive boundary values from real constraints. Assert actual
   stored text and unchanged state on refusal. Distinguish SQLite behavior from
   model/serializer validation or an untested PostgreSQL claim.

4. Finish applicable BR-02 condition combinations and BR-03/BR-04 state/role
   scenarios from the reconciled graph. Preserve infeasible combinations with
   evidence. Exercise allowed/forbidden operations from meaningful states,
   self/nonowner/reporting-manager/permission roles, repetition and invalid
   action IDs. Verify requested-only edits/deletes, overlap exclusions,
   conditional attachments, approval/refund/cancel/cancellation decisions and
   requester-versus-acting-user balance invariants. Add source-backed missing
   reference/relational contexts carried from Prompt 2.

5. Complete connected W1-to-W2 workflow assertions: grant balance, submit/approve
   consumption, refuse over-balance requests, perform accepted reversal/refund
   transitions and repeat decisions without duplicate credits/debits/records.
   Read through the API and independently corroborate persisted state where
   appropriate. No successful response alone establishes correct integration.

6. Establish actual FR-01..FR-10 and BR-01..BR-04 evidence. Map each requirement to
   its required assertions, cases, supported roles/conditions and real results.
   FR acceptance is not inferred from tags, source file presence, generated-case
   counts or passing tooling. Keep partial requirements explicit.

7. For every genuine newly reproduced defect, retain the exact tested source,
   fixture/pre-state, HTTP input/result, persisted post-state and strict failed
   assertion before editing. Implement the smallest source-backed correction,
   retain strict regression tests and run affected upstream tests separately.
   Record root cause, proposed severity/priority, risk, actual fix commit and
   passing-after evidence. Harness/oracle corrections must be labelled honestly.
   No xfail, required skip, weakened assertion or success-forcing exit.

8. Complete the feasible Area 2 defect-management work: reconcile actual repository
   product Issues/PRs with behavior-to-ID mapping and evidence; create/update
   directly necessary factual project records under the authorized identity.
   Close only an Issue whose actual accepted fix/retest warrants closure and for
   which permissions/ownership permit it. Do not impersonate owner approval or
   send unrelated messages. Missing owner review/triage authority becomes a precise
   Wasay item, not a reason to leave the technical evidence unfinished.

9. Update source-backed two-major-defect 5 Whys/cause diagrams and the clearly
   defined Pareto population using actual confirmed defects. Preserve historical
   four/seven-defect populations as dated snapshots if new defects change totals.
   Count defects rather than failing parametrizations. Do not fabricate extra
   major defects, human RCA meetings, effort or lifecycle events.

## Required outputs and checks

- Run all new/affected business/API regressions against isolated real HTTP and
  persisted state; run relevant original team and upstream collections.
- Update the contract/data/consumers if a legitimate accepted rule or source fix
  changes their expectations; retain lineage and stale-output verification.
- Recheck materially affected personal browser flows and regeneration if a change
  impacts their paths. Prompt 4 still performs final integrated verification.
- Update AREA2_DEFECTS, RCA, management/risk/GQM/traceability, coverage matrix,
  evidence and AI records; write RAYYAN_FINISH_03_STATUS.md.
- Every feasible item should be implemented/debugged here. The remaining ledger
  must distinguish verified work, genuine external decisions/permissions and
  final integrated verification reserved for Prompt 4.
- Commit/push meaningful checkpoints and retain actual before/after run links.

Finish with concrete results and exact final-stage carryover. Do not assign
routine debugging to Wasay or request a new planning prompt. Prompt 4 is the
last execution and must complete any feasible leftover technical work.
