"""Reusable Requests assertions for the existing Area 2 real-server fixtures."""

import copy
import json
from datetime import date, timedelta

def response_rows(response):
    assert response.status_code == 200, response.text[:500]
    body = response.json()
    return body["results"] if isinstance(body, dict) else body


class LeaveHTTP:
    def __init__(self, base, session, context, artifact, record_property):
        self.base = base
        self.session = session
        self.context = context
        self.artifact = artifact
        self.record_property = record_property
        self.headers = {}
        for role, username, password in (
            ("employee", "team_employee", "TeamEmploy#2026"),
            ("approver", "team_approver", "TeamApprove#2026"),
            ("outsider", "team_outsider", "TeamOutside#2026"),
        ):
            response = session.post(base + "/api/v1/auth/login/", json={"username": username, "password": password}, timeout=30)
            assert response.status_code == 200, "Synthetic role login failed"
            self.headers[role] = {"Authorization": "Bearer " + response.json()["access"]}
        for key in ("spec_sha256", "bindings_sha256", "data_sha256"):
            record_property(key, artifact[key])

    def request(self, method, route, role="employee", body=None, files=None, query=None):
        kwargs = {"headers": self.headers[role], "timeout": 30}
        if query is not None:
            kwargs["params"] = query
        if files is not None:
            kwargs.update(data=body or {}, files=files)
        elif body is not None:
            kwargs["json"] = body
        return self.session.request(method, self.base + route, **kwargs)

    def case(self, case_id):
        return next(case for case in self.artifact["cases"] if case["id"] == case_id)

    def baseline(self, kind):
        operation = "self_allocation_create" if kind == "allocation" else "self_leave_create"
        case = self.case(f"{operation}:body:description:EP:valid")
        body = copy.deepcopy(case["baseline"]["body"])
        body.pop("attachment", None)
        return body

    def lineage(self, case_id, body=None):
        self.record_property("case_id", case_id)
        info = {"case_id": case_id, "spec_sha256": self.artifact["spec_sha256"],
                "data_sha256": self.artifact["data_sha256"]}
        if body is not None:
            # No credentials, JWTs or real personal data are in these bodies.
            from hashlib import sha256
            info["bound_request_sha256"] = sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
            self.record_property("bound_request_sha256", info["bound_request_sha256"])
        print(json.dumps(info))

    def allocations(self):
        return response_rows(self.request("GET", "/api/v1/leave/user-allocation-request/"))

    def leaves(self):
        return response_rows(self.request("GET", "/api/v1/leave/user-request/"))

    def balance(self, role="employee"):
        records = response_rows(self.request("GET", "/api/v1/leave/available-leave/", role))
        own = [row for row in records if row["leave_type_id"]["id"] == self.context["leave_type"].pk]
        if not own:
            return None
        assert len(own) == 1
        return (float(own[0]["available_days"]), float(own[0]["carryforward_days"]))

    def snapshot(self):
        return {"employee": self.balance(), "approver": self.balance("approver"),
                "outsider": self.balance("outsider"), "allocations": self.allocations(),
                "leaves": self.leaves()}

    def create_allocation(self, body=None):
        before = {row["id"] for row in self.allocations()}
        body = body or self.baseline("allocation")
        response = self.request("POST", "/api/v1/leave/user-allocation-request/", body=body)
        assert response.status_code == 200, response.text[:500]
        created = [row for row in self.allocations() if row["id"] not in before]
        assert len(created) == 1
        record = created[0]
        assert record["employee_id"]["id"] == self.context["employee"].pk
        assert record["status"] == "requested"
        assert float(record["requested_days"]) == float(body["requested_days"])
        return record["id"]

    def grant(self, days=5):
        body = self.baseline("allocation")
        body["requested_days"] = days
        pk = self.create_allocation(body)
        response = self.request("PUT", f"/api/v1/leave/allocation-approve/{pk}/", "approver", {})
        assert response.status_code == 200, response.text[:500]
        assert self.balance() == (float(days), 0.0)
        assert self.balance("approver") == (7.0, 0.0)
        return pk

    def create_leave(self, body=None):
        body = body or self.baseline("leave")
        response = self.request("POST", "/api/v1/leave/user-request/", body=body)
        assert response.status_code == 201, response.text[:500]
        pk = response.json()["id"]
        record = self.leave_detail(pk)
        assert record["status"] == "requested"
        assert record["start_date"] == body["start_date"]
        assert record["end_date"] == body["end_date"]
        return pk

    def leave_detail(self, pk):
        response = self.request("GET", f"/api/v1/leave/user-request/{pk}/")
        assert response.status_code == 200, response.text[:500]
        return response.json()

    def allocation_detail(self, pk):
        response = self.request("GET", f"/api/v1/leave/allocation-request/{pk}/")
        assert response.status_code == 200, response.text[:500]
        return response.json()

    def approve_leave(self, pk):
        response = self.request("PUT", f"/api/v1/leave/approve/{pk}/", "approver", {})
        assert response.status_code == 200, response.text[:500]
        assert self.leave_detail(pk)["status"] == "approved"

    def shifted_leave(self, days):
        body = self.baseline("leave")
        for field in ("start_date", "end_date"):
            body[field] = (date.fromisoformat(body[field]) + timedelta(days=days)).isoformat()
        return body
