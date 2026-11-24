"""Source-backed Phase C cases and reversible test-oracle assumptions.

This catalog is dependency-free. Existence here means planned/implemented,
never executed. Dates, IDs and balances are bound by the HTTP fixtures.
"""

from itertools import product


def decision_rows():
    rows = []
    names = ("assigned", "ordered", "matching", "attachment", "no_overlap")
    for index, values in enumerate(product((False, True), repeat=5), 1):
        conditions = dict(zip(names, values))
        # A mismatch matters only on a single day; reversed dates cannot be
        # the same date. All 32 rows are retained, including infeasible rows.
        feasible = conditions["ordered"] or conditions["matching"]
        rows.append({
            "id": f"DEC-BR02-{index:02d}", "conditions": conditions,
            "feasible": feasible,
            "reason": "" if feasible else "Reversed dates cannot be a same-day breakdown mismatch",
            "expected_status": 201 if all(values) else 400,
            "requirements": ["FR-05", "FR-07", "BR-02"],
        })
    return rows


def authorization_rows():
    return [
        {"id": f"AUTH-BR04-{index:02d}", "owner": owner,
         "permission": permission, "manager": manager,
         "expected_status": 200 if not owner and (permission or manager) else 403,
         "requirements": ["FR-08", "BR-04"]}
        for index, (owner, permission, manager) in enumerate(
            product((False, True), repeat=3), 1
        )
    ]


ALLOCATION_STATES = ("requested", "approved", "rejected")
LEAVE_STATES = ("requested", "approved", "rejected", "cancel_requested", "cancelled")


def state_rows():
    rows = []
    for state in ALLOCATION_STATES:
        rows.append({"id": f"STATE-ALLOC-{state}-self-approve", "kind": "allocation",
                     "state": state, "action": "self-approve", "allowed": False,
                     "target": state, "expected_status": 403,
                     "requirements": ["BR-03", "BR-04"]})
        for action in ("approve", "reject", "update", "delete"):
            allowed = state == "requested" or (state == "approved" and action == "reject")
            target = {"approve": "approved", "reject": "rejected",
                      "update": "requested", "delete": "deleted"}[action] if allowed else state
            rows.append({"id": f"STATE-ALLOC-{state}-{action}", "kind": "allocation",
                         "state": state, "action": action, "allowed": allowed,
                         "target": target, "expected_status": 201 if allowed and action == "update" else 200 if allowed else 400,
                         "requirements": ["FR-02", "FR-03", "FR-04", "BR-03"]})
    for state in LEAVE_STATES:
        for action in ("approve", "reject", "cancel", "cancellation-approve",
                       "cancellation-reject", "update", "delete"):
            target = state
            allowed = False
            if state == "requested" and action in {"approve", "reject", "update", "delete"}:
                target = {"approve": "approved", "reject": "rejected",
                          "update": "requested", "delete": "deleted"}[action]
                allowed = True
            elif state == "approved" and action in {"reject", "cancel"}:
                target = "rejected" if action == "reject" else "cancel_requested"
                allowed = True
            elif state == "cancel_requested" and action in {"cancellation-approve", "cancellation-reject"}:
                target = "cancelled" if action == "cancellation-approve" else "approved"
                allowed = True
            rows.append({"id": f"STATE-LEAVE-{state}-{action}", "kind": "leave",
                         "state": state, "action": action, "allowed": allowed,
                         "target": target, "expected_status": 201 if allowed and action == "update" else 200 if allowed else 400,
                         "requirements": ["FR-08", "FR-09", "BR-03"]})
    return rows


def selected_generated_cases(artifact):
    """Expand supported self-create/update body classes; no unknown case is hidden.

    Path/action/generic and remaining query coverage stay explicitly unfinished.
    File inputs are exercised separately by the multipart B consumer, because
    JSON cannot represent an uploaded file. Non-file cases use an otherwise
    valid baseline without the optional attachment. This deliberate scenario
    binding is recorded in the HTTP lineage rather than called a raw replay.
    """
    operations = {"self_allocation_create", "self_leave_create",
                  "self_allocation_update", "self_leave_update"}
    already_in_b = {
        "self_allocation_create:body:requested_days:EP:valid",
        "self_allocation_create:body:requested_days:EP:nonnumeric",
    }
    selected = [case for case in artifact["cases"]
                if case["operation"] in operations and case["location"] == "body"
                and case["field"] != ["attachment"] and case["id"] not in already_in_b]
    return selected


def effective_balance(available, carryforward, policy, cap, forecast=0):
    """Test oracle derived from LeaveRequest.clean, not imported product code."""
    carry = min(carryforward, cap) if policy in {"carryforward", "carryforward expire"} else 0
    return available + carry + forecast
