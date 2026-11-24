# AI-Use Record

Required by brief Â§7: tool, purpose, output, and what we checked or changed. Keep prompts.

| # | Date | Member | Tool | Purpose / prompt (summary) | Output | What we checked / changed |
|---|---|---|---|---|---|---|
| 1 | 2026-11-18 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Examine the project brief and say what it's about"; "Search for an appropriate MIS" (InvenTree, frappe/helpdesk, akaunting already taken) | Summary of brief; shortlist: Horilla, NetBox, pretix | _TODO: confirm repo is free in section sheet_ |
| 2 | 2026-11-18 | Muhammad Wasay Tariq (24I-3071) | Claude Code (Claude Opus 5.5) | "Check if horilla_api has leave endpoints, then set up the base of the project" | Cloned upstream at baseline commit; confirmed `/api/leave/*` endpoints; local venv + SQLite setup; `tests/team/` scaffold; draft `SCOPE.md`, `SETUP.md`; seed/reset scripts | _TODO: each member reviews SCOPE.md rules against the code and running app; edit before use_ |
| 3 | 2026-11-23 | Syed Muhammad Rayyan Hassan (24I-3000) | ChatGPT / Codex coding assistance | Execute supplied `SQE_IMPLEMENTATION_PHASE_B.md`; preserve scope and document blockers | Source-reconstructed scoped OpenAPI JSON, deterministic EP/BVA generator, focused independent regressions, five-case real-HTTP consumer and disposable settings, coverage/status/communication records | Automated checks and source inspection are reported in `reports/SQE_IMPLEMENTATION_PHASE_B_STATUS.md`; a source-inspection test initially failed because it omitted inherited handlers and was corrected. HTTP, Django, formal schema validation and Ruff were attempted but dependencies were unavailable. No live API pass, recovered A evidence, personal human review or completed viva is claimed. Prompt retained in `docs/team/SQE_IMPLEMENTATION_PHASE_B.md`; exact supplied attachment was read in full. |
| 4 | 2026-11-23 | Syed Muhammad Rayyan Hassan (24I-3000) | ChatGPT / Codex coding assistance | Execute supplied C prompt, verify commit/push/pull, and transfer blocked remaining execution to Wasay as explicitly requested | Real GitHub checkpoint commits under verified rayyanhasan899 author/committer; delivered owner issue/handoff; generated-input, decision/state/auth/integration/regression sources; producer and isolated GitHub Actions verification | Independent checks, actual local failures, remote-run results and any later source fixes/retests are separated in `reports/SQE_IMPLEMENTATION_PHASE_C_STATUS.md`. Source candidates are not called reproduced defects until actual results establish them. Scope gaps, provisional oracles and personal human review/viva remain explicit. No D implementation is authorized by this entry. |

24 November 2026 continuation: Codex read the current Phase C attachment and
GitHub merge/run evidence, retained actual 14/8/176+2 result populations, added
generated update/file/pagination consumers and strict runner result handling.
Independent subprocess checks exercise failure retention/reversed execution;
new API assertions require real runtime verification. No disputed duplicate or
terminal-state oracle was changed. Incomplete mandatory execution is assigned
to Wasay/his agent in handoff.md; human review/viva remains unverified.
