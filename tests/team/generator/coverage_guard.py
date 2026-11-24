"""Strict deterministic consumer accounting against genuine JUnit, not counters."""
import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TEAM=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TEAM/"generator"))
from wire_catalog import build


def results(paths):
    if not paths:
        raise ValueError("No actual JUnit supplied")
    observed,failures,total={},[],0
    for path in paths:
        root=ET.parse(path).getroot(); cases=list(root.iter("testcase"))
        if not cases: raise ValueError("Empty JUnit: "+str(path))
        total+=len(cases)
        for test in cases:
            props={p.get("name"):p.get("value",p.text) for p in test.findall("./properties/property")}
            bad=next((tag for tag in ("failure","error","skipped") if test.find(tag) is not None),None)
            case_id=props.get("case_id"); node=test.get("classname","")+"::"+test.get("name","")
            row=dict(status=bad or "passed",junit=str(path),node=node,source_sha=props.get("source_sha"),
                     spec_sha256=props.get("spec_sha256"),bound_data_sha256=props.get("data_sha256"),
                     bound_request_sha256=props.get("bound_request_sha256"),input_family=props.get("input_family"))
            if bad: failures.append(dict(row,case_id=case_id))
            if case_id: observed.setdefault(case_id,[]).append(row)
    return observed,failures,total


def validate(artifact,ledger,wire,paths,*,stage2=False,expected_source=None):
    entries=ledger["entries"]; ids=[r["case_id"] for r in entries]
    if len(ids)!=len(set(ids)): raise ValueError("Duplicate consumer mapping")
    generated={r["id"] for r in artifact["cases"]}
    mapped={r["case_id"] for r in entries if r["generated"]}
    pending=set(ledger["unconsumed_generated_case_ids"])
    if mapped&pending or mapped|pending!=generated: raise ValueError("Lost or duplicated generated ID")
    if ledger["spec_sha256"]!=artifact["spec_sha256"] or ledger["data_sha256"]!=artifact["data_sha256"]:
        raise ValueError("Stale ledger fingerprints")
    expected_wire={r["id"] for r in wire["cases"]}
    actual_wire={r["case_id"] for r in entries if r["file"]=="test_runtime_wire.py"}
    if expected_wire!=actual_wire: raise ValueError("Missing mandatory wire reader/consumer")
    for row in entries:
        if row.get("applicability")=="not_applicable" and not row.get("evidence"): raise ValueError("Invented N/A")
        if row.get("implementation_status")=="unsupported": raise ValueError("Required reader unsupported")
    observed,failed,total=results(paths)
    missing=sorted(set(ids)-set(observed))
    bad=sorted(k for k,v in observed.items() if any(r["status"]!="passed" for r in v))
    wrong_spec=sorted(k for k,v in observed.items() if any(r["spec_sha256"]!=artifact["spec_sha256"] for r in v))
    wrong_source=sorted(k for k,v in observed.items() if expected_source and any(r["source_sha"]!=expected_source for r in v))
    deferred={r["id"] for r in artifact["cases"] if r["field"]==["reason"] or r["expected"]["oracle"]=="date-order"}
    unresolved=sorted(pending-deferred) if stage2 else sorted(pending)
    passed=not(missing or bad or failed or wrong_spec or wrong_source or unresolved)
    complete=passed and not artifact["exclusions"] and not pending and not stage2
    return dict(label="Derived from actual JUnit and deterministic consumer ledgers",
                expected_source_sha=expected_source,canonical_cases=len(generated),generated_mapped=len(mapped),
                generated_pending=sorted(pending),wire_cases=len(expected_wire),
                mandatory_input_families=wire["mandatory_input_families"],api_mapping_count=len(ids),
                actual_testcase_count=total,observed_unique_ids=len(observed),missing_ids=missing,
                failed_error_or_skipped_ids=bad,raw_failures=failed,wrong_spec_ids=wrong_spec,
                wrong_source_ids=wrong_source,unjustified_pending=unresolved,
                stage2_accepted=passed if stage2 else False,complete_scope_accepted=complete,
                coarse_scope_exclusions=artifact["exclusions"],results=observed)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--junit",action="append",default=[])
    parser.add_argument("--output",required=True)
    parser.add_argument("--stage2",action="store_true")
    parser.add_argument("--require-complete",action="store_true")
    args=parser.parse_args()
    try:
        artifact=json.loads((TEAM/"generator/generated_cases.json").read_text(encoding="utf-8"))
        ledger=json.loads((TEAM/"api/case_ledger.json").read_text(encoding="utf-8"))
        report=validate(artifact,ledger,build(),args.junit,stage2=args.stage2,
                        expected_source=os.environ.get("AREA2_SOURCE_SHA") or os.environ.get("GITHUB_SHA"))
        Path(args.output).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        print("COVERAGE_SUMMARY "+json.dumps({k:v for k,v in report.items() if k!="results"}),flush=True)
        good=report["complete_scope_accepted"] if args.require_complete else report["stage2_accepted"]
        return 0 if good else 3
    except (ValueError,KeyError,OSError,ET.ParseError) as error:
        print("Coverage refused: "+str(error)); return 4


if __name__=="__main__":
    raise SystemExit(main())
