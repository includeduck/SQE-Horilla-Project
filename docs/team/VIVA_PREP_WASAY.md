# Viva preparation: Muhammad Wasay Tariq (24I-3071)

These items were moved out of the AI-use record, where they were open notes, so that the record shows only what was checked. Each one is something to be able to do by hand or explain without the tool.

| AI-use entry | Be able to |
|---|---|
| 6 SonarQube | Re-count the CFG nodes and edges of `calculate_requested_days` by hand and get cyclomatic complexity 6 (E − N + 2 and decisions + 1) |
| 7 White-box | Re-derive one MCC table (C1 or C3) and the C5 MC/DC pairs by hand |
| 8 Mutation | Explain each custom operator, 3 equivalent mutants (including the `>` vs `>=` one) and 3 survivors that new tests killed |
| 10 Security | Show SEC-01 (state change on a GET) and explain why AD-2 is a denial even though it returns HTTP 200 |
| 11 Performance | Explain the choice of the p95 ≤ 500 ms limit and what REC-01 is |
| 12 Accessibility | Explain the contrast ratio calculation and why issues found by both Lighthouse and axe are counted once |
| 14 Use cases | Walk through each UC-WAS flow and its postconditions |
| 16 Fix #46 | Explain why a failure at the 2nd write left a partial commit, and how `transaction.atomic` and the row lock (`select_for_update`) prevent it |
| 17 CI gate | Explain why the score threshold alone would not have blocked PR #34 (97.3% ≥ 95%) and what the "no unexplained survivor" rule adds |
