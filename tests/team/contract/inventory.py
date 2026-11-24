"""Reproducible complete scope/input and generated-ID audit; never a pass counter."""
import argparse
import ast
import importlib.util
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEAM = ROOT / "tests/team"
FINISH = ROOT / "docs/team/finish-line"
RUNTIME = ROOT / "docs/team/evidence/area2/finish-01/runtime-contract-current.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def source_routes():
    urls = ast.parse((ROOT / "horilla_api/api_urls/leave/urls.py").read_text(encoding="utf-8"))
    views = ast.parse((ROOT / "horilla_api/api_views/leave/views.py").read_text(encoding="utf-8"))
    classes = {c.name: c for c in views.body if isinstance(c, ast.ClassDef)}
    def methods(name):
        if name not in classes:
            return {}
        result = {}
        for parent in classes[name].bases:
            if isinstance(parent, ast.Name):
                result.update(methods(parent.id))
        result.update({f.name: f for f in classes[name].body if isinstance(f, ast.FunctionDef)
                       and f.name in ("get", "post", "put", "delete", "patch")})
        return result
    rows = {}
    for node in ast.walk(urls):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "path":
            route = "/api/v1/leave/" + node.args[0].value.replace("<int:pk>", "{pk}")
            view = node.args[1].func.value.id
            for method, fn in methods(view).items():
                rows[(route, method.upper())] = {
                    "view": view, "source_line": fn.lineno,
                    "decorators": [ast.unparse(d) for d in fn.decorator_list],
                    "explicit_query_reads": sorted({call.args[0].value
                        for call in ast.walk(fn) if isinstance(call, ast.Call)
                        and isinstance(call.func, ast.Attribute) and call.func.attr in ("get", "getlist")
                        and "request.GET" in ast.unparse(call.func) and call.args
                        and isinstance(call.args[0], ast.Constant)}),
                }
    return rows


def context(operation, role):
    allocation = "allocation" in operation
    assignment = operation.startswith("assignment_")
    detail = any(t in operation for t in ("update", "delete", "detail"))
    action = operation in ("approve", "reject", "cancel", "cancellation_approve",
                           "cancellation_reject", "allocation_approve", "allocation_reject")
    return {
        "role": "normal employee" if role == "employee" else "normal approver with exact operation permission",
        "binding_role": role,
        "record_binding": "AvailableLeave.id" if assignment and detail else "Employee.id" if operation == "employee_leave_type_list" else "LeaveAllocationRequest.id" if allocation and (detail or action) else "LeaveRequest.id" if detail or action else "create/list route",
        "state": "assigned record (no leave workflow status)" if assignment else "cancel_requested" if operation.startswith("cancellation_") else "approved" if operation == "cancel" else "requested for editable/approval/decision targets",
        "preparation": "Use existing real HTTP W1/W2 helpers; bind independent normal users and real IDs. Assignment admin cases grant exact availableleave permissions to a synthetic non-superuser. For employee_leave_type_list bind Employee, not leave/assignment ID.",
        "baseline": "Assigned type; non-overlapping future dates 2030-01-07..09; matching full-day breakdowns; required proof if enabled; effective balance >= requested days; no unintended duplicate pending record. Keep other query filters omitted.",
    }


def wire_plan(case):
    field = case["field"][-1]
    location = case["location"]
    if location == "path":
        return {"status_rule": "Non-integer/negative/null/missing-segment routing representations -> 404 before the view. Positive missing reference -> endpoint-specific guard/lookup 400 or 404; probe before fixing the test oracle.",
                "binding": "Replace only the path token; omitted token retains the empty segment, never collapse it onto a collection route. Valid IDs must reference the operation's correct owned/stateful model.",
                "schema_predicate_is_http_oracle": False}
    if location == "query":
        return {"status_rule": "page_size: positive integer parsed/clamped to 100, otherwise configured default 20. Query null is omitted by Requests. Other input/filter outcomes use the runtime Filter field.",
                "binding": "One active query dimension with unrelated optional filters omitted; populate enough rows to distinguish fallback/clamp and verify unchanged IDs/balances.",
                "schema_predicate_is_http_oracle": False}
    if field == "reason":
        return {"status_rule": "Optional helper ignores missing/null/nonstring/blank, strips text and truncates 1000; actual action succeeds only in its allowed role/state. Persisted model length conflict needs Prompt 3 assertion.",
                "binding": "Use an independent requested/approved/cancel_requested target appropriate to each reject endpoint; compare actual stored reason and balance.",
                "schema_predicate_is_http_oracle": False}
    return {"status_rule": "Field schema predicate plus actual DRF coercion; case rejection generally 400, allowed field value succeeds only with the independently valid bound business baseline. Falsy end_date normalizes to start; JSON file-null differs from multipart omission.",
            "binding": "Preserve generated baseline/current field and record any fixture-ID/media normalization. Binary descriptors become real multipart bytes, not mocked uploads.",
            "schema_predicate_is_http_oracle": False}


def filter_classes(meta):
    """Wire partitions derive from the actual Django form field, never an invented domain bound."""
    common = ["omitted", "empty", "matching", "nonmatching", "malformed"]
    kind = meta.get("form_field", "")
    if kind in ("DecimalField", "FloatField", "IntegerField"):
        common += ["negative", "zero", "fractional", "nonfinite", "exponent", "lookup_threshold_below_at_above"]
        common += ["validator_boundary:" + v["class"] + ":" + v["limit_value"]
                   for v in meta.get("validators", []) if v.get("limit_value")]
    elif kind in ("DateField", "DateTimeField"):
        common += ["valid_calendar", "invalid_calendar", "leap_day", "lookup_date_before_at_after"]
    elif "MultipleChoice" in kind:
        common += ["real_reference", "missing_reference", "wrong_relation_reference", "repeated_keys", "mixed_valid_invalid"]
    elif kind == "ChoiceField":
        common += ["choice:" + v for v in meta.get("static_choices", [])] + ["invalid_choice"]
    elif kind in ("NullBooleanField", "BooleanField"):
        common += ["true", "false", "null", "unknown_boolean", "wire_coercions"]
    else:
        common += ["whitespace", "unicode", "case", "partial_match", "lookup_exactness"]
    return common


def build():
    artifact = read(TEAM / "generator/generated_cases.json")
    ledger = read(TEAM / "api/case_ledger.json")
    doc = read(TEAM / "generator/openapi.json")
    runtime = read(RUNTIME)
    lineage_path = FINISH / "CONTRACT_LINEAGE.json"
    lineage = read(lineage_path) if lineage_path.exists() else {}
    cases = artifact["cases"]
    refs = {r["case_id"]: r for r in ledger["entries"] if r["generated"]}
    old_refs = set(lineage.get("old_referenced_ids", refs))
    old_unconsumed = set(lineage.get("preserved_ids", [c["id"] for c in cases])) - old_refs
    scope = {}
    routes = source_routes()
    runtime_routes = {}
    for row in runtime["routes"]:
        route = row["route"].replace("999999", "{pk}")
        for method in row.get("methods", [row.get("method")]):
            runtime_routes[(route, method)] = row
    for route, item in doc["paths"].items():
        for method, operation in item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            key = (route, method.upper())
            assert key in routes, key
            rt = runtime_routes.get(key, {})
            scope[operation["operationId"]] = {
                "operation": operation["operationId"], "route": route, "method": method.upper(),
                "requirements": operation.get("x-requirements", []),
                "source": routes[key], "runtime_view": rt.get("view"),
                "parsers": rt.get("parsers", ["application/json", "application/x-www-form-urlencoded", "multipart/form-data"]),
                "success_status": next((int(s) for s in operation["responses"] if s.startswith("2")), None),
                "context": context(operation["operationId"], operation["x-role"]), "input_ids": [],
                "renderers": rt.get("renderers", []),
            }
    audit = []
    families = {}
    def add(op, location, field, category, details, stage=2):
        key = "INPUT:" + op + ":" + location + ":" + field
        if key in families:
            return families[key]
        row = {"id": key, "operation": op, "location": location, "field": field,
               "category": category, "requirements": scope[op]["requirements"],
               "details": details, "generated_ids": [], "referenced_ids": [],
               "status": "planned", "mandatory": True, "stage": stage,
               "phase": "C" if stage == 3 else "B-C",
               "evidence": ["docs/team/finish-line/CONTRACT_RECONCILIATION.md", str(RUNTIME.relative_to(ROOT))],
               "dependencies": ["Independent valid role/state/model fixture", "Prompt " + str(stage) + " actual execution"],
               "original_owner": "Rayyan / Area 2", "current_executor": "Codex for Rayyan",
               "acceptance": "All applicable classes bound and executed with exact response plus persisted postconditions; N/A needs specific evidence, not unsupported-reader status."}
        families[key] = row
        scope[op]["input_ids"].append(key)
        return row
    for index, case in enumerate(cases):
        op, location = case["operation"], case["location"]
        field = ".".join(str(v) for v in case["field"])
        family = add(op, location, field, "declared_generated_input",
                     {"source": case["provenance"]["source"], "schema": case["provenance"]["schema"]},
                     3 if case["field"] == ["reason"] or case["expected"]["oracle"] == "date-order" else 2)
        family["generated_ids"].append(case["id"])
        if case["id"] in refs:
            family["referenced_ids"].append(case["id"])
        audit.append({"id": case["id"], "operation": op, "method": case["method"], "route": case["route"],
                      "location": location, "field": case["field"], "technique": case["technique"],
                      "schema_class": case["class"], "schema_expectation": case["expected"],
                      "source": case["provenance"]["source"], "requirements": case["requirements"],
                      "generated_request_reference": {"file": "tests/team/generator/generated_cases.json", "pointer": "/cases/" + str(index)},
                      "context": scope[op]["context"], "expected_wire_behavior": wire_plan(case),
                      "live_lookup_observation": next((p for p in runtime.get("lookup_probes", []) if p["operation"] == op), None) if location == "path" else None,
                      "lookup_caveat": "403 on ungranted generic delete permission precedes object lookup; do not call it a fully authorized missing-ID oracle." if op in ("leave_delete", "allocation_delete") else None,
                      "consumer": refs.get(case["id"]), "planned_consumer": "existing parameterized module if referenced; otherwise tests/team/api contract consumer in Prompt " + str(family["stage"]),
                      "applicability": "mandatory_applicable_requires_context_binding",
                      "execution_status": "pending_reconciled_contract", "baseline_evidence": {"run_id": 45388276552, "previously_referenced": case["id"] in old_refs,
                          "meaning": "Previous all-pass collection only, not execution of this reconciled request/hash"},
                      "old_399_member": case["id"] in old_unconsumed, "disposition_stage": family["stage"]})
    for op, operation in scope.items():
        route, method = operation["route"], operation["method"]
        rt = runtime_routes.get((route, method), {})
        for field, meta in rt.get("filters", {}).items() if method == "GET" else ():
            add(op, "query", field, "runtime_filter", {"filter": meta, "classes": filter_classes(meta),
                "binding": "Use actual Filter.field semantics and fixture relations; invalid filters may be ignored by .qs rather than become HTTP 400. Do not assume schema validity equals filter semantics."})
        if method == "GET" and ("list" in op or op == "own_balance"):
            active = add(op, "query", "is_active", "manager_query", {"source": "base/horilla_company_manager.py:HorillaCompanyManager.all", "classes": ["omitted", "true", "false", "False", "all", "invalid"], "expected": "Manager .all defaults active-only; false/False selects inactive. Existing django-filter is_active can further interact. Employee-specific type list applies this to AvailableLeave before LeaveType filtering. Assert real persisted identities, not just list length."})
            active["details"]["manager_selector"] = "HorillaCompanyManager.all active/inactive selection precedes serializer/filter rendering"
            add(op, "query", "page", "pagination", {"classes": ["omitted", "1", "last", "beyond_last", "zero", "negative", "malformed"],
                "expected": "DRF page-number parse / NotFound behavior; actual list population and links"})
        for field in operation["source"]["explicit_query_reads"]:
            add(op, "query", field, "view_query", {"classes": ["omitted", "valid_model_field", "invalid_field", "nested_field"],
                "expected": "groupby branch uses stock PageNumberPagination, unlike ungrouped page_size clamp; malformed grouping must be reproduced, never silently accepted as safe"})
        add(op, "header", "Authorization", "authentication_roles", {"classes": ["absent", "invalid", "normal_owner", "foreign_owner", "exact_permission", "reporting_manager"],
            "expected": "Missing/invalid JWT 401; permission refusals controlled 403; role/state methods and object guards separately bound"})
        add(op, "header", "Accept", "response_negotiation", {"classes": ["JSON", "unsupported_media"], "expected": "Supported renderer versus 406; inspect real renderers/HTTP"})
        if method in ("POST", "PUT", "PATCH"):
            add(op, "header", "Content-Type", "request_media", {"classes": operation["parsers"] + ["unsupported", "missing_header", "malformed_payload"],
                "expected": "Actual parser selection; 400 parse errors/415 unsupported only if handler consumes request.data. No assumption for data-ignoring actions."})
            add(op, "body", "$whole", "whole_body", {"classes": ["omitted", "empty_object", "null", "array", "scalar", "malformed_JSON", "unknown_property"],
                "expected": "Exact view/serializer/body-requiredness behavior; data-ignoring actions differ from creates"})
        if "allocation" in op or "leave" in op:
            if method in ("POST", "PUT"):
                add(op, "body", "$server_managed_fields", "injection_integrity", {"fields": ["id", "created_by", "modified_by", "employee_id"],
                    "expected": "Respect read-only/injected fields and preserve own record identity; generic employee input is separately writable where source allows"})
        if op in ("leave_create", "leave_update", "self_leave_create", "self_leave_update"):
            for field, details in {
                "$effective_duration": "Positive effective day count; 0, below/at/above available+capped carry+source-backed forecast",
                "$holidays": "Target-employee versus other employee holidays; company/holiday overlap without double subtraction",
                "$breakdown_overlap_attachment": "Complete feasible BR-02 combinations and invalid non-overlapping baselines",
            }.items():
                add(op, "relational", field, "business_rule", {"expected": details}, stage=3)
        if op in ("assignment_create",):
            add(op, "body", "$collection_encoding", "multipart_array", {"classes": ["JSON_arrays", "repeated_form_keys", "invalid_item", "mixed_valid_missing", "duplicate_ids", "cartesian_no_duplicate_assignment"],
                "expected": "Use ManyRelatedField/getlist and source validate_* nonempty; repeated assignment is source idempotent for an existing employee/type"})
    source_inventory = []
    selected = {(v["route"], v["method"]) for v in scope.values()}
    for (route, method), source in sorted(routes.items()):
        included = (route, method) in selected
        source_inventory.append({"route": route, "method": method, **source, "selected": included,
            "scope_reason": "W1/W2 core, assignment setup administration or type reference read" if included else
            "Not selected: leave-type/holiday/company configuration writes, bulk workflow variants, status dashboard or permission-check UI helpers; fixture prerequisites are recorded separately. Revisit only if accepted workflow scope changes."})
    expected_filters = {(row["route"].replace("999999", "{pk}"), name)
                        for row in runtime["routes"]
                        if row.get("method") == "GET" or "GET" in row.get("methods", [])
                        for name in row.get("filters", {})}
    actual_filters = {(scope[row["operation"]]["route"], row["field"])
                      for row in families.values() if row["category"] == "runtime_filter"}
    if actual_filters != expected_filters:
        raise ValueError("Runtime GET filters lost across shared method routes")
    # Live Swagger is observation, not authority over custom hand-rolled views.
    live = {}
    for schema in runtime["schemas"]:
        if schema["kind"] != "production" or schema["status"] != 200:
            continue
        for row in schema.get("normalized", {}).get("operations", []):
            route = row["route"].replace("{id}", "{pk}")
            live.setdefault((route, row["method"]), row)
    differences = []
    for op, operation in scope.items():
        observed = live.get((operation["route"], operation["method"]))
        differences.append({"operation": op, "in_production_swagger": observed is not None,
            "path_parameter_schema": [p for p in (observed or {}).get("parameters", []) if p.get("in") == "path"],
            "live_declared_statuses": list((observed or {}).get("responses", {})),
            "actual_success_status_source": operation["success_status"],
            "live_has_body_or_form": any(p.get("in") in ("body", "formData") for p in (observed or {}).get("parameters", [])),
            "resolution": "Normalize Swagger {id} to resolver {pk}; actual int converter, serializers and source response are authoritative over generic Swagger defaults. Alternative media and mandatory undeclared inputs remain planned, not verified."})
    spec = importlib.util.spec_from_file_location("inventory_case_catalog", TEAM / "api/case_catalog.py")
    catalog = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(catalog)
    required_rows = list(families.values())
    for row in required_rows:
        row["remaining_generated_ids"] = sorted(set(row["generated_ids"]) - set(row["referenced_ids"]))
    summary = {"canonical_operations": len(scope), "canonical_generated_inputs": len(artifact["inventory"]),
               "generated_cases": len(cases), "referenced_generated_ids": len(refs),
               "unconsumed_generated_ids": len(cases) - len(refs),
               "old_399_accounted": sum(r["old_399_member"] for r in audit),
               "retired_old_ids": len(lineage.get("retired_ids", [])),
               "required_input_families": len(required_rows),
               "required_families_without_generated_ids": sum(not row["generated_ids"] for row in required_rows),
               "input_families_by_stage": dict(Counter(row["stage"] for row in required_rows)),
               "new_contract_executed_all": False, "coverage_complete": False}
    outputs = {
        "GENERATED_CASE_AUDIT.json": {"summary": summary, "spec_sha256": artifact["spec_sha256"],
                                    "data_sha256": artifact["data_sha256"], "entries": audit,
                                    "note": "Every current generated ID accounted; no deferred/unsupported ID falsely classified N/A. Previous results and current hashes are separate."},
        "OPERATION_INPUT_INVENTORY.json": {"summary": summary, "operations": list(scope.values()),
                                         "inputs": required_rows, "all_leave_source_routes": source_inventory,
                                         "swagger_comparison": differences,
                                         "decision_plan": catalog.decision_rows(), "authorization_plan": catalog.authorization_rows(),
                                         "state_plan": catalog.state_rows(),
                                         "BVA_applicability": artifact["inventory"]},
        "REMAINING_WORK.json": {"summary": summary, "prepared_stage": 1,
                               "items": required_rows,
                               "mandatory_external_items": [
                                   {"id": "SHARED-CI-OWNER", "phase": "D", "original_owner": "Wasay", "current_executor": "Wasay / agent",
                                    "status": "blocked", "reason": "Overall Sonar/mutation/required merge/deploy administration is owner scope; available scoped producers already supplied.",
                                    "acceptance": "Actual required-check policy and genuine blocked/fixed PR enforcement evidence"},
                                   {"id": "SHARED-GROUP-PACKAGE", "phase": "D", "original_owner": "Shared", "current_executor": "Codex where genuine inputs exist, otherwise Wasay coordinates Zain",
                                    "status": "planned", "reason": "Final group PDF/ZIP/history depends on actual Area 1/3 evidence; verify at Prompt 4, do not fabricate.",
                                    "acceptance": "Verified all-area package and synchronized permitted .git"},
                                   {"id": "ACCESS-LOCAL-WORKSPACE", "phase": "A-D", "original_owner": "Shared environment", "current_executor": "Wasay if still unavailable at final closure",
                                    "status": "blocked", "reason": "Execution environment declared unavailable mid-Prompt 1. Connected GitHub CI/publication works; this does NOT block independent Area 2 execution.",
                                    "acceptance": "Permitted synchronized checkout preserving existing files; no reset/bypass"}],
                               "closure_policy": "Prompts 2-4 finish feasible technical work. Only genuine residual execution is mandatory Wasay work after Prompt 4; no fifth Rayyan prompt.",
                               "historical_archive": "Unavailable original A archive is not reconstructed; fresh runtime evidence establishes a new foundation, not fabricated history."},
    }
    validate(outputs, cases, old_unconsumed)
    return outputs


def validate(outputs, cases, old_unconsumed):
    ids = [r["id"] for r in outputs["GENERATED_CASE_AUDIT.json"]["entries"]]
    if len(ids) != len(set(ids)) or set(ids) != {c["id"] for c in cases}:
        raise ValueError("Generated audit lost/duplicated a case")
    actual = {r["id"] for r in outputs["GENERATED_CASE_AUDIT.json"]["entries"] if r["old_399_member"]}
    if actual != old_unconsumed:
        raise ValueError("Original unconsumed population lost or relabelled")
    inputs = outputs["OPERATION_INPUT_INVENTORY.json"]["inputs"]
    if len({r["id"] for r in inputs}) != len(inputs):
        raise ValueError("Duplicate required input identity")
    if any(r["status"] == "justified_not_applicable" and not r.get("evidence") for r in inputs):
        raise ValueError("Unsupported N/A assertion")
    if not all(r.get("evidence") and r.get("dependencies") and r.get("phase") for r in inputs):
        raise ValueError("Input lacks traceability/dependency/phase")
    if any(not r["acceptance"] or not r["current_executor"] for r in inputs):
        raise ValueError("Unassigned or untestable obligation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    outputs = build()
    for name, payload in outputs.items():
        text = json.dumps(payload, indent=2, ensure_ascii=True) + "\n"
        (output / name).write_text(text, encoding="utf-8")
        if args.emit:
            for i in range(0, len(text), 10000):
                print("INVENTORY_FILE_CHUNK " + json.dumps({"path": "docs/team/finish-line/" + name,
                    "index": i // 10000, "total": (len(text) + 9999) // 10000, "text": text[i:i + 10000]}), flush=True)
    print("INVENTORY_SUMMARY " + json.dumps(outputs["REMAINING_WORK.json"]["summary"]), flush=True)
