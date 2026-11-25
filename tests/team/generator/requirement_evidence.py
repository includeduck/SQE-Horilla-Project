"""Curated assertion-to-requirement evidence from real source-bound JUnit reports.

Selectors name actual assertions/conditions, rather than accepting broad FR tags
on catalog rows as proof. Missing or failed cases keep that requirement partial.
"""
import argparse
import json
from pathlib import Path


ASSERTIONS = {
    "FR-01": "Assigned-type allocation creation: exact field/owner/count persistence, invalid input refusal, unchanged balances; W1 grants remain separate actions.",
    "FR-02": "Requested allocation approval credits requester exactly once; forbidden roles/states preserve all users' balances.",
    "FR-03": "Requested allocation rejection stores the actual normalized reason without changing balance; malformed approved rejection preserves pre-state.",
    "FR-04": "Requested-only allocation updates/deletes; foreign-owner and owner-to-foreign target transfers are refused without mutation.",
    "FR-05": "All generic/self create/update date/breakdown/attachment/assignment contexts assert exact persisted identity and effective duration.",
    "FR-06": "Effective positive duration, below/at/above balances and caps, forecast reset boundaries, explicit expiry lifecycle and over-balance refusal.",
    "FR-07": "All feasible BR-02 decisions plus requested/approved/pending-cancellation overlap refusal; terminal and foreign-employee exclusions; complementary halves.",
    "FR-08": "Approval truth table and current-balance/policy recheck; exact debit split and unchanged approver/outsider balances; no repeated debit.",
    "FR-09": "Approved rejection/cancellation refund to requester, exact available/carry split, terminal refusals, optional reason normalization and persistence.",
    "FR-10": "Actual available-leave HTTP reads after allocation, consumption, refused overdraft, refund and repetition corroborate persisted assignment fields.",
    "BR-01": "Independent effective-day and effective-funds boundaries, holiday context, forecast/expiry policy and current approval funds; no overdraw.",
    "BR-02": "24 feasible condition combinations; all nine same-day breakdown pairs, assignment/attachment gates and meaningful overlap contexts.",
    "BR-03": "Every graph state/action, four distinct actor modes and repeated allowed decisions; status and requester-versus-actor balance invariants.",
    "BR-04": "All eight permission/manager/self truth rows, exact permission versus reporting-manager roles, foreign ownership and changed-target denial.",
}


def selected(requirement, entry, generated):
    case_id=entry["case_id"]
    op=generated.get(case_id,{}).get("operation", "")
    business=case_id.startswith("BUSINESS:")
    reason=case_id.startswith("REASON:") or ":body:reason:" in case_id
    integration=case_id.startswith("INTEGRATION")
    state=case_id.startswith(("STATE-","ROLE:"))
    auth=case_id.startswith("AUTH-BR04") or (case_id.startswith("WIRE:") and ":header:Authorization:" in case_id)
    if requirement=="FR-01": return op in {"allocation_create","self_allocation_create"} or integration
    if requirement=="FR-02": return (state and "ALLOC-" in case_id and "approve" in case_id) or integration or case_id=="REPEAT-ALLOCATION-APPROVE-001"
    if requirement=="FR-03": return (reason and "allocation_reject" in case_id) or (state and "ALLOC-" in case_id and "reject" in case_id) or case_id=="REJECT-ALLOCATION:malformed-approved-body"
    if requirement=="FR-04": return (state and "ALLOC-" in case_id and case_id.endswith(("update","delete"))) or case_id.startswith("DEFECT-NONOWNER-ALLOCATION") or case_id=="REFERENCE:allocation:owner-transfer"
    if requirement=="FR-05": return business or op in {"leave_create","leave_update","self_leave_create","self_leave_update"}
    if requirement in {"FR-06","BR-01"}: return business or case_id.startswith("APPROVE-POLICY:") or integration or case_id=="DEFECT-CARRYFORWARD-CAP-001"
    if requirement=="FR-07": return case_id.startswith("DEC-BR02") or (business and any(s in case_id for s in ("overlap","complementary"))) or case_id=="REPEAT-LEAVE-CREATE-001"
    if requirement=="FR-08": return auth or case_id.startswith("APPROVE-POLICY:") or integration or (state and "LEAVE-" in case_id and "approve" in case_id) or case_id=="REPEAT-LEAVE-APPROVE-001"
    if requirement=="FR-09": return (reason and "allocation_reject" not in case_id) or integration or (state and "LEAVE-" in case_id and any(s in case_id for s in ("reject","cancel"))) or case_id.startswith(("DEFECT-REFUND","CANCEL-DECISION"))
    if requirement=="FR-10": return integration or state or business or case_id.startswith(("DEFECT-REFUND","CANCEL-DECISION","REPEAT-"))
    if requirement=="BR-02": return case_id.startswith("DEC-BR02") or business
    if requirement=="BR-03": return state or integration or reason or case_id.startswith(("REPEAT-","CANCEL-DECISION","REJECT-ALLOCATION:"))
    if requirement=="BR-04": return auth or case_id.startswith(("ROLE:","REFERENCE:","DEFECT-NONOWNER-ALLOCATION"))
    raise ValueError(requirement)


def build(artifact,ledger,reports,source):
    if not reports: raise ValueError("Actual result reports are required")
    if any(r["expected_source_sha"]!=source for r in reports): raise ValueError("Wrong tested source")
    generated={r["id"]:r for r in artifact["cases"]}
    rows=[]
    for requirement,assertions in ASSERTIONS.items():
        cases=[r["case_id"] for r in ledger["entries"] if selected(requirement,r,generated)]
        missing=sorted({case for case in cases if any(case not in r["results"] for r in reports)})
        bad=sorted({case for case in cases for report in reports for observation in report["results"].get(case,[])
            if observation["status"]!="passed" or observation["source_sha"]!=source or observation["spec_sha256"]!=artifact["spec_sha256"]})
        rows.append(dict(requirement=requirement,required_assertions=assertions,
            required_case_ids=cases,consumer_files=sorted({r["file"] for r in ledger["entries"] if r["case_id"] in cases}),
            tested_source_sha=source,collections=len(reports),missing_ids=missing,failed_or_wrong_lineage_ids=bad,
            status="verified-on-recorded-source" if cases and not(missing or bad) else "partial"))
    return dict(label="Derived from explicit assertion selectors and actual source-bound JUnit; tags alone are not evidence",
        tested_source_sha=source,spec_sha256=artifact["spec_sha256"],
        all_requirements_verified=all(r["status"]=="verified-on-recorded-source" for r in rows),requirements=rows)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",action="append",required=True)
    parser.add_argument("--source",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args(); team=Path(__file__).resolve().parents[1]
    read=lambda path:json.loads(Path(path).read_text(encoding="utf-8"))
    result=build(read(team/"generator/generated_cases.json"),read(team/"api/case_ledger.json"),[read(p) for p in args.report],args.source)
    Path(args.output).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("REQUIREMENT_SUMMARY "+json.dumps({r["requirement"]:{"status":r["status"],"cases":len(r["required_case_ids"]),"missing":len(r["missing_ids"]),"bad":len(r["failed_or_wrong_lineage_ids"])} for r in result["requirements"]},sort_keys=True))
    raise SystemExit(0 if result["all_requirements_verified"] else 3)
