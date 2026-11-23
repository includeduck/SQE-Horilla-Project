"""FR-01, FR-10, R3-R5: five generated cases over real loopback HTTP.

No mock endpoints. No whole-suite completion claim: full coverage belongs to C.
"""

import json

import pytest


CASE_IDS = [
    "self_allocation_create:body:requested_days:EP:valid",
    "self_allocation_create:body:requested_days:EP:nonnumeric",
    "self_allocation_create:body:attachment:BVA:x-filename-maxLength-below",
    "self_allocation_create:body:attachment:BVA:x-filename-maxLength-at",
    "self_allocation_create:body:attachment:BVA:x-filename-maxLength-above",
]


def rows(response):
    assert response.status_code == 200, response.text[:500]
    payload = response.json()
    return payload["results"] if isinstance(payload, dict) else payload


def login(session, base, username, password):
    response = session.post(base + "/api/v1/auth/login/", json={"username": username, "password": password}, timeout=30)
    assert response.status_code == 200, response.text[:500]
    # Keep tokens in memory; never print or persist login response bodies.
    return {"Authorization": "Bearer " + response.json()["access"]}


@pytest.mark.parametrize("case_id", CASE_IDS, ids=CASE_IDS)
def test_generated_allocation(case_id, live_server, area2_seed, area2_http, runtime_cases, record_property):
    from leave.models import AvailableLeave, LeaveAllocationRequest

    case = next(case for case in runtime_cases["cases"] if case["id"] == case_id)
    for key in ("spec_sha256", "bindings_sha256", "data_sha256"):
        record_property(key, runtime_cases[key])
    record_property("case_id", case_id)
    print(json.dumps({"case_id": case_id, "spec_sha256": runtime_cases["spec_sha256"],
                      "data_sha256": runtime_cases["data_sha256"]}))
    base = live_server.url
    employee_headers = login(area2_http, base, "team_employee", "TeamEmploy#2026")
    approver_headers = login(area2_http, base, "team_approver", "TeamApprove#2026")
    employee = area2_seed["employee"]
    leave_type = area2_seed["leave_type"]
    collection = base + "/api/v1/leave/user-allocation-request/"
    balance_url = base + "/api/v1/leave/available-leave/"
    before_rows = rows(area2_http.get(collection, headers=employee_headers, timeout=30))
    before_balance = rows(area2_http.get(balance_url, headers=employee_headers, timeout=30))
    assert before_rows == []
    own = [r for r in before_balance if r["leave_type_id"]["id"] == leave_type.pk]
    assert len(own) == 1 and float(own[0]["available_days"]) == 0
    assert float(own[0]["carryforward_days"]) == 0
    assert case["media_type"] == "multipart/form-data"
    payload = dict(case["request"]["body"])
    descriptor = payload.pop("attachment")
    assert isinstance(descriptor, dict), "Only serialized file descriptors selected in B"
    files = {"attachment": (descriptor["filename"], descriptor["text"].encode("utf-8"), descriptor["content_type"])}
    response = area2_http.post(base + case["route"], headers=employee_headers, data=payload, files=files, timeout=30)
    accepted = case["expected"]["predicate"] == "accept"
    assert response.status_code == (200 if accepted else 400), response.text[:500]
    after_rows = rows(area2_http.get(collection, headers=employee_headers, timeout=30))
    after_balance = rows(area2_http.get(balance_url, headers=employee_headers, timeout=30))
    assert after_balance == before_balance
    assert rows(area2_http.get(balance_url, headers=approver_headers, timeout=30)) == []
    balances = AvailableLeave.objects.filter(employee_id=employee, leave_type_id=leave_type)
    assert balances.count() == 1 and balances.get().available_days == 0
    allocations = LeaveAllocationRequest.objects.filter(employee_id=employee, leave_type_id=leave_type)
    if accepted:
        assert len(after_rows) == 1
        record = after_rows[0]
        assert record["employee_id"]["id"] == employee.pk
        assert record["leave_type_id"]["id"] == leave_type.pk
        assert record["status"] == "requested"
        assert float(record["requested_days"]) == float(payload["requested_days"])
        detail = area2_http.get(base + f"/api/v1/leave/allocation-request/{record['id']}/", headers=employee_headers, timeout=30)
        assert detail.status_code == 200
        assert detail.json()["description"] == payload["description"]
        assert detail.json()["attachment"]
        assert allocations.count() == 1
        stored = allocations.get()
        assert stored.status == "requested" and stored.requested_days == float(payload["requested_days"])
        # HorillaModel.created_by points to HorillaUser, not Employee.
        assert stored.created_by_id == area2_seed["employee_user"].pk
        with stored.attachment.open("rb") as attachment:
            assert attachment.read() == descriptor["text"].encode("utf-8")
    else:
        field = case["field"][-1]
        assert field in response.json() and response.json()[field], response.text[:500]
        assert after_rows == before_rows and allocations.count() == 0
