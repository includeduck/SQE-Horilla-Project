"""Export the defect log from GitHub Issues and draw the Pareto charts.

Reads every issue labelled `defect` (labels carry severity, priority, triage,
category, source and status), writes docs/team/defects/DEFECT_LOG.csv and two
Pareto charts (by count, and weighted by severity) as PNG.

Usage (needs the GitHub CLI logged in, and matplotlib):
    python scripts/team/defect_pareto.py
"""

import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = "includeduck/SQE-Horilla-Project"
OUT = Path(__file__).resolve().parents[2] / "docs/team/defects"
WEIGHT = {"high": 3, "medium": 2, "low": 1}
NAMES = {
    "input-validation": "Input validation /\nerror handling",
    "leave-rule-logic": "Leave rule logic\n(BR-01/BR-02)",
    "access-control": "Access control\n(BR-04)",
    "security-config": "Security\nconfiguration",
    "dependency": "Third-party\ndependency",
    "state-transition": "State transition /\nduplicates (BR-03)",
    "data-integrity": "Data integrity /\natomicity",
    "maintainability": "Maintainability",
}


def label(labels, prefix):
    return next((l.split(":", 1)[1] for l in labels if l.startswith(prefix + ":")), "")


def fetch():
    raw = subprocess.run(
        ["gh", "issue", "list", "-R", REPO, "--label", "defect", "--state", "all", "--limit", "200",
         "--json", "number,title,state,labels,createdAt,closedAt"],
        capture_output=True, text=True, encoding="utf-8", check=True).stdout
    rows = []
    for i in json.loads(raw):
        labels = [l["name"] for l in i["labels"]]
        rows.append({
            "issue": i["number"], "title": i["title"], "state": i["state"].lower(),
            "category": label(labels, "category"), "severity": label(labels, "severity"),
            "priority": label(labels, "priority"), "triage": label(labels, "triage"),
            "source": label(labels, "source"), "status": label(labels, "status") or i["state"].lower(),
            "created": i["createdAt"][:10], "closed": (i["closedAt"] or "")[:10],
        })
    missing = [r["issue"] for r in rows if not (r["category"] and r["severity"])]
    if missing:
        sys.exit(f"defects without category/severity labels: {missing}")
    return sorted(rows, key=lambda r: r["issue"])


def pareto(counter, title, ylabel, path):
    items = counter.most_common()
    labels = [NAMES.get(k, k) for k, _ in items]
    values = [v for _, v in items]
    total = sum(values)
    cumulative, running = [], 0
    for v in values:
        running += v
        cumulative.append(100 * running / total)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    bars = ax.bar(range(len(values)), values, color="#AC3B2A")
    ax.bar_label(bars, padding=2)
    ax.set_xticks(range(len(values)), labels, fontsize=8.5)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax2 = ax.twinx()
    ax2.plot(range(len(values)), cumulative, color="#1f4e79", marker="o")
    for x, y in enumerate(cumulative):
        ax2.annotate(f"{y:.0f}%", (x, y), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    ax2.axhline(80, color="grey", linestyle="--", linewidth=1)
    ax2.set_ylim(0, 110)
    ax2.set_ylabel("Cumulative %")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return list(zip([k for k, _ in items], values, cumulative))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = fetch()
    with open(OUT / "DEFECT_LOG.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    by_count = Counter(r["category"] for r in rows)
    by_weight = Counter()
    for r in rows:
        by_weight[r["category"]] += WEIGHT[r["severity"]]
    a = pareto(by_count, f"Defects by category (n = {len(rows)})", "Number of defects", OUT / "pareto-count.png")
    b = pareto(by_weight, "Defects by category, weighted by severity (high 3, medium 2, low 1)",
               "Severity-weighted score", OUT / "pareto-severity.png")
    print(json.dumps({"defects": len(rows), "by_count": a, "by_severity": b,
                      "severity": Counter(r["severity"] for r in rows),
                      "state": Counter(r["state"] for r in rows),
                      "status": Counter(r["status"] for r in rows),
                      "source": Counter(r["source"] for r in rows)}, indent=1))


if __name__ == "__main__":
    main()
