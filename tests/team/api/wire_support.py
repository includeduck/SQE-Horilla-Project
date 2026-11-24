"""Execute the deterministic wire catalog through the existing real HTTP fixtures."""
import copy
import json

from contract_support import assert_result, balances, bound_body, prepare, send, state
from query_support import assert_read, fetch, query_model, read_fixture, run_query

IGNORES_BODY={"allocation_approve","cancellation_approve"}
REASON_ACTIONS={"reject","allocation_reject","cancel","cancellation_reject"}


def prototype(h,case):
    original=next(c for c in h.artifact["cases"] if c["operation"]==case["operation"])
    result=copy.deepcopy(original)
    result.update({k:case[k] for k in ("id","operation","method","route","role")})
    result["request"]=copy.deepcopy(original["baseline"])
    return result


def success(case):
    if case["method"] in {"GET","DELETE"} or case["operation"] in {
        "approve","reject","cancel","cancellation_approve","cancellation_reject",
        "allocation_approve","allocation_reject","self_allocation_create"}:
        return 200
    return 201


def auth_status(case,actor):
    op,method=case["operation"],case["method"]
    if actor in {"absent","invalid"}: return 401
    if op.startswith("assignment_"): return success(case) if actor=="exact_permission" else 403
    if op in {"leave_type_list","employee_leave_type_list","own_balance"}: return 200
    if op in {"approve","reject","allocation_approve","allocation_reject","cancellation_approve","cancellation_reject"}:
        return 200 if actor in {"exact_permission","reporting_manager"} else 403
    if op=="cancel": return 200 if actor=="normal_owner" else 400
    if op.startswith("self_"):
        if method=="POST" or ("list" in op and method=="GET"): return success(case)
        if actor=="normal_owner": return success(case)
        return 403 if "allocation" in op else 400
    if method=="GET" and "list" in op:
        return 200 if actor in {"exact_permission","reporting_manager"} else 403
    if method=="POST": return 403 if actor=="foreign_owner" else success(case)
    return 403 if actor=="foreign_owner" else success(case)


def run_auth(h,case):
    proto=prototype(h,case)
    ctx=read_fixture(h,case) if case["method"]=="GET" and ("list" in case["operation"] or case["operation"]=="own_balance") else prepare(h,proto)
    body=bound_body(h,proto); body.pop("attachment",None)
    label=case["class"]
    actor={"normal_owner":"employee","foreign_owner":"outsider","exact_permission":"approver","reporting_manager":"approver"}.get(label,ctx["role"])
    ctx["role"]=actor
    if label=="reporting_manager":
        h.context["approver_user"].user_permissions.clear()
    elif label=="exact_permission":
        from employee.models import EmployeeWorkInformation
        EmployeeWorkInformation.objects.filter(employee_id=h.context["employee"]).update(reporting_manager_id=None)
    owner=actor if case["operation"].startswith("self_") and case["method"]=="POST" else "employee"
    ctx["owner_role"]=owner
    before,amounts=state(),balances(h)
    headers={"Authorization":"" if label=="absent" else "Bearer intentionally-invalid"} if label in {"absent","invalid"} else None
    response=send(h,ctx,body,headers=headers)
    expected=auth_status(case,label)
    original=h.context["employee"]
    try:
        if owner!="employee": h.context["employee"]=h.context[owner]
        assert_result(h,case,ctx,response,before,amounts,body,expected)
    finally:
        h.context["employee"]=original
    if expected==200 and case["method"]=="GET" and case["operation"].startswith("self_"):
        model=query_model(case["operation"])
        own=set(model.objects.entire().filter(employee_id=h.context[actor]).values_list("id",flat=True))
        assert {r["id"] for r in response.json()["results"]}==own


def field_wire(h,case,proto,ctx,body):
    field,label=case["field"],case["class"]; schema=case["details"]["schema"]
    value=body.get(field); encoding,raw,headers="json",None,None; expected=success(case)
    if case["location"]=="path":
        token={"zero":"0","negative":"-1","huge_integer":"9"*100,"encoded_nonnumeric":"not%2Fa%2Fnumber"}[label]
        ctx["route"]=case["route"].replace("{pk}",token)
        expected=404 if label in {"negative","encoded_nonnumeric"} else 400 if case["operation"].startswith(("self_","assignment_")) or case["operation"] in {"cancel","employee_leave_type_list"} else 404
    elif case["location"]=="query":
        query={"page_size":"2" if label=="numeric_string" else " 2 " if label=="whitespace_integer" else "1e2"}
        if case["operation"]=="assignment_detail":
            before,amounts=state(),balances(h); response=send(h,ctx,None,query=query)
            assert response.status_code==200 and response.json()["id"]==ctx["pk"]
            assert state()==before and balances(h)==amounts
            return
        ctx=read_fixture(h,case,3)
        before,amounts=state(),balances(h); response=send(h,ctx,None,query=query)
        assert response.status_code==200,response.text[:1000]
        payload=response.json(); size=2 if label in {"numeric_string","whitespace_integer"} else min(20,payload["count"])
        assert len(payload["results"])==size
        assert state()==before and balances(h)==amounts
        return
    elif schema.get("format")=="binary":
        if label=="JSON_descriptor": raw,headers,expected=json.dumps(body),{"Content-Type":"application/json"},400
        elif label=="multipart_omitted": body.pop(field,None); encoding="multipart"
        elif label=="multipart_empty": body[field]={"filename":"empty.txt","text":"","content_type":"text/plain"}; expected=400
        else: body[field]={"filename":"ثبوت.txt","text":"actual wire bytes","content_type":"text/plain"}
    elif schema.get("format")=="date":
        if label=="leap_day":
            body.update(start_date="2032-02-28",end_date="2032-03-01"); body[field]="2032-02-29"
        else:
            body[field]="2030-01-07T00:00:00Z" if label=="datetime_string" else "2030-02-30" if label=="invalid_calendar" else " 2030-01-07 "
            expected=400
    elif schema["type"] in {"number","integer"}:
        if label=="numeric_string": body[field]=str(value)
        elif label=="whitespace_numeric": body[field]=" "+str(value)+" "
        elif label=="fractional": body[field]=float(value)+.5
        elif label=="boolean":
            body[field]=True
            if schema.get("x-reference"): expected=400
        else: body[field]="NaN"; expected=400
    elif schema["type"]=="boolean":
        body[field]={"zero":0,"one":1,"true_string":"true","false_string":"false","blank":"","unrecognized":"maybe"}[label]
        if label in {"blank","unrecognized"}: expected=400
    elif schema["type"]=="array":
        body[field]=[None] if label=="null_item" else [value[0],2147483647] if label=="mixed_item" else [value[0],value[0]]
        if label in {"null_item","mixed_item"}: expected=400
        if label=="repeated_form_keys": encoding="form"
    else:
        body[field]=42 if label=="numeric_coercion" else True if label=="boolean" else "اردو wire" if label=="unicode" else "  "+str(value)+"  "
        if label=="boolean" or schema.get("enum"): expected=400
    before,amounts=state(),balances(h)
    response=send(h,ctx,body,headers=headers,encoding=encoding,raw=raw)
    assert_result(h,case,ctx,response,before,amounts,body,expected)


def run_wire(h,case):
    h.lineage(case["id"]); h.record_property("input_family",case["input_id"]); h.record_property("wire_class",case["class"])
    category,label=case["category"],case["class"]
    if category in {"runtime_filter","pagination","manager_query","view_query","advanced_query","ordering"}:
        return run_query(h,case)
    if category=="authentication_roles": return run_auth(h,case)
    proto=prototype(h,case)
    if category=="declared_generated_input" and case["location"]=="query" and case["operation"]!="assignment_detail":
        return field_wire(h,case,proto,{}, {})
    ctx=prepare(h,proto); body=bound_body(h,proto)
    if not(category=="declared_generated_input" and case["details"].get("schema",{}).get("format")=="binary"):
        body.pop("attachment",None)
    if category=="declared_generated_input": return field_wire(h,case,proto,ctx,body)
    before,amounts=state(),balances(h)
    headers,raw,encoding=None,None,"json"; expected=success(case)
    if category=="response_negotiation":
        headers={"Accept":{"JSON":"application/json","HTML":"text/html","wildcard":"*/*","unsupported":"application/x-unknown"}[label]}
        if label=="unsupported": expected=406
    elif category=="request_media":
        if label in {"form","multipart"}: encoding=label
        elif label in {"unsupported","missing_header","malformed_JSON"}:
            raw="{" if label=="malformed_JSON" else json.dumps(body)
            headers={"Content-Type":"application/json" if label=="malformed_JSON" else "" if label=="missing_header" else "application/x-unknown"}
            expected=success(case) if case["operation"] in IGNORES_BODY else 400 if label=="malformed_JSON" else 415
    elif category=="whole_body":
        if label=="omitted": body=None
        elif label=="empty_object": body={}
        elif label=="null": body,raw,headers=None,"null",{"Content-Type":"application/json"}
        elif label=="array": body=[]
        elif label=="scalar": body=42
        elif label=="malformed_JSON": raw,headers="{",{"Content-Type":"application/json"}
        else: body["unexpected_wire_key"]={"nested":"ignored"}
        if case["operation"] in IGNORES_BODY: expected=success(case)
        elif case["operation"] in REASON_ACTIONS or case["operation"]=="approve":
            expected=400 if label in {"null","array","scalar","malformed_JSON"} else success(case)
        else: expected=success(case) if label=="unknown_property" else 400
    elif category=="injection_integrity":
        if label=="employee_id_binding":
            body["employee_id"]=h.context["outsider"].pk if case["operation"].startswith("self_") else h.context["employee"].pk
        else:
            body[label]=2147483647
    elif category=="multipart_array":
        if label in {"repeated_form_keys","duplicate_ids"}:
            body["employee_ids"]*=2; body["leave_type_ids"]*=2
            if label=="repeated_form_keys": encoding="form"
        elif label in {"invalid_item","mixed_valid_missing"}:
            body["employee_ids"]=["not-an-ID"] if label=="invalid_item" else [body["employee_ids"][0],2147483647]
            expected=400
    else:
        raise AssertionError("Missing wire consumer "+category)
    response=send(h,ctx,body,headers=headers,raw=raw,encoding=encoding)
    assert_result(h,case,ctx,response,before,amounts,body,expected)
    if category=="response_negotiation" and label=="HTML" and expected<400:
        assert response.headers["Content-Type"].startswith("text/html")
    if category=="multipart_array" and label=="cartesian_idempotence":
        again_before,again_amounts=state(),balances(h)
        again=send(h,ctx,body)
        assert_result(h,case,ctx,again,again_before,again_amounts,body,201)
