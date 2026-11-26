"""Mutation part of the Area 1 CI quality gate.

  python tests/team/ci/mutation_gate.py <summary.json>

Fails (exit 1) when
  * the mutation score is below the threshold in docs/team/ci/gate-thresholds.json, or
  * any surviving mutant is not a documented equivalent mutant
    (docs/team/ci/mutation-equivalents.json, justified in MUTATION_TESTING.md §5).
Mutants are matched by function + changed lines, because mutmut's mutant numbers
shift whenever the surrounding code changes.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main(summary_path):
    cfg = json.loads((ROOT / "docs/team/ci/gate-thresholds.json").read_text(encoding="utf-8"))["mutation"]
    equivalents = json.loads((ROOT / cfg["equivalents_file"]).read_text(encoding="utf-8"))["equivalents"]
    known = {(e["function"], tuple(e["change"])) for e in equivalents}
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))

    score = summary["score_percent"]
    unexplained = [s for s in summary["survivors"] if (s["function"], tuple(s["change"])) not in known]
    ok = score >= cfg["min_score_percent"] and not unexplained

    lines = [
        f"### Mutation gate: {'PASS' if ok else 'FAIL'}", "",
        f"- Mutants: {summary['mutants']} | status: {summary['status']}",
        f"- Score: **{score}%** (threshold {cfg['min_score_percent']}%)",
        f"- Survivors: {len(summary['survivors'])}, documented equivalent: {len(summary['survivors']) - len(unexplained)}, "
        f"**unexplained: {len(unexplained)}**",
    ]
    for s in unexplained:
        lines.append(f"  - `{s['key']}` ({s['function']}): " + " / ".join(f"`{c}`" for c in s["change"]))
    report = "\n".join(lines)
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(report + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
