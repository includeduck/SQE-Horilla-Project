"""Strict HTTP/state regressions for Prompt 3. Synthetic setup only; no mocks."""
import hashlib
import json
from datetime import date, timedelta

import pytest

from business_catalog import business_rows, reason_rows
from contract_support import balances, grant_operation_permissions, run_generated, state


def observe(h, case_id, family, body, response, before, amounts, expected, **extra):
    h.lineage(case_id, body)
    h.record_property("input_family", family)
    h.record_property("asserted_requirements", json.dumps(extra.get("requirements", [])))
    after, after_amounts = state(), balances(h)
    print("BUSINESS_OBSERVATION "+json.dumps(dict(case_id=case_id, input_family=family,
        request=body, expected_status=expected, actual_status=response.status_code,
        response=response.text[:1500],before=before,after=after,
        before_balances=amounts,after_balances=after_amounts,**extra),default=str,sort_keys=True),flush=True)
    assert response.status_code==expected,(case_id,response.status_code,response.text[:1200])
    if expected>=400:
        assert after==before and after_amounts==amounts,"Refusal changed persistent state/balances"
    return after,after_amounts


@pytest.mark.parametrize("row",business_rows(),ids=lambda r:r["id"])
def test_effective_business_context(leave_http,row):
    from base.models import Holidays, CompanyLeaves
    from leave.models import AvailableLeave, LeaveRequest, LeaveType

    h=leave_http; grant_operation_permissions(h); h.grant(10)
    op,label=row["operation"],row["label"]
    updating=op.endswith("update")
    pk=h.create_leave(h.shifted_leave(400)) if updating else None
    typ=h.context["leave_type"]; employee=h.context["employee"]
    LeaveType.objects.filter(pk=typ.pk).update(reset=False,exclude_holiday="no",exclude_company_leave="no")
    anchor=date.today()+timedelta(days=120)
    anchor+=timedelta(days=(-anchor.weekday())%7)
    body=h.baseline("leave")
    body.update(start_date=anchor.isoformat(),end_date=(anchor+timedelta(days=2)).isoformat())
    body.update(start_date_breakdown="full_day",end_date_breakdown="full_day")
    amount,carry=10,0
    type_changes={}
    if label.startswith("same_day:"):
        _,left,right=label.split(":")
        body.update(end_date=body["start_date"],start_date_breakdown=left,end_date_breakdown=right)
    if label in {"zero_holiday","negative_half_holiday"}:
        body["end_date"]=body["start_date"]
        if label=="negative_half_holiday":
            body.update(start_date_breakdown="first_half",end_date_breakdown="first_half")
    holiday_labels={"holiday","both_overlap","both_distinct","target_holiday","other_holiday","zero_holiday","negative_half_holiday"}
    if label in holiday_labels:
        type_changes["exclude_holiday"]="yes"
        holiday=Holidays.objects.create(name="Synthetic business holiday",start_date=anchor,end_date=anchor,
            is_specific=label in {"target_holiday","other_holiday"},company_id=h.context["company"])
        if holiday.is_specific:
            holiday.employees.add(employee if label=="target_holiday" else h.context["outsider"])
        if label=="other_holiday": amount=2
    if label in {"company","both_overlap","both_distinct"}:
        type_changes["exclude_company_leave"]="yes"
        CompanyLeaves.objects.create(based_on_week=None,based_on_week_day=str((anchor.weekday()+(label=="both_distinct"))%7))
    if label.startswith("balance_"): amount={"balance_below":2.5,"balance_at":3,"balance_above":3.5}[label]
    if label=="no_carry_stale":
        amount,carry=0,5
        type_changes.update(carryforward_type="no carryforward",carryforward_max=10)
    if label.startswith("cap_"):
        amount,carry=0,5
        type_changes.update(carryforward_type="carryforward",carryforward_max={"cap_below":2.5,"cap_at":3,"cap_above":3.5}[label])
    if label.startswith("forecast_"):
        amount=0
        type_changes.update(reset=True,reset_based="custom",custom_reset_days=30,total_days=1)
        start=date.today()+timedelta(days={"forecast_before":29,"forecast_at":30,"forecast_after":31}[label])
        body.update(start_date=start.isoformat(),end_date=start.isoformat())
    if label.startswith("expiry_"):
        amount,carry=0,5
        type_changes.update(carryforward_type="carryforward expire",carryforward_max=3,total_days=0)
    LeaveType.objects.filter(pk=typ.pk).update(**type_changes)
    AvailableLeave.objects.filter(employee_id=employee,leave_type_id=typ).update(
        available_days=amount,carryforward_days=carry,total_leave_days=amount+carry)
    if label.startswith("expiry_"):
        # Exercise the existing expiry lifecycle; validation does not invent a
        # second rule that expires a scheduled balance by requested start date.
        expired=date.today()+timedelta(days={"expiry_before":-1,"expiry_at":0,"expiry_after":1}[label])
        AvailableLeave.objects.filter(employee_id=employee,leave_type_id=typ).update(expired_date=expired)
        available=AvailableLeave.objects.get(employee_id=employee,leave_type_id=typ)
        assert available.expire_carryforward(date.today()) is (label!="expiry_after")
    if label.startswith("overlap_") or label in {"other_employee_overlap","complementary_halves"}:
        owner=h.context["outsider"] if label=="other_employee_overlap" else employee
        old_state=label.removeprefix("overlap_") if label.startswith("overlap_") else "requested"
        half=label=="complementary_halves"
        LeaveRequest.objects.create(employee_id=owner,leave_type_id=typ,start_date=anchor,
            end_date=anchor if half else anchor+timedelta(days=2),status=old_state,
            start_date_breakdown="first_half" if half else "full_day",
            end_date_breakdown="first_half" if half else "full_day",description="Synthetic overlapping setup")
        if half: body.update(end_date=body["start_date"],start_date_breakdown="second_half",end_date_breakdown="second_half")
    files=None
    if label.startswith("attachment_"):
        LeaveType.objects.filter(pk=typ.pk).update(require_attachment="yes")
        if label=="attachment_present": files={"attachment":("proof.txt",b"synthetic business proof","text/plain")}
    if label=="unassigned": AvailableLeave.objects.filter(employee_id=employee,leave_type_id=typ).delete()
    if not op.startswith("self_"): body["employee_id"]=employee.pk
    route="/api/v1/leave/"+("user-request/" if op.startswith("self_") else "request/")
    route+=f"{pk}/" if updating else ""
    before,amounts=state(),balances(h)
    response=h.request("PUT" if updating else "POST",route,"employee" if op.startswith("self_") else "approver",body,files=files)
    after,after_amounts=observe(h,row["id"],row["input_family"],body,response,before,amounts,row["status"],requirements=row["requirements"],expected_days=row["days"])
    if row["status"]==201:
        actual_pk=response.json()["id"]
        assert not updating or actual_pk==pk
        record=LeaveRequest.objects.entire().get(pk=actual_pk)
        assert record.employee_id_id==employee.pk and record.status=="requested"
        assert record.requested_days==row["days"],(label,record.requested_days,row["days"])
        detail=h.leave_detail(actual_pk)
        assert float(detail["requested_days"])==row["days"]
        assert after_amounts==amounts
        assert len(after["leaves"])==len(before["leaves"])+(not updating)
        if files:
            with record.attachment.open("rb") as stream: assert stream.read()==b"synthetic business proof"


def reason_action(h,action,body,case_id):
    from leave.models import LeaveRequest, LeaveAllocationRequest, LeaverequestComment
    h.grant(5)
    pk=h.create_allocation({**h.baseline("allocation"),"description":"Synthetic reason allocation"}) if action=="allocation_reject" else h.create_leave()
    if action!="allocation_reject": h.approve_leave(pk)
    if action=="cancellation_reject":
        assert h.request("PUT",f"/api/v1/leave/cancel/{pk}/",body={"reason":"Original synthetic request"}).status_code==200
    route_name=action.replace("_","-")
    before,amounts=state(),balances(h)
    response=h.request("PUT",f"/api/v1/leave/{route_name}/{pk}/","employee" if action=="cancel" else "approver",body)
    expected=200 if isinstance(body,dict) else 400
    observe(h,case_id,f"INPUT:{action}:body:reason",body,response,before,amounts,expected,requirements=["FR-03" if action=="allocation_reject" else "FR-09","BR-03"])
    if expected==400: return
    raw=body.get("reason")
    normalized=raw.strip()[:1000] if isinstance(raw,str) else ""
    record=(LeaveAllocationRequest if action=="allocation_reject" else LeaveRequest).objects.entire().get(pk=pk)
    assert record.status=={"allocation_reject":"rejected","reject":"rejected","cancel":"cancel_requested","cancellation_reject":"approved"}[action]
    assert record.reject_reason==("" if action=="cancellation_reject" else normalized)
    if action=="cancellation_reject" and normalized:
        comment=LeaverequestComment.objects.filter(request_id=record).order_by("id").last()
        assert normalized in comment.comment
    expected_amount=(5.,0.) if action in {"allocation_reject","reject"} else (2.,0.)
    assert h.balance()==expected_amount
    assert h.balance("approver")==amounts["approver"] and h.balance("outsider")==amounts["outsider"]
    # The SQLite TextField write above and explicit field validation are
    # different observations. No PostgreSQL enforcement is inferred.
    field=record._meta.get_field("reject_reason")
    h.record_property("model_reason_max_length",str(field.max_length))
    h.record_property("helper_reason_limit","1000")
    if field.max_length and len(normalized)>field.max_length:
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError): field.clean(normalized,record)


@pytest.mark.parametrize("row",reason_rows(),ids=lambda r:r["id"])
def test_reason_wire_and_persistence(leave_http,row):
    body=row["value"] if row["label"].startswith("whole_") else {} if row["label"]=="missing" else {"reason":row["value"]}
    reason_action(leave_http,row["action"],body,row["id"])


@pytest.mark.parametrize("case_id",[
    f"{op}:body:reason:EP:{label}" for op in ("allocation_reject","cancellation_reject","reject")
    for label in ("valid","missing","null","wrong-type","empty")
]+[f"{op}:body:end_date:BVA:date-order-{label}" for op in ("leave_create","leave_update") for label in ("below","at","above")])
def test_remaining_generated_business_cases(leave_http,case_id):
    h=leave_http; case=h.case(case_id)
    if case["field"]==["reason"]:
        h.record_property("schema_predicate",case["expected"]["predicate"])
        h.record_property("binding_transform","reject_reason_from ignores nonstring/null; schema class is not the runtime refusal oracle")
        reason_action(h,case["operation"],case["request"]["body"],case_id)
    else:
        run_generated(h,case)


@pytest.mark.parametrize("policy,cap,expected",[("no carryforward",10,400),("carryforward",1,400),("carryforward",3,200)])
def test_approval_rechecks_current_policy(leave_http,policy,cap,expected):
    from leave.models import AvailableLeave,LeaveType
    h=leave_http; h.grant(5); pk=h.create_leave()
    LeaveType.objects.filter(pk=h.context["leave_type"].pk).update(carryforward_type=policy,carryforward_max=cap,reset=False)
    AvailableLeave.objects.filter(employee_id=h.context["employee"],leave_type_id=h.context["leave_type"]).update(available_days=0,carryforward_days=5,total_leave_days=5)
    before,amounts=state(),balances(h)
    response=h.request("PUT",f"/api/v1/leave/approve/{pk}/","approver",{})
    observe(h,f"APPROVE-POLICY:{policy}:{cap}","BR-01:approval",{},response,before,amounts,expected,requirements=["FR-08","BR-01","BR-03"])
    if expected==200:
        assert h.balance()==(0.,2.) and h.leave_detail(pk)["status"]=="approved"
        assert h.balance("approver")==amounts["approver"]


def test_malformed_approved_allocation_rejection_is_atomic(leave_http):
    h=leave_http; pk=h.grant(5); before,amounts=state(),balances(h)
    response=h.request("PUT",f"/api/v1/leave/allocation-reject/{pk}/","approver",[])
    observe(h,"REJECT-ALLOCATION:malformed-approved-body","BR-03:allocation-reject",[],response,before,amounts,400,requirements=["FR-03","BR-03"])
