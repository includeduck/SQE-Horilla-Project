"""Prompt 3's independent business inputs; catalog entries are not test results."""
from itertools import product

OPERATIONS = ("self_leave_create", "self_leave_update", "leave_create", "leave_update")
BREAKDOWNS = ("full_day", "first_half", "second_half")


def business_rows():
    rows = []
    scenarios = [
        ("positive", "effective_duration", 3, 201),
        ("zero_holiday", "effective_duration", 0, 400),
        ("negative_half_holiday", "effective_duration", -.5, 400),
        ("holiday", "holidays", 2, 201),
        ("company", "holidays", 2, 201),
        ("both_overlap", "holidays", 2, 201),
        ("both_distinct", "holidays", 1, 201),
        ("target_holiday", "holidays", 2, 201),
        ("other_holiday", "holidays", 3, 400),
        ("balance_below", "effective_duration", 3, 400),
        ("balance_at", "effective_duration", 3, 201),
        ("balance_above", "effective_duration", 3, 201),
        ("no_carry_stale", "effective_duration", 3, 400),
        ("cap_below", "effective_duration", 3, 400),
        ("cap_at", "effective_duration", 3, 201),
        ("cap_above", "effective_duration", 3, 201),
        ("forecast_before", "effective_duration", 1, 400),
        ("forecast_at", "effective_duration", 1, 201),
        ("forecast_after", "effective_duration", 1, 201),
        ("expiry_before", "effective_duration", 3, 400),
        ("expiry_at", "effective_duration", 3, 400),
        ("expiry_after", "effective_duration", 3, 201),
        ("overlap_requested", "breakdown_overlap_attachment", 3, 400),
        ("overlap_approved", "breakdown_overlap_attachment", 3, 400),
        ("overlap_cancel_requested", "breakdown_overlap_attachment", 3, 400),
        ("overlap_rejected", "breakdown_overlap_attachment", 3, 201),
        ("overlap_cancelled", "breakdown_overlap_attachment", 3, 201),
        ("other_employee_overlap", "breakdown_overlap_attachment", 3, 201),
        ("complementary_halves", "breakdown_overlap_attachment", .5, 201),
        ("attachment_missing", "breakdown_overlap_attachment", 3, 400),
        ("attachment_present", "breakdown_overlap_attachment", 3, 201),
        ("unassigned", "breakdown_overlap_attachment", 3, 400),
    ]
    for operation in OPERATIONS:
        for label, family, days, status in scenarios:
            rows.append(dict(id=f"BUSINESS:{operation}:{label}", operation=operation,
                label=label, days=days, status=status,
                input_family=f"INPUT:{operation}:relational:${family}",
                requirements=["FR-05", "FR-06", "FR-07", "BR-01", "BR-02"]))
        for left, right in product(BREAKDOWNS, repeat=2):
            label=f"same_day:{left}:{right}"
            rows.append(dict(id=f"BUSINESS:{operation}:{label}",operation=operation,
                label=label,days=1 if left=="full_day" else .5,
                status=201 if left==right else 400,
                input_family=f"INPUT:{operation}:relational:$breakdown_overlap_attachment",
                requirements=["FR-05", "BR-01", "BR-02"]))
    return rows


def reason_rows():
    samples = [("missing", None), ("null", None), ("number", 7), ("boolean", True),
        ("object", {"synthetic": True}), ("array", ["synthetic"]), ("empty", ""),
        ("whitespace", " \t\n "), ("meaningful", "  Synthetic reason  "),
        ("unicode", "  \u8acb\u5047 \u0627\u062c\u0627\u0632\u062a  ")]
    samples += [(f"length_{n}", "r"*n) for n in (254,255,256,999,1000,1001)]
    samples += [("whole_array", []), ("whole_scalar", "synthetic")]
    return [dict(id=f"REASON:{action}:{label}",action=action,label=label,value=value,
                 requirements=["FR-03" if action=="allocation_reject" else "FR-09", "BR-03"])
            for action in ("allocation_reject","reject","cancel","cancellation_reject")
            for label,value in samples]


def role_state_rows():
    from case_catalog import state_rows
    return [dict(id=f"ROLE:{row['id']}:{role}", transition=row, role=role,
                 requirements=["FR-02","FR-03","FR-08","FR-09","BR-03","BR-04"])
            for row in state_rows() if row["action"] not in {"self-approve","update","delete"}
            for role in ("employee","manager","permission","outsider")]


def business_entries(artifact):
    entries=[]
    for row in business_rows()+reason_rows()+role_state_rows():
        family=row.get("input_family") or (f"INPUT:{row['action']}:body:reason" if "action" in row else "BR-03/BR-04:state-role")
        entries.append(dict(case_id=row["id"],file="test_business_rules.py",generated=False,
            input_family=family,requirements=row["requirements"]))
    for case in artifact["cases"]:
        if case["field"]==["reason"] or (case["operation"] in {"leave_create","leave_update"} and case["expected"]["oracle"]=="date-order"):
            entries.append(dict(case_id=case["id"],file="test_business_rules.py",generated=True,
                input_family="INPUT:"+case["operation"]+":"+case["location"]+":"+".".join(map(str,case["field"])),
                requirements=["FR-03" if case["operation"]=="allocation_reject" else "FR-09"] if case["field"]==["reason"] else ["FR-05","BR-02"]))
    for policy,cap in (("no carryforward",10),("carryforward",1),("carryforward",3)):
        entries.append(dict(case_id=f"APPROVE-POLICY:{policy}:{cap}",file="test_business_rules.py",generated=False,requirements=["FR-08","BR-01","BR-03"]))
    entries.append(dict(case_id="REJECT-ALLOCATION:malformed-approved-body",file="test_business_rules.py",generated=False,requirements=["FR-03","BR-03"]))
    for kind in ("allocation","leave"):
        entries.append(dict(case_id=f"REFERENCE:{kind}:owner-transfer",file="test_business_rules.py",generated=False,requirements=["FR-04" if kind=="allocation" else "FR-05","BR-04"]))
    for action in ("reject","cancellation-approve"):
        entries.append(dict(case_id="INTEGRATION:CARRY-SPLIT:"+action,file="test_business_rules.py",generated=False,requirements=["FR-01","FR-02","FR-05","FR-06","FR-08","FR-09","FR-10","BR-01","BR-03"]))
    return entries
