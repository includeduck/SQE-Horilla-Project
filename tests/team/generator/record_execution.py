"""Reconcile immutable CI result rows with the existing input and case ledgers.

This records observations; it never promotes a mapping or a collected case into
a pass. Reports are produced by coverage_guard from actual JUnit.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from build_case_ledger import build_ledger
from wire_catalog import build, source_inventory, supplements

TEAM = Path(__file__).resolve().parents[1]
ROOT = TEAM.parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, document):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(document, indent=2, ensure_ascii=True)+"\n", encoding="utf-8")


def reconcile(reports, source, run, evidence):
    artifact=read(TEAM/"generator/generated_cases.json")
    ledger,wire=build_ledger()
    expected={row["case_id"] for row in ledger["entries"]}
    observed={}
    for report in reports:
        if report["expected_source_sha"]!=source:
            raise ValueError("Report belongs to a different tested source")
        if report["api_mapping_count"]!=len(expected):
            raise ValueError("Report belongs to another consumer population")
        for case_id, rows in report["results"].items():
            if case_id not in expected:
                raise ValueError("Unknown executed identity: "+case_id)
            if any(row["source_sha"]!=source or row["spec_sha256"]!=artifact["spec_sha256"] for row in rows):
                raise ValueError("Execution lineage differs from the current contract")
            observed.setdefault(case_id,[]).extend(rows)
    def outcome(case_ids):
        rows=[row for case_id in case_ids for row in observed.get(case_id,[])]
        if any(row["status"]!="passed" for row in rows):
            return "failed"
        if not case_ids or any(case_id not in observed for case_id in case_ids):
            return "not-yet-observed"
        if any(len(observed[case_id])<len(reports) for case_id in case_ids):
            return "partial-orders"
        return "verified-on-recorded-source"
    for row in ledger["entries"]:
        row["execution_status"]=outcome([row["case_id"]])
        row["tested_source_sha"]=source
        row["execution_evidence"]=observed.get(row["case_id"],[])
    mapping={row["case_id"]:row for row in ledger["entries"] if row["generated"]}
    lineage=read(ROOT/"docs/team/finish-line/CONTRACT_LINEAGE.json")
    old_gap=set(lineage["preserved_ids"])-set(lineage["old_referenced_ids"])
    generated=[]
    for case in artifact["cases"]:
        case_id=case["id"]
        generated.append(dict(case_id=case_id,operation=case["operation"],field=case["field"],
            location=case["location"],applicability="mandatory",
            implementation_status="implemented" if case_id in mapping else "planned-Prompt-3",
            execution_status=outcome([case_id]),tested_source_sha=source,
            original_399_gap=case_id in old_gap,consumer=mapping.get(case_id,{}).get("file"),
            execution_evidence=observed.get(case_id,[]),stage=2 if case_id in mapping else 3))
    inventory=source_inventory()
    input_rows=inventory["inputs"]+supplements(inventory)
    families=[]
    for row in input_rows:
        ids=[case["id"] for case in wire["cases"] if case["input_id"]==row["id"]]
        canonical=[case["id"] for case in artifact["cases"] if
            "INPUT:"+case["operation"]+":"+case["location"]+":"+".".join(map(str,case["field"]))==row["id"]]
        active=ids+[case_id for case_id in canonical if case_id in mapping]
        deferred=[case_id for case_id in canonical if case_id not in mapping]
        families.append(dict(input_id=row["id"],operation=row["operation"],location=row["location"],
            field=row["field"],category=row["category"],stage=row["stage"],requirements=row["requirements"],
            applicability="mandatory",implementation_status="implemented" if row["stage"]==2 else "planned-Prompt-3",
            stage_execution_status=outcome(active) if row["stage"]==2 else "not-yet-observed",
            complete_input_status="planned-Prompt-3" if row["stage"]==3 or deferred else outcome(active),
            tested_source_sha=source,consumer_ids=active,remaining_generated_ids=deferred))
    shared=dict(label="Derived from actual source-bound JUnit; mappings alone are not passes",
                tested_source_sha=source,run_id=run,evidence=evidence,
                spec_sha256=artifact["spec_sha256"],data_sha256=artifact["data_sha256"])
    summary=dict(shared,canonical_generated_cases=len(generated),generated_statuses=dict(Counter(
        row["execution_status"] for row in generated)),api_cases=len(expected),wire_cases=len(wire["cases"]),
        mandatory_input_families=len(families),input_stages=dict(Counter(row["stage"] for row in families)),
        input_execution_statuses=dict(Counter(row["stage_execution_status"] for row in families)),
        complete_input_statuses=dict(Counter(row["complete_input_status"] for row in families)),
        old_399_statuses=dict(Counter(row["execution_status"] for row in generated if row["original_399_gap"])),
        collections=[{key:report[key] for key in ("actual_testcase_count","observed_unique_ids","stage2_accepted",
            "complete_scope_accepted","failed_error_or_skipped_ids","missing_ids")} for report in reports],
        full_scope_accepted=False)
    output=ROOT/"docs/team/finish-line"
    write(output/"PROMPT02_GENERATED_LEDGER.json",dict(shared,rows=generated))
    write(output/"PROMPT02_INPUT_LEDGER.json",dict(shared,rows=families))
    write(output/"PROMPT02_EXECUTION_SUMMARY.json",summary)
    write(TEAM/"api/case_ledger.json",ledger)
    remaining=read(output/"REMAINING_WORK.json")
    indexed={row["id"]:row for row in remaining["items"]}
    for family in families:
        row=indexed.get(family["input_id"])
        if row is None:
            row=dict(id=family["input_id"],phase="B-C",mandatory=True,
                original_owner="Rayyan / Area 2",current_executor="Codex for Rayyan",
                dependencies=[],acceptance="Actual HTTP, exact response and persisted-state/balance assertions")
            remaining["items"].append(row)
        row.update(operation=family["operation"],location=family["location"],field=family["field"],
            stage=family["stage"],requirements=family["requirements"],applicability="mandatory",
            implementation_status=family["implementation_status"],
            execution_status=family["stage_execution_status"],
            status="verified" if family["stage_execution_status"]=="verified-on-recorded-source" else "planned",
            tested_source_sha=source,evidence=[evidence,"docs/team/finish-line/PROMPT02_INPUT_LEDGER.json"],
            remaining_generated_ids=family["remaining_generated_ids"],
            complete_input_status=family["complete_input_status"])
    remaining["summary"].update(summary)
    remaining["summary"].update(referenced_generated_ids=len(mapping),
        unconsumed_generated_ids=len(generated)-len(mapping),required_input_families=len(families),
        required_families_without_generated_ids=len(families)-len(artifact["inventory"]),
        input_families_by_stage=dict(Counter(row["stage"] for row in families)),
        verified_generated_ids_on_recorded_source=sum(row["execution_status"]=="verified-on-recorded-source" for row in generated),
        coverage_complete=False,new_contract_executed_all=False)
    remaining["prepared_stage"]=2
    write(output/"REMAINING_WORK.json",remaining)
    return summary


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",action="append",required=True)
    parser.add_argument("--source",required=True)
    parser.add_argument("--run",type=int,required=True)
    parser.add_argument("--evidence",required=True)
    args=parser.parse_args()
    print(json.dumps(reconcile([read(path) for path in args.report],args.source,args.run,args.evidence),sort_keys=True))
