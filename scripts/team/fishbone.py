"""Draw the Ishikawa (fishbone) diagrams for the two root cause analyses.

Usage: python scripts/team/fishbone.py   (needs matplotlib)
Writes docs/team/defects/fishbone-<id>.png. Causes are the ones analysed in
docs/team/reports/DEFECT_ANALYSIS.md section 4.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "docs/team/defects"

DIAGRAMS = {
    "issue-4": (
        "#4: rejecting an approved leave\nrefunds the approver, not the requester",
        {
            "Code / design": ["API re-implements the refund\ninstead of reusing web logic",
                              "Variable `employee_id` holds\nthe acting user, not the owner"],
            "Requirements": ["'Refund goes to the requester'\nnever written as a rule",
                             "API added later (2024) with\nno spec of its own"],
            "Process": ["Review checked permissions,\nnot the money flow",
                        "No defect class 'wrong actor'\nin review checklist"],
            "Testing": ["Upstream API tests assert\nscoping, never balances",
                        "No test reads the requester's\nbalance after a reject"],
            "People": ["Security fixes (GHSA) focused\nreviews on who may act",
                       "Ambiguous naming accepted"],
            "Tools / data": ["No static check links actor\nvs. record owner",
                             "Duplicated logic (4.6% dup.\nin leave/) not flagged"],
        },
    ),
    "issue-46": (
        "#46 (REC-01): failed approval\nplus retry credits balance twice",
        {
            "Code / design": ["Two dependent writes without\ntransaction.atomic",
                              "Status checked before, not\nlocked (no select_for_update)"],
            "Requirements": ["No rule 'approval is\nall-or-nothing'",
                             "Retry behaviour never\nspecified"],
            "Process": ["Atomicity used in some views\n(bulk ops) but not as a standard",
                        "No failure-mode review\nfor state-changing endpoints"],
            "Testing": ["Tests only exercise the happy\npath and validation errors",
                        "No fault injection before\nthis project (test double)"],
            "Environment": ["ATOMIC_REQUESTS not enabled\nin settings",
                            "Django autocommit: each save()\ncommits immediately"],
            "Tools / data": ["No DB-failure simulation\nin CI",
                             "Monitoring cannot see a\ncredit without status change"],
        },
    ),
}


def draw(key, effect, causes):
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis("off")
    spine_y, head_x = 3.5, 11.2
    ax.annotate("", xy=(head_x, spine_y), xytext=(0.6, spine_y),
                arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#333333"))
    ax.text(head_x + 0.15, spine_y, effect, va="center", ha="left", fontsize=11, weight="bold",
            bbox=dict(boxstyle="round,pad=0.5", fc="#fbe9e6", ec="#AC3B2A", lw=1.5))
    cats = list(causes.items())
    xs = [2.6, 5.6, 8.6]
    for idx, (cat, items) in enumerate(cats):
        top = idx % 2 == 0
        x_end = xs[idx // 2]
        y0 = 6.3 if top else 0.7
        ax.plot([x_end - 1.3, x_end], [y0, spine_y], color="#555555", lw=1.6)
        ax.text(x_end - 1.3, y0 + (0.25 if top else -0.25), cat, ha="center",
                va="bottom" if top else "top", fontsize=10.5, weight="bold", color="#1f4e79")
        for j, cause in enumerate(items):
            frac = (j + 1) / (len(items) + 1)
            cx = x_end - 1.3 + 1.3 * frac
            cy = y0 + (spine_y - y0) * frac
            ax.plot([cx - 0.9, cx], [cy, cy], color="#999999", lw=1)
            ax.text(cx - 0.95, cy, cause, ha="right", va="center", fontsize=7.8)
    fig.tight_layout()
    fig.savefig(OUT / f"fishbone-{key}.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for key, (effect, causes) in DIAGRAMS.items():
        draw(key, effect, causes)
    print("written:", ", ".join(f"fishbone-{k}.png" for k in DIAGRAMS))
