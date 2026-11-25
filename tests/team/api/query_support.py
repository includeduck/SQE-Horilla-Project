"""Independent fixtures/predicates for the existing real-server query consumers."""
from datetime import date, datetime, timedelta
from decimal import Decimal, localcontext
import json

from contract_support import balances, prepare, send, state


def query_model(op):
    from leave.models import AvailableLeave, LeaveAllocationRequest, LeaveRequest, LeaveType
    if op in {"leave_type_list","employee_leave_type_list"}:
        return LeaveType
    if "allocation" in op:
        return LeaveAllocationRequest
    if op in {"leave_list","self_leave_list"}:
        return LeaveRequest
    return AvailableLeave


def create_reference(model,h,depth=0,force_new=False):
    from django.db import models
    from django.utils import timezone
    for key in ("employee","company","leave_type","employee_user"):
        if not force_new and isinstance(h.context[key],model):
            return h.context[key]
    existing=None if force_new else model._base_manager.first()
    if existing:
        return existing
    assert depth<5,("Unbound reference cycle",model.__name__)
    fields={}
    for f in model._meta.concrete_fields:
        if f.primary_key or f.auto_created or f.has_default() or f.null or f.blank:
            continue
        if f.is_relation:
            fields[f.name]=create_reference(f.related_model,h,depth+1)
        elif f.choices:
            fields[f.name]=list(f.flatchoices)[0][0]
        elif isinstance(f,models.DateTimeField):
            fields[f.name]=timezone.now()
        elif isinstance(f,models.DateField):
            fields[f.name]=date(2030,1,7)
        elif isinstance(f,models.BooleanField):
            fields[f.name]=False
        elif isinstance(f,(models.IntegerField,models.FloatField,models.DecimalField)):
            fields[f.name]=1
        else:
            fields[f.name]=("Wire "+f.name)[:f.max_length or 40]
    return model._base_manager.create(**fields)


def value_at(obj,path,h=None,materialize=False):
    for name in path.split("__"):
        value=getattr(obj,name,None)
        if hasattr(value,"all"):
            target=value.first()
            if target is None and materialize:
                target=create_reference(value.model,h); value.add(target)
            value=target
        if value is None and materialize:
            f=obj._meta.get_field(name)
            if f.is_relation:
                value=create_reference(f.related_model,h)
            elif f.get_internal_type()=="DateField":
                value=date(2030,1,7)
            elif f.get_internal_type()=="DateTimeField":
                from django.utils import timezone
                value=timezone.now()
            elif f.get_internal_type() in {"FloatField","IntegerField","DecimalField"}:
                value=1
            else:
                value="Wire value"
            setattr(obj,name,value); obj.save(update_fields=[name])
        obj=value
        if obj is None:
            break
    return obj


def scalar(value):
    return value.pk if hasattr(value,"pk") else value


def compare(actual,token,lookup):
    actual=scalar(actual)
    if actual is None:
        return False
    if lookup=="icontains":
        return str(token).casefold() in str(actual).casefold()
    if isinstance(actual,bool):
        token=str(token).lower() in {"true","1"}
    elif isinstance(actual,(int,float,Decimal)):
        actual,token=Decimal(str(actual)),Decimal(str(token))
    elif isinstance(actual,datetime):
        from django.utils import timezone
        token=datetime.fromisoformat(str(token))
        if timezone.is_aware(actual) and timezone.is_naive(token):
            token=timezone.make_aware(token)
    elif isinstance(actual,date):
        token=date.fromisoformat(str(token))
    else:
        token=str(token)
    return {"exact":lambda:actual==token,"gte":lambda:actual>=token,"lte":lambda:actual<=token,
            "gt":lambda:actual>token,"lt":lambda:actual<token}[lookup]()


def read_fixture(h,case,count=2):
    from leave.models import AvailableLeave, LeaveAllocationRequest, LeaveRequest, LeaveType
    ctx=prepare(h,case); op=case["operation"]
    if "allocation" in op:
        for i in range(count):
            h.create_allocation({**h.baseline("allocation"),"description":f"Wire allocation {i}","requested_days":i+1})
        LeaveAllocationRequest.objects.create(employee_id=h.context["outsider"],leave_type_id=h.context["leave_type"],
                                              requested_days=7,description="Wire foreign",created_by=h.context["outsider_user"])
    elif op in {"leave_list","self_leave_list"}:
        for i in range(count):
            body=h.shifted_leave(i*7); body["description"]=f"Wire leave {i}"
            h.create_leave(body)
        LeaveRequest.objects.create(employee_id=h.context["outsider"],leave_type_id=h.context["leave_type"],
                                    start_date=date(2031,1,1),end_date=date(2031,1,1),description="Wire foreign")
        # Query-only fixture: distinguish current approved versus future rows.
        first=LeaveRequest.objects.entire().filter(employee_id=h.context["employee"]).order_by("pk").first()
        LeaveRequest.objects.entire().filter(pk=first.pk).update(start_date=date.today(),end_date=date.today(),status="approved")
    else:
        for i in range(count):
            typ=LeaveType.objects.create(name=f"Wire type {i}",total_days=i+1,limit_leave=True,
                                         require_attachment="no",require_approval="yes")
            if op!="leave_type_list":
                AvailableLeave.objects.create(employee_id=h.context["employee"],leave_type_id=typ,available_days=i+1)
    return ctx


def fetch(h,ctx,query=None):
    response=send(h,ctx,None,query=query)
    assert response.status_code==200,(ctx,response.status_code,response.text[:1000])
    result=response.json()
    return result["results"],result


def assert_read(h,case,ctx,query,expected,*,status=200,ordered=False):
    before,amounts=state(),balances(h)
    response=send(h,ctx,None,query=query)
    after,after_amounts=state(),balances(h)
    if response.status_code!=status:
        print("HTTP_REPRODUCTION "+json.dumps(dict(case_id=case["id"],query=query,
            expected_status=status,actual_status=response.status_code,before=before,after=after,
            before_balances=amounts,after_balances=after_amounts),default=str,sort_keys=True),flush=True)
    assert response.status_code==status,(case["id"],query,response.status_code,response.text[:1200])
    if status==200:
        actual=[r["id"] for r in response.json()["results"]]
        assert (actual==expected if ordered else set(actual)==set(expected)),(case["id"],query,actual,expected)
        assert len(actual)==len(set(actual))
    else:
        assert response.content
    assert after==before and after_amounts==amounts


def run_filter(h,case):
    ctx=read_fixture(h,case); op,field,label=case["operation"],case["field"],case["class"]
    meta=case["details"]["filter"]; kind=meta["form_field"]; lookup=meta["lookup_expr"]
    rows,_=fetch(h,ctx,{"page_size":100}); ids=[r["id"] for r in rows]
    assert len(ids)>=2
    model=query_model(op); records=[model.objects.entire().get(pk=pk) for pk in ids]
    query,expected={"page_size":100},ids
    if label in {"omitted","empty"}:
        if label=="empty": query[field]=""
        return assert_read(h,case,ctx,query,expected)
    custom=meta.get("method"); path=meta["field_name"]
    if field in {"search","name_or_badge"} and op!="leave_type_list" and not(op=="self_leave_list" and field=="search"):
        if label=="badge":
            employee=h.context["employee"]; employee.badge_id="WIRE-001"
            employee.save(update_fields=["badge_id"])
        token="Employee" if label in {"matching","case","partial","whitespace"} else "NO-SUCH-WIRE"
        if label=="case": token=token.lower()
        if label=="partial": token="mploy"
        if label=="whitespace": token="  Employee  "
        if label=="badge": token="WIRE-001"
        if label=="comma_terms": token=" Employee, Outsider "
        terms=[term.strip().casefold() for term in token.split(",")] if field=="name_or_badge" else [token.strip().casefold()]
        expected=[r.pk for r in records if any(term in (
            str(r.employee_id.employee_first_name)+" "+str(r.employee_id.employee_last_name)+" "+str(r.employee_id.badge_id)).casefold() for term in terms)]
    elif field=="search_field":
        token="description" if label=="matching" else "not_a_real_field"
        if label=="unicode": token="غیرموجود"
        if label=="whitespace": token=" description "
        if label=="case": token="DESCRIPTION"
        if label=="partial": token="descr"
        query["search"]="wire"
        expected=[r.pk for r in records if "wire" in r.description.lower()] if token=="description" else []
    elif field=="overall_leave":
        token="month" if label=="matching" else "invalid-window"
        today=date.today()
        expected=[r.pk for r in records if r.status in {"approved","cancel_requested"} and r.start_date<=today<=r.end_date]
    elif field=="today_leave":
        token={"matching":"true","true":"true","one":"1","nonmatching":"false","false":"false","zero":"0","null":"null"}.get(label,"unknown")
        expected=[r.pk for r in records if r.start_date<=date.today()<=(r.end_date or r.start_date)] if token=="true" else ids
    elif field=="payment" and op=="leave_list":
        token=label.split(":",1)[1] if label.startswith("choice:") else "paid" if label=="matching" else "unpaid" if label=="nonmatching" else "invalid-choice"
        expected=[r.pk for r in records if (r.leave_type_id.payment=="paid")==(token=="paid")] if token in {"paid","unpaid"} else ids
    else:
        if custom=="filter_from_date": path="end_date"
        actual=value_at(records[0],path,h,True)
        for record in records: record.refresh_from_db()
        if "MultipleChoice" in kind:
            ref=scalar(actual); token=[ref]
            if label=="nonmatching":
                related=type(actual)
                other=related._base_manager.exclude(pk=ref).first() or create_reference(related,h,force_new=True)
                if op=="self_leave_list" and field=="leave_type_id":
                    # UserLeaveRequestFilter restricts choices to types in the
                    # caller's requests. An unused type is an invalid choice and
                    # is ignored, so bind a distinct VALID type to a second row.
                    # The filter must then exclude the first row and select the
                    # second exactly, rather than weakening the result oracle.
                    assert len(records)>=2
                    from leave.models import AvailableLeave
                    AvailableLeave.objects.get_or_create(employee_id=h.context["employee"],leave_type_id=other)
                    type(records[1]).objects.entire().filter(pk=records[1].pk).update(leave_type_id=other)
                    records[1].refresh_from_db()
                token=[other.pk]
                expected=[r.pk for r in records if scalar(value_at(r,path))==other.pk]
            elif label in {"malformed","mixed_valid_missing"}:
                token=[ref,2147483647] if label=="mixed_valid_missing" else ["not-an-id"]
                expected=ids
            else:
                if label=="repeated_keys": token=[ref,ref]
                expected=[r.pk for r in records if scalar(value_at(r,path))==ref]
        elif kind in {"DecimalField","FloatField","IntegerField"}:
            anchor=Decimal(str(actual)); token=str(anchor)
            if label in {"malformed","nonfinite"}:
                token="NaN" if label=="nonfinite" else "not-a-number"; expected=ids
            else:
                if label.startswith("threshold_"):
                    token=str(anchor+{"threshold_below":-1,"threshold_at":0,"threshold_above":1}[label])
                elif label=="nonmatching": token="2147483647"
                elif label=="negative": token="-1"
                elif label=="zero": token="0"
                elif label=="fractional": token="0.5"
                elif label.startswith("validator_"):
                    bound=next(v["limit_value"] for v in meta["validators"] if v["class"]=="MaxValueValidator")
                    with localcontext() as precision:
                        precision.prec=100
                        # The live MaxValueValidator stores a Python float;
                        # Decimal(str(1e50))+1 is still below that float's actual
                        # value. Use its exact representation for +/-1 BVA.
                        exact=Decimal.from_float(float(bound))
                        token=str(exact+{"validator_below":-1,"validator_at":0,"validator_above":1}[label])
                expected=ids if label=="validator_above" else [r.pk for r in records if compare(value_at(r,path),token,lookup)]
        elif kind in {"DateField","DateTimeField"}:
            anchor=actual.date() if isinstance(actual,datetime) and kind=="DateField" else actual
            token=anchor.isoformat()
            if label in {"malformed","invalid_calendar"}:
                token="2030-02-30"; expected=ids
            else:
                if label in {"before","after"}: token=(anchor+timedelta(days=-1 if label=="before" else 1)).isoformat()
                elif label=="leap_day": token="2032-02-29T00:00:00+05:00" if kind=="DateTimeField" else "2032-02-29"
                elif label=="nonmatching": token="2099-12-31"
                if custom=="filter_from_date":
                    bound=date.fromisoformat(token)
                    expected=[r.pk for r in records if (r.end_date is not None and r.end_date>=bound) or (r.end_date is None and r.start_date>=bound)]
                else:
                    expected=[r.pk for r in records if compare(value_at(r,path),token,lookup)]
        elif kind in {"NullBooleanField","BooleanField"}:
            token={"matching":"true","true":"true","one":"1","nonmatching":"false","false":"false","zero":"0","null":"null"}.get(label,"unknown")
            # Django NullBooleanField recognizes true/false; 1/0 and literal null
            # normalize to None and leave the filter unapplied.
            boolean=True if token=="true" else False if token=="false" else None
            expected=ids if boolean is None else [r.pk for r in records if bool(value_at(r,path)) is boolean]
            if field=="is_active": expected=[] if boolean is False else ids
        elif kind=="ChoiceField":
            allowed=[str(v) for v in meta.get("static_choices",[]) if v]
            token=label.split(":",1)[1] if label.startswith("choice:") else str(actual) if label=="matching" else "invalid-choice"
            expected=[r.pk for r in records if str(value_at(r,path))==token] if token in allowed else ids
        else:
            token=str(actual)
            if label in {"nonmatching","malformed","unicode"}: token="غیرموجود" if label=="unicode" else "NO-SUCH-WIRE"
            elif label=="case": token=token.swapcase()
            elif label=="partial": token=token[:max(1,len(token)//2)]
            elif label=="whitespace": token="  "+token+"  "
            expected=[r.pk for r in records if compare(value_at(r,path),token.strip(),lookup)]
    query[field]=token
    h.record_property("bound_query",str(query))
    assert_read(h,case,ctx,query,expected)


def run_query(h,case):
    category,label=case["category"],case["class"]
    if category=="runtime_filter": return run_filter(h,case)
    ctx=read_fixture(h,case,23 if category=="pagination" else 2)
    query={"page_size":100}; rows,_=fetch(h,ctx,query); ids=[r["id"] for r in rows]
    if category=="ordering":
        if label!="omitted": query["ordering"]=label
        return assert_read(h,case,ctx,query,ids,ordered=True)
    if category=="pagination":
        query={}
        token={"first":1,"last":"last","beyond_last":999999,"zero":0,"negative":-1,"malformed":"invalid"}.get(label)
        if token is not None: query["page"]=token
        expected=ids[(len(ids)-1)//20*20:] if label=="last" else ids[:20]
        return assert_read(h,case,ctx,query,expected,status=404 if label in {"beyond_last","zero","negative","malformed"} else 200,ordered=True)
    if category=="manager_query":
        from leave.models import AvailableLeave
        if case["operation"]=="employee_leave_type_list":
            AvailableLeave.objects.entire().filter(employee_id=h.context["employee"],leave_type_id_id=ids[0]).update(is_active=False)
        else:
            query_model(case["operation"]).objects.entire().filter(pk=ids[0]).update(is_active=False)
        if label!="omitted": query["is_active"]=label
        return assert_read(h,case,ctx,query,[ids[0]] if label in {"false","False"} else ids[1:])
    if category=="view_query":
        if label=="omitted": return assert_read(h,case,ctx,query,ids)
        before,amounts=state(),balances(h)
        query["groupby_field"]="id" if label in {"field","grouped_page_size"} else "employee_id__employee_first_name" if label=="nested_field" else "not_a_real_field"
        if label=="grouped_page_size": query["page_size"]=1
        response=send(h,ctx,None,query=query)
        assert response.status_code==(400 if label=="invalid_field" else 200),(case["id"],response.text[:1000])
        if label!="invalid_field":
            groups=response.json()["results"]
            assert sum(g["count"] for g in groups)==len(ids)
            assert all(g["name"] and "filter_url" in g for g in groups)
            if label=="grouped_page_size": assert len(groups)==len(ids)
        assert state()==before and balances(h)==amounts
        return
    if category=="advanced_query":
        key=case["details"]["keys"][0]
        if ":" in label:
            key,label=label.split(":",1)
        number=key in {"carryforward_max","total_days"}
        token="0" if number else "2000-01-01"
        query.update(custom_field=[key],custom_lookup=["gte"],custom_value=[token])
        if label=="unknown_key": query["custom_field"]=["not_a_real_field"]
        elif label=="unknown_lookup": query["custom_lookup"]=["regex"]
        elif label=="malformed_value": query["custom_value"]=["not-a-value"]
        elif label=="empty": query["custom_value"]=[""]
        elif label=="parallel_rows": query.update(custom_field=[key,key],custom_lookup=["gte","lte"],custom_value=[token,"999999" if number else "2099-12-31"])
        elif label=="unequal_arrays": query["custom_field"]=[key,"ignored"]
        expected=ids
        if label not in {"unknown_key","unknown_lookup","malformed_value","empty"}:
            model=query_model(case["operation"])
            expected=[pk for pk in ids if value_at(model.objects.entire().get(pk=pk),key) is not None]
        return assert_read(h,case,ctx,query,expected,status=400 if label=="malformed_value" and not number else 200)
    raise AssertionError("Missing query consumer "+category)

