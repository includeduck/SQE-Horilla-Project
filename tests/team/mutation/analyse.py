"""Summarise a mutmut run for the scoped business-rule functions.

Run after run_mutmut.py, from the repo root (WSL):
    python tests/team/mutation/analyse.py --out docs/team/evidence/mutation
Writes summary.json and survivors.md (every surviving mutant with its diff and
the operator that produced it).
"""

import argparse
import difflib
import fnmatch
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from mutmut.mutation.diff_apply import get_diff_for_mutant
from mutmut.stats import status_by_exit_code

TEAM = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("_run", TEAM / "mutation" / "run_mutmut.py")
_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_run)
ops = _run._load("_ops", TEAM / "mutation" / "custom_operators.py")

FILES = ["leave/models.py", "leave/methods.py", "horilla_api/api_views/leave/views.py"]


def changed_fragments(diff):
    old = [line[1:] for line in diff.splitlines() if line.startswith("-") and not line.startswith("---")]
    new = [line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++")]
    a, b = "\n".join(old), "\n".join(new)
    frags = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            frags.append((a[i1:i2], b[j1:j2]))
    return a, b, frags


def signature(diff):
    """Stable identity of a mutant: its changed lines (mutant numbers shift when code changes)."""
    return [line[0] + line[1:].strip() for line in diff.splitlines()
            if line[:1] in "+-" and not line.startswith(("---", "+++"))]


def classify(diff):
    a, b, frags = changed_fragments(diff)
    lits_a = re.findall(r"""["']([a-z_]+)["']""", a)
    lits_b = re.findall(r"""["']([a-z_]+)["']""", b)
    for x, y in zip(lits_a, lits_b):
        if x != y and ops.STATE_NEIGHBOUR.get(x) == y:
            return "custom:leave_state_swap (BR-03)"
        if x != y and ops.BREAKDOWN_SWAP.get(x) == y:
            return "custom:day_breakdown_swap (BR-01)"
    if len(b) < len(a) and "days" in a and re.search(r"[+-]\s", a) and "(" in b and not re.search(r"[+-]\s.*days", "".join(n for _, n in frags)):
        removed = "".join(o for o, _ in frags)
        if re.search(r"[+-]", removed):
            return "custom:balance_term_drop (BR-01)"
    joined = " | ".join(f"{o!r}->{n!r}" for o, n in frags)[:80]
    return f"built-in: {joined}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    status_of = {}
    for f in FILES:
        meta = json.loads(Path(f"mutants/{f}.meta").read_text())
        for key, code in meta["exit_code_by_key"].items():
            if any(fnmatch.fnmatch(key, g) for g in _run.SCOPED_GLOBS):
                status_of[key] = (f, status_by_exit_code[code] if code is not None else "not checked")

    per_func = defaultdict(Counter)
    per_op = defaultdict(Counter)
    survivors = []
    for key, (f, status) in sorted(status_of.items(), key=lambda kv: (kv[0].rsplit("_", 1)[0], int(kv[0].rsplit("_", 1)[1]))):
        diff = get_diff_for_mutant(key, path=Path(f))
        op = classify(diff)
        func = key.split("__mutmut_")[0].split(".")[-1].replace("xǁ", "").replace("ǁ", ".").removeprefix("x_")
        per_func[func][status] += 1
        per_op["custom" if op.startswith("custom") else "built-in"][status] += 1
        if op.startswith("custom"):
            per_op[op][status] += 1
        if status == "survived":
            survivors.append({"key": key, "function": func, "operator": op, "diff": diff})

    totals = Counter(s for _, s in status_of.values())
    killed, survived = totals["killed"], totals["survived"]
    score = 100 * killed / (killed + survived) if killed + survived else 0
    summary = {
        "mutants": len(status_of), "status": dict(totals), "score_percent": round(score, 1),
        "per_function": {k: dict(v) for k, v in per_func.items()},
        "per_operator": {k: dict(v) for k, v in per_op.items()},
        "survivors": [{"function": x["function"], "change": signature(x["diff"]), "key": x["key"]} for x in survivors],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    with open(out / "survivors.md", "w", encoding="utf-8") as fh:
        fh.write(f"# Surviving mutants ({survived})\n\nScore {score:.1f}% ({killed} killed / {killed + survived}).\n\n")
        for i, s in enumerate(survivors, 1):
            fh.write(f"## S{i:02d} `{s['key']}`\n\nFunction: `{s['function']}`. Operator: {s['operator']}\n\n```diff\n{s['diff']}\n```\n\n")
    print(json.dumps({k: summary[k] for k in ("mutants", "status", "score_percent", "per_operator")}, indent=2, ensure_ascii=False))
    for k, v in sorted(per_func.items()):
        print(f"  {k:70s} {dict(v)}")


if __name__ == "__main__":
    main()
