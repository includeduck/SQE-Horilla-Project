"""Fresh foundation and actual HTTP schema/serializer introspection."""
import hashlib
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import pytest
from django.conf import settings
from django.db import connection
from django.urls import resolve

pytestmark = pytest.mark.urls("contract_urls")


def field_info(field, depth=0):
    from rest_framework.fields import empty
    row = {"class": type(field).__name__}
    for name in ("required", "read_only", "write_only", "allow_null", "allow_blank",
                 "allow_empty_file", "allow_empty", "min_value", "max_value",
                 "min_length", "max_length"):
        value = getattr(field, name, empty)
        if value is not empty and isinstance(value, (str, int, float, bool, type(None))):
            row[name] = value
    default = getattr(field, "default", empty)
    if default is not empty:
        row["default"] = default if isinstance(default, (str, int, float, bool, type(None))) else type(default).__name__
    choices = getattr(field, "choices", None)
    if choices is not None:
        row["choices"] = [str(key) for key in choices]
    queryset = getattr(field, "queryset", None)
    if queryset is not None:
        row["reference_model"] = queryset.model._meta.label
    child = getattr(field, "child", None)
    if child is not None and depth < 2:
        row["child"] = field_info(child, depth + 1)
    return row


def filters_for(cls):
    filter_class = getattr(cls, "filterset_class", None)
    if not filter_class:
        return {}
    rows = {}
    for name, field in filter_class.base_filters.items():
        row = {"class": type(field).__name__, "field_name": field.field_name,
               "lookup_expr": field.lookup_expr,
               "method": field.method if isinstance(field.method, str) else None}
        try:
            row.update(form_field=type(field.field).__name__, required=field.field.required)
        except Exception as error:
            row["introspection_error"] = type(error).__name__ + ": " + str(error)[:250]
        rows[name] = row
    return rows


def normalized_schema(body):
    rows = []
    for path, item in body.get("paths", {}).items():
        if "/leave/" not in path:
            continue
        route = "/api/v1/" + path[path.index("/leave/") + 1:]
        for method, operation in item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            params = item.get("parameters", []) + operation.get("parameters", [])
            rows.append({"route": route, "method": method.upper(),
                         "original_schema_path": path,
                         "parameters": params, "consumes": operation.get("consumes", body.get("consumes")),
                         "responses": operation.get("responses", {})})
    # Keep definitions so body/response references remain resolvable.
    return {"operations": rows, "definitions": body.get("definitions", {}),
            "securityDefinitions": {name: {k: v for k, v in value.items() if k in ("type", "in", "name")}
                                    for name, value in body.get("securityDefinitions", {}).items()}}


def test_fresh_foundation_and_live_contract(leave_http, record_property):
    from django.core.management import call_command
    from horilla_api.api_serializers.leave import serializers as module
    from leave.models import AvailableLeave, LeaveAllocationRequest, LeaveRequest, LeaveType
    from rest_framework.serializers import BaseSerializer
    h = leave_http
    folder = Path(os.environ["AREA2_CONTRACT_EVIDENCE"])
    folder.mkdir(parents=True, exist_ok=False)
    record_property("case_id", "FOUNDATION-CONTRACT-01")
    assert settings.AREA2_ISOLATED_TESTS is True
    assert Path(connection.settings_dict["NAME"]).resolve().parent == settings.AREA2_TEMP_ROOT.resolve()
    assert connection.settings_dict["ENGINE"] == "django.db.backends.sqlite3"
    assert not LeaveAllocationRequest.objects.exists() and not LeaveRequest.objects.exists()
    call_command("check")
    document = json.loads((Path(__file__).resolve().parents[1] / "generator/openapi.json").read_text(encoding="utf-8"))
    result = {"population": "one foundation/schema probe; distinct from API inventory",
              "fresh_database": str(connection.settings_dict["NAME"]), "routes": [],
              "serializers": {}, "models": {}, "schemas": [],
              "roles": {role: {"superuser": h.context[role + "_user"].is_superuser,
                               "user_id": h.context[role + "_user"].pk,
                               "employee_id": h.context[role].pk}
                        for role in ("employee", "approver", "outsider")},
              "versions": {n: importlib.metadata.version(n) for n in
                           ("Django", "djangorestframework", "pytest", "pytest-django", "requests", "drf-yasg")}}
    assert not any(row["superuser"] for row in result["roles"].values())
    assert h.balance() == (0.0, 0.0) and h.balance("approver") == (7.0, 0.0) and h.balance("outsider") == (9.0, 0.0)
    for route, item in document["paths"].items():
        for method, operation in item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            cls = resolve(route.replace("{pk}", "999999")).func.view_class
            assert resolve(route.replace("/api/v1/", "/api/", 1).replace("{pk}", "999999")).func.view_class is cls
            result["routes"].append({"operation": operation["operationId"], "method": method.upper(),
                                     "route": route, "view": cls.__name__,
                                     "parsers": [p.media_type for p in cls().get_parsers()],
                                     "filters": filters_for(cls) if method == "get" else {}})
    for route in ("/api/v1/leave/assign-leave/", "/api/v1/leave/assign-leave/999999/",
                  "/api/v1/leave/leave-type/", "/api/v1/leave/employee-leave-type/999999/"):
        cls = resolve(route).func.view_class
        result["routes"].append({"route": route, "view": cls.__name__,
                                 "methods": [m.upper() for m in ("get", "post", "put", "delete") if hasattr(cls, m)],
                                 "filters": filters_for(cls)})
    for name, cls in vars(module).items():
        if inspect.isclass(cls) and cls.__module__ == module.__name__ and issubclass(cls, BaseSerializer):
            try:
                result["serializers"][name] = {key: field_info(value) for key, value in cls().fields.items()}
            except Exception as error:
                result["serializers"][name] = {"introspection_error": type(error).__name__, "detail": str(error)[:250]}
    for model in (LeaveRequest, LeaveAllocationRequest, AvailableLeave, LeaveType):
        result["models"][model.__name__] = {
            field.name: {"class": type(field).__name__, "null": field.null, "blank": field.blank,
                         "max_length": field.max_length,
                         "reference_model": field.remote_field.model._meta.label if getattr(field.remote_field, "model", None) else None}
            for field in model._meta.fields
        }
    assert result["serializers"]["LeaveAllocationRequestCreateSerializer"]["attachment"]["max_length"] == 100
    assert result["serializers"]["LeaveAllocationRequestCreateSerializer"]["attachment"]["allow_empty_file"] is False
    assert result["models"]["LeaveRequest"]["created_by"]["reference_model"] == "employee.Employee"
    assert result["models"]["LeaveAllocationRequest"]["created_by"]["reference_model"] != "employee.Employee"
    for name, route in (("production", "/api/v1/swagger.json/"), ("isolated_leave_fallback", "/__area2_contract_schema__/?format=openapi")):
        response = h.session.get(h.base + route, headers=h.headers["employee"], timeout=180)
        capture = {"kind": name, "route": route, "status": response.status_code,
                   "content_type": response.headers.get("Content-Type"),
                   "response_sha256": hashlib.sha256(response.content).hexdigest()}
        try:
            body = response.json()
        except ValueError:
            body = {}
        if response.status_code == 200 and isinstance(body, dict) and ("swagger" in body or "openapi" in body):
            (folder / (name + "-schema.json")).write_text(json.dumps(body, indent=2), encoding="utf-8")
            capture.update(dialect=body.get("swagger", body.get("openapi")),
                           basePath=body.get("basePath"), paths=len(body.get("paths", {})),
                           normalized=normalized_schema(body))
        else:
            # Debug HTML can include Authorization headers. Never persist it.
            capture["limitation"] = "No successful schema document; status/hash only, no unsafe debug HTML"
        result["schemas"].append(capture)
    # Source-specific missing-reference outcomes, with real JWT and URL routing.
    # These probes are not counted as generated consumers or extra API scenarios.
    from django.contrib.auth.models import Permission
    permission_names = ("view_availableleave", "add_availableleave", "change_availableleave", "delete_availableleave")
    permissions = Permission.objects.filter(content_type__app_label="leave", codename__in=permission_names)
    h.context["approver_user"].user_permissions.add(*permissions)
    result["lookup_probe_permissions"] = list(permissions.values_list("codename", flat=True))
    result["lookup_probes"] = []
    before_probes = h.snapshot()
    for path, item in document["paths"].items():
        if "{pk}" not in path:
            continue
        for method, operation in item.items():
            if method not in ("get", "put", "delete"):
                continue
            role = operation.get("x-role", "employee")
            values = {}
            for label, value in (("positive_missing", "2147483647"), ("unroutable", "not-an-int")):
                response = h.request(method.upper(), path.replace("{pk}", value), role, {} if method != "get" else None)
                values[label] = response.status_code
                if label == "unroutable":
                    assert response.status_code == 404
                else:
                    assert response.status_code in (400, 403, 404), (operation["operationId"], response.status_code)
            result["lookup_probes"].append({"operation": operation["operationId"], "route": path,
                                             "method": method.upper(), "role": role, "statuses": values})
    assert h.snapshot() == before_probes
    allocation_id = h.grant(5)
    leave_id = h.create_leave()
    h.approve_leave(leave_id)
    assert h.balance() == (2.0, 0.0)
    before = h.snapshot()
    refusal = h.request("POST", "/api/v1/leave/user-request/", body=h.shifted_leave(14))
    assert refusal.status_code == 400 and "enough leave" in str(refusal.json()).lower()
    assert h.snapshot() == before
    stored = LeaveRequest.objects.get(pk=leave_id)
    balance = AvailableLeave.objects.get(employee_id=h.context["employee"], leave_type_id=h.context["leave_type"])
    assert stored.employee_id_id == h.context["employee"].pk and stored.status == "approved"
    assert float(stored.requested_days) == 3 and balance.available_days == 2
    assert h.balance("approver") == (7.0, 0.0) and h.balance("outsider") == (9.0, 0.0)
    result["foundation"] = {"verified": True, "allocation_id": allocation_id, "leave_id": leave_id,
                            "sequence": [0, 5, 2], "rejection_status": 400, "rejection_unchanged": True,
                            "ORM_owner_amount_balance": True}
    (folder / "runtime-contract.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("FOUNDATION_CONTRACT_RESULT " + json.dumps(result, sort_keys=True))
