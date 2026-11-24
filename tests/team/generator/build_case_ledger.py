"""Rebuild mappings without marking any consumer executed."""
import argparse
import json
import sys
from pathlib import Path
TEAM=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TEAM/"generator"))
from wire_catalog import build


def build_ledger():
    path=TEAM/"api/case_ledger.json"
    ledger=json.loads(path.read_text(encoding="utf-8"))
    ledger["entries"]=[r for r in ledger["entries"] if r["file"]!="test_runtime_wire.py"]
    wire=build()
    ledger["entries"] += [dict(case_id=r["id"],file="test_runtime_wire.py",generated=False,
                                applicability="mandatory",implementation_status="implemented",
                                execution_status="pending-current-build",input_family=r["input_id"]) for r in wire["cases"]]
    ledger["implemented_api_cases"]=len(ledger["entries"])
    ledger["wire_cases"]=len(wire["cases"])
    ledger["mandatory_input_families"]=wire["mandatory_input_families"]
    ledger["note"]="Consumer mappings are distinct from current JUnit execution; reason/date-order/relational work remains mandatory in Prompt 3."
    return ledger,wire


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--wire-output")
    args=parser.parse_args(); ledger,wire=build_ledger(); path=TEAM/"api/case_ledger.json"
    if args.check:
        if json.loads(path.read_text(encoding="utf-8"))!=ledger: raise SystemExit("Stale consumer ledger")
    else:
        path.write_text(json.dumps(ledger,indent=2)+"\n",encoding="utf-8")
    if args.wire_output: Path(args.wire_output).write_text(json.dumps(wire,indent=2)+"\n",encoding="utf-8")
    print("WIRE_LEDGER "+json.dumps({k:ledger[k] for k in ("implemented_api_cases","wire_cases","mandatory_input_families")}))
