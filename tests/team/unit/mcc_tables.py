"""Generate MCC (multiple condition coverage) tables and MC/DC pairs for the
compound decisions in the critical module (LeaveRequest.clean and
LeaveRequest.leaveoverlapping).

Python evaluates `and`/`or` with short-circuiting, so for each feasible
combination we also record which conditions are actually evaluated ("-" = not
evaluated). MC/DC pairs are chosen from the MCC table:
  * unique-cause pair: rows differ only in condition c and the outcome differs;
  * otherwise masking (short-circuit) pair: c is evaluated in both rows with
    different values, the outcome differs, and every other condition evaluated
    in both rows has the same value.

Usage: python tests/team/unit/mcc_tables.py > docs/team/reports/MCC_MCDC_TABLES.md
"""

from itertools import product


def ev_and(values):
    """Short-circuit AND: returns (result, evaluated mask)."""
    mask = []
    for v in values:
        mask.append(True)
        if not v:
            return False, mask + [False] * (len(values) - len(mask))
    return True, mask


def ev_c5(v):
    """(Dp and InDept and NoJobs) or (Jb and InJobs)."""
    left, m_left = ev_and(v[:3])
    if left:
        return True, m_left + [False, False]
    right, m_right = ev_and(v[3:])
    return right, m_left + m_right


DECISIONS = [
    {
        "id": "C1",
        "where": "leave/models.py:2072 (single-day breakdown mismatch)",
        "expr": "A and B",
        "conds": ["A: start_date == end_date", "B: start_breakdown != end_breakdown"],
        "eval": ev_and,
        "infeasible": lambda v: None,
        "tests": "test_c1_single_day_breakdown_mismatch_mcc",
    },
    {
        "id": "C2",
        "where": "leave/models.py:2081 (attachment required)",
        "expr": "L and R and N",
        "conds": ["L: leave_type is set", "R: require_attachment == 'yes'", "N: no attachment"],
        "eval": ev_and,
        "infeasible": lambda v: "L=F impossible: line 2049 already returned" if not v[0] else None,
        "tests": "test_c2_attachment_required_mcc",
    },
    {
        "id": "C3",
        "where": "leave/models.py:2106 (past-date restriction, non-superuser)",
        "expr": "R and P",
        "conds": ["R: past-leave restriction enabled for company", "P: start_date < today"],
        "eval": ev_and,
        "infeasible": lambda v: None,
        "tests": "test_c3_past_date_restriction_mcc",
    },
    {
        "id": "C5",
        "where": "leave/models.py:2198-2202 (restriction targets employee)",
        "expr": "(Dp and InDept and NoJobs) or (Jb and InJobs)",
        "conds": [
            "Dp: employee has a department",
            "InDept: restriction lists that department",
            "NoJobs: restriction lists no job positions",
            "Jb: employee has a job position",
            "InJobs: restriction lists that job position",
        ],
        "eval": ev_c5,
        "infeasible": lambda v: (
            "InDept=T needs a department (Dp=F)" if (not v[0] and v[1])
            else "InJobs=T needs a job (Jb=F)" if (not v[3] and v[4])
            else "NoJobs=T contradicts InJobs=T" if (v[2] and v[4])
            else None
        ),
        "tests": "test_c5_restriction_targets_department_or_job_mcdc",
    },
    {
        "id": "H",
        "where": "leave/models.py:1969 (leaveoverlapping half-day exception)",
        "expr": "c1 and c2 and c3 and c4 and c5",
        "conds": [
            "c1: existing.start == new.start",
            "c2: existing.start_breakdown != full_day",
            "c3: new.start_breakdown != full_day",
            "c4: existing.start_breakdown != new.start_breakdown",
            "c5: existing.end_breakdown != new.end_breakdown",
        ],
        "eval": ev_and,
        "infeasible": lambda v: (
            "both full day, so breakdowns are equal (c4 must be F)" if (not v[1] and not v[2] and v[3])
            else "one full day and one half day, so breakdowns differ (c4 must be T)" if ((v[1] != v[2]) and not v[3])
            else None
        ),
        "tests": "test_leaveoverlapping_half_day_exception_mcdc",
    },
]


def fmt(b):
    return "T" if b else "F"


def build(dec):
    n = len(dec["conds"])
    rows = []
    for i, v in enumerate(product([True, False], repeat=n), start=1):
        reason = dec["infeasible"](v)
        out, mask = dec["eval"](list(v))
        rows.append({"no": i, "v": v, "out": out, "mask": mask, "reason": reason})
    return rows


def find_pairs(dec, rows):
    feas = [r for r in rows if not r["reason"]]
    pairs = {}
    for c in range(len(dec["conds"])):
        best = None
        for a in feas:
            for b in feas:
                if a["no"] >= b["no"] or a["out"] == b["out"] or a["v"][c] == b["v"][c]:
                    continue
                if not (a["mask"][c] and b["mask"][c]):
                    continue
                unique = all(a["v"][k] == b["v"][k] for k in range(len(a["v"])) if k != c)
                masking = all(
                    a["v"][k] == b["v"][k]
                    for k in range(len(a["v"]))
                    if k != c and a["mask"][k] and b["mask"][k]
                )
                if unique:
                    best = (a["no"], b["no"], "unique-cause")
                    break
                if masking and best is None:
                    best = (a["no"], b["no"], "masking")
            if best and best[2] == "unique-cause":
                break
        pairs[c] = best
    return pairs


def main():
    print("# MCC and MC/DC tables: critical module\n")
    print("Generated by `tests/team/unit/mcc_tables.py`. T/F = condition value, "
          "`-` = not evaluated because of short-circuiting.\n")
    for dec in DECISIONS:
        rows = build(dec)
        names = [c.split(":")[0] for c in dec["conds"]]
        print(f"## {dec['id']}: `{dec['expr']}`\n")
        print(f"Location: {dec['where']}. Tests: `{dec['tests']}`.\n")
        for c in dec["conds"]:
            print(f"- {c}")
        print()
        print("| # | " + " | ".join(names) + " | Evaluated as | Outcome | Feasible? |")
        print("|---|" + "---|" * len(names) + "---|---|---|")
        for r in rows:
            evald = " ".join(fmt(x) if m else "-" for x, m in zip(r["v"], r["mask"]))
            feas = "yes" if not r["reason"] else f"no: {r['reason']}"
            print(f"| {r['no']} | " + " | ".join(fmt(x) for x in r["v"]) + f" | {evald} | {fmt(r['out'])} | {feas} |")
        feasible = [r for r in rows if not r["reason"]]
        distinct = {tuple(fmt(x) if m else "-" for x, m in zip(r["v"], r["mask"])) for r in feasible}
        print(f"\nMCC: {len(rows)} combinations, {len(feasible)} feasible, "
              f"{len(distinct)} distinct short-circuit evaluations.\n")
        pairs = find_pairs(dec, rows)
        print("| Condition | MC/DC pair (rows) | Type |")
        print("|---|---|---|")
        needed = set()
        for c, p in pairs.items():
            if p:
                needed.update(p[:2])
                print(f"| {names[c]} | {p[0]} / {p[1]} | {p[2]} |")
            else:
                print(f"| {names[c]} | none possible | n/a |")
        print(f"\nMinimum MC/DC test set: rows {sorted(needed)} ({len(needed)} tests for "
              f"{len(names)} conditions; N+1 = {len(names) + 1}).\n")


if __name__ == "__main__":
    main()


# --- helpers used by the tests to execute every feasible MCC row -------------
def feasible_rows(decision_id):
    dec = next(d for d in DECISIONS if d["id"] == decision_id)
    return [r for r in build(dec) if not r["reason"]]


def row_id(row):
    return f"row{row['no']}-" + "".join(fmt(x) for x in row["v"]) + f"->{fmt(row['out'])}"
