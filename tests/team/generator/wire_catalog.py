"""Deterministic runtime input reader; complements the one canonical OpenAPI JSON."""
import copy
import hashlib
import json
from pathlib import Path

TEAM = Path(__file__).resolve().parents[1]
ROOT = TEAM.parents[1]


def source_inventory():
    path = TEAM / "generator/wire_inputs.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    # The source snapshot also supports independent local development.
    inventory = json.loads((ROOT / "docs/team/finish-line/OPERATION_INPUT_INVENTORY.json").read_text(encoding="utf-8"))
    for op in inventory["operations"]:
        op["role"] = op["context"]["binding_role"]
    return inventory


def supplements(inventory):
    ops = {r["operation"]:r for r in inventory["operations"]}
    extra = []
    extra.append(dict(id="INPUT:cancel:body:reason",operation="cancel",field="reason",location="body",
        category="declared_generated_input",stage=3,requirements=["FR-09","BR-03"],
        details={"source":"LeaveRequestCancelAPIView.put calls reject_reason_from before request_leave_cancellation",
                 "schema":{"type":"string","nullable":True},
                 "note":"Prompt 3 source-discovered optional reason; real normalization/persistence covered by business consumers."}))
    for op, keys in {"allocation_list":["requested_date","created_at"], "self_allocation_list":["requested_date","created_at"],
                     "leave_list":["created_at"], "leave_type_list":["carryforward_max","total_days"]}.items():
        for name in ("custom_field","custom_lookup","custom_value"):
            extra.append(dict(id=f"INPUT:{op}:query:{name}", operation=op, field=name, location="query",
                              category="advanced_query", stage=2, requirements=ops[op]["requirements"],
                              details={"keys":keys,"source":"HorillaFilterSet._apply_custom_filters; leave filter registry"}))
    for op in ops.values():
        if op["method"]=="GET" and ("list" in op["operation"] or op["operation"]=="own_balance"):
            name=op["operation"]
            extra.append(dict(id=f"INPUT:{name}:query:ordering", operation=name, field="ordering", location="query",
                              category="ordering", stage=2, requirements=op["requirements"],
                              details={"source":"Active APIViews have explicit queryset order and no OrderingFilter"}))
    return extra


def classes(row):
    category=row["category"]
    fixed={
        "authentication_roles":["absent","invalid","normal_owner","foreign_owner","exact_permission","reporting_manager"],
        "response_negotiation":["JSON","HTML","wildcard","unsupported"],
        "request_media":["JSON","form","multipart","unsupported","missing_header","malformed_JSON"],
        "whole_body":["omitted","empty_object","null","array","scalar","malformed_JSON","unknown_property"],
        "injection_integrity":["id","created_by","modified_by","employee_id_binding"],
        "multipart_array":["JSON_arrays","repeated_form_keys","invalid_item","mixed_valid_missing","duplicate_ids","cartesian_idempotence"],
        "pagination":["omitted","first","last","beyond_last","zero","negative","malformed"],
        "manager_query":["omitted","true","false","False","all","invalid"],
        "view_query":["omitted","field","nested_field","invalid_field","grouped_page_size"],
        "advanced_query":["valid","unknown_key","unknown_lookup","malformed_value","empty","parallel_rows","unequal_arrays"],
        "ordering":["omitted","id","-id","invalid"]}
    if category in fixed:
        if category=="advanced_query":
            return fixed[category]+[key+":"+label for key in row["details"]["keys"][1:] for label in fixed[category]]
        return fixed[category]
    if category=="declared_generated_input":
        if row["location"]=="path":
            return ["zero","negative","huge_integer","encoded_nonnumeric"]
        if row["location"]=="query":
            return ["numeric_string","whitespace_integer","exponent"]
        schema=row["details"]["schema"]
        if schema.get("format")=="binary":
            return ["JSON_descriptor","multipart_omitted","multipart_empty","unicode_filename"]
        if schema.get("format")=="date":
            return ["datetime_string","invalid_calendar","leap_day","whitespace"]
        return {"number":["numeric_string","whitespace_numeric","fractional","boolean","nonfinite_string"],
                "integer":["numeric_string","whitespace_numeric","fractional","boolean","nonfinite_string"],
                "boolean":["zero","one","true_string","false_string","blank","unrecognized"],
                "array":["null_item","mixed_item","duplicate_ids","repeated_form_keys"],
                "string":["numeric_coercion","boolean","unicode","trimmed"]}[schema["type"]]
    if category=="runtime_filter":
        meta=row["details"]["filter"]; kind=meta["form_field"]
        result=["omitted","empty","matching","nonmatching","malformed"]
        if kind in {"DecimalField","FloatField","IntegerField"}:
            result+=["negative","zero","fractional","nonfinite","threshold_below","threshold_at","threshold_above"]
            if any(v["class"]=="MaxValueValidator" for v in meta.get("validators",[])):
                result+=["validator_below","validator_at","validator_above"]
        elif kind in {"DateField","DateTimeField"}:
            result+=["invalid_calendar","leap_day","before","at","after"]
        elif "MultipleChoice" in kind:
            result+=["repeated_keys","mixed_valid_missing"]
        elif kind=="ChoiceField":
            result+=["choice:"+str(v) for v in meta.get("static_choices",[]) if v]
        elif kind in {"NullBooleanField","BooleanField"}:
            result+=["true","false","null","one","zero"]
        else:
            result+=["whitespace","unicode","case","partial"]
            if row["field"]=="name_or_badge":
                result+=["badge","comma_terms"]
        return result
    raise ValueError("Unsupported mandatory reader: "+category)


def build(inventory=None):
    inventory=inventory or source_inventory()
    ops={r["operation"]:r for r in inventory["operations"]}
    rows=inventory["inputs"]+supplements(inventory)
    cases=[]
    for row in rows:
        if row["stage"]==3:
            continue
        op=ops[row["operation"]]
        for label in classes(row):
            cases.append(dict(id="WIRE:"+row["id"][6:]+":"+label, input_id=row["id"],
                              operation=row["operation"], route=op["route"], method=op["method"],
                              role=op["role"], field=row["field"], location=row["location"],
                              category=row["category"], details=row["details"], requirements=row["requirements"],
                              **{"class":label}))
    if len({r["id"] for r in cases})!=len(cases):
        raise ValueError("Duplicate wire identity")
    return dict(cases=cases, supplemental_inputs=supplements(inventory),
                mandatory_input_families=len(rows),
                source_sha256=hashlib.sha256(json.dumps(inventory,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
                scope_complete=False)


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    result=build(); path=Path(args.output)
    if args.check:
        if json.loads(path.read_text(encoding="utf-8"))!=result:
            raise SystemExit("Stale wire data")
    else:
        path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"wire_cases":len(result["cases"]),"input_families":result["mandatory_input_families"]}))

