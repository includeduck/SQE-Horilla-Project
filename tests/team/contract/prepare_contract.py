"""Build a reconciled candidate in a disposable CI checkout, retaining old IDs."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEAM = ROOT / "tests/team"


def emit(path, content):
    # Plain JSON chunks avoid log masking of Swagger documentation descriptions.
    # These files contain synthetic contract metadata/data, never auth tokens.
    size = 10000
    for i in range(0, len(content), size):
        print("CONTRACT_FILE_CHUNK " + json.dumps({"path": path, "index": i // size,
              "total": (len(content) + size - 1) // size, "text": content[i:i + size]}), flush=True)


def build(output):
    output.mkdir(parents=True, exist_ok=False)
    source = (TEAM / "generator/generate.py").read_text(encoding="utf-8")
    old = '''                if len(content) != 1:
                    raise ContractError("Scoped operation must select exactly one request media type")
                media_type, media = next(iter(content.items()))'''
    new = '''                preferred = operation.get("x-generator-media-type")
                if preferred is None:
                    if len(content) != 1:
                        raise ContractError("Multiple media require an explicit x-generator-media-type")
                    media_type, media = next(iter(content.items()))
                else:
                    if preferred not in content:
                        raise ContractError("Preferred generator media absent from declared content")
                    if set(content) - {"application/json", "application/x-www-form-urlencoded", "multipart/form-data"}:
                        raise ContractError("Unsupported declared alternative media")
                    if any(candidate.get("schema") != content[preferred].get("schema")
                           or set(candidate) - {"schema", "example", "examples"}
                           for candidate in content.values()):
                        raise ContractError("Alternative media need identical schemas; encodings/distinct schemas require a reader")
                    media_type, media = preferred, content[preferred]'''
    if old in source:
        source = source.replace(old, new)
    elif new not in source:
        raise ValueError("Generator media-selection source changed; inspect rather than patch blindly")
    doc = json.loads((TEAM / "generator/openapi.json").read_text(encoding="utf-8"))
    before = json.loads((TEAM / "generator/generated_cases.json").read_text(encoding="utf-8"))
    bindings = json.loads((TEAM / "generator/bindings.json").read_text(encoding="utf-8"))
    bindings.setdefault("available_leave_id", 501)
    schemas = doc["components"]["schemas"]
    for name in ("AllocationUpdate", "SelfAllocationUpdate"):
        schemas[name]["properties"]["is_active"] = {
            "type": "boolean", "example": True,
            "x-source": "Runtime LeaveAllocationRequestSerilaizer.is_active: writable BooleanField, optional, non-null",
        }
    def reference(binding):
        return {"type": "integer", "x-binding": binding,
                "x-reference": {"missing-binding": "missing_id"},
                "x-source": "Runtime related field / int:pk route; existence and ownership bound separately"}
    schemas["AssignmentCreate"] = {
        "type": "object", "required": ["employee_ids", "leave_type_ids"],
        "properties": {
            "employee_ids": {"type": "array", "minItems": 1, "items": reference("employee_id"),
                             "x-source": "AssignLeaveCreateSerializer.validate_employee_ids rejects empty, despite child allow_empty=True"},
            "leave_type_ids": {"type": "array", "minItems": 1, "items": reference("leave_type_id"),
                              "x-source": "AssignLeaveCreateSerializer.validate_leave_type_ids rejects empty"},
        },
    }
    schemas["AssignmentUpdate"] = {
        "type": "object", "required": ["available_days"], "properties": {
            "available_days": {"type": "number", "example": 5, "x-source": "Runtime AvailableLeaveUpdateSerializer: required, non-null, no declared numeric bounds"},
            "carryforward_days": {"type": "number", "example": 0, "x-source": "Runtime AvailableLeaveUpdateSerializer: optional, non-null, no declared numeric bounds"},
        },
    }
    schemas["OptionalReason"] = {
        "type": "object", "properties": {"reason": {
            "type": "string", "nullable": True, "example": "Synthetic rejection",
            "x-source": "reject_reason_from: optional text, strip, truncate to 1000, ignore nonstrings; persistence separately constrained",
            "x-wire-coercion": "Non-string/null/missing/blank is ignored, not schema-rejected. This schema is the text interpretation; Prompt 3 binds actual wire outcomes.",
        }},
    }
    page = copy.deepcopy(doc["paths"]["/api/v1/leave/available-leave/"]["get"]["parameters"])
    def operation(name, method, requirements, role="approver", schema=None, success=200):
        row = {"operationId": name, "x-role": role, "x-requirements": requirements,
               "x-source": "horilla_api/api_urls/leave/urls.py; runtime resolver and serializers; finish-01 probe",
               "security": [{"BearerAuth": []}],
               "responses": {str(success): {"description": "Source/runtime field reconciliation; operation consumer planned"},
                             "400": {"description": "Validation/business rejection"},
                             "401": {"description": "Authentication required"},
                             "403": {"description": "Permission denied"}}}
        if method == "get":
            row["parameters"] = copy.deepcopy(page)
        if schema:
            row["requestBody"] = {"required": True, "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/" + schema}}}}
        return row
    def path_parameter(binding):
        return [{"name": "pk", "in": "path", "required": True, "schema": reference(binding)}]
    doc["paths"]["/api/v1/leave/assign-leave/"] = {
        "get": operation("assignment_list", "get", ["FR-01", "FR-10", "BR-04"]),
        "post": operation("assignment_create", "post", ["FR-01", "FR-10", "BR-04"], schema="AssignmentCreate", success=201),
    }
    doc["paths"]["/api/v1/leave/assign-leave/{pk}/"] = {
        "parameters": path_parameter("available_leave_id"),
        "get": operation("assignment_detail", "get", ["FR-10", "BR-04"]),
        "put": operation("assignment_update", "put", ["FR-10", "BR-04"], schema="AssignmentUpdate", success=201),
        "delete": operation("assignment_delete", "delete", ["FR-10", "BR-04"]),
    }
    doc["paths"]["/api/v1/leave/leave-type/"] = {
        "get": operation("leave_type_list", "get", ["FR-01", "FR-05"], role="employee")}
    doc["paths"]["/api/v1/leave/employee-leave-type/{pk}/"] = {
        "parameters": path_parameter("employee_id"),
        "get": operation("employee_leave_type_list", "get", ["FR-01", "FR-05", "BR-04"], role="employee")}
    for item in doc["paths"].values():
        for method, op in item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            if op["operationId"] in ("reject", "allocation_reject", "cancellation_reject"):
                op["requestBody"] = {"required": False, "content": {
                    "application/json": {"schema": {"$ref": "#/components/schemas/OptionalReason"}}}}
            if "requestBody" in op:
                content = op["requestBody"]["content"]
                chosen = op.get("x-generator-media-type", next(iter(content)))
                selected = copy.deepcopy(content[chosen])
                op["requestBody"]["content"] = {media: copy.deepcopy(selected) for media in
                    ("application/json", "application/x-www-form-urlencoded", "multipart/form-data")}
                op["x-generator-media-type"] = chosen
                op["x-media-consumption-status"] = "Generator selects one documented baseline media; alternative-media consumers remain mandatory in the inventory"
    doc["x-input-inventory"] = "docs/team/finish-line/OPERATION_INPUT_INVENTORY.json"
    doc["x-exclusions"] = [
        "Required runtime filter/search/grouping/page inputs are completely inventoried but not all represented/consumed by this reader; Prompt 2 must implement them.",
        "New assignment/reference/reason/is_active classes and remaining old generated IDs need actual consumers or justified evidence-backed N/A; ID reference alone is not a pass.",
        "All accepted media, whole-body omission/null/unknown properties, numeric/reference coercions and collection wire encodings are not exhaustively consumed.",
        "Effective positive duration, employee-specific holidays, forecast, complete decision/state/reference/balance scenarios remain Prompt 3 work.",
        "Reason text schema is not its wire normalization oracle; ignored/truncated values and persistence limits require Prompt 3 verification.",
    ]
    spec = importlib.util.spec_from_loader("reconciled_generator", loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(compile(source, "reconciled_generate.py", "exec"), module.__dict__)
    artifact = module.generate(doc, bindings)
    # Existing parametrized consumers automatically collect newly declared self-update fields.
    spec2 = importlib.util.spec_from_file_location("case_catalog", TEAM / "api/case_catalog.py")
    catalog = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(catalog)
    ledger = json.loads((TEAM / "api/case_ledger.json").read_text(encoding="utf-8"))
    entries = ledger["entries"]
    present = {e["case_id"] for e in entries}
    for case in catalog.selected_generated_cases(artifact):
        if case["id"] not in present:
            entries.append({"case_id": case["id"], "file": "test_generated_inputs.py",
                            "generated": True, "execution_status": "pending-current-build"})
            present.add(case["id"])
    all_ids = {c["id"] for c in artifact["cases"]}
    refs = {e["case_id"] for e in entries if e["generated"]}
    assert refs <= all_ids
    ledger.update(spec_sha256=artifact["spec_sha256"], data_sha256=artifact["data_sha256"],
                  implemented_api_cases=len(entries), referenced_generated_case_ids=len(refs),
                  generated_data_cases=len(all_ids), unconsumed_generated_case_ids=sorted(all_ids - refs),
                  note="Reconciled input declaration; new-build execution is pending. Referenced IDs are not a complete input/FR acceptance.")
    old_ids = {c["id"] for c in before["cases"]}
    lineage = {"old_spec_sha256": before["spec_sha256"], "new_spec_sha256": artifact["spec_sha256"],
               "old_data_sha256": before["data_sha256"], "new_data_sha256": artifact["data_sha256"],
               "old_operations": len(before["operations"]), "new_operations": len(artifact["operations"]),
               "old_cases": len(old_ids), "new_cases": len(all_ids),
               "preserved_ids": sorted(old_ids & all_ids), "added_ids": sorted(all_ids - old_ids),
               "retired_ids": sorted(old_ids - all_ids),
               "baseline_changes": "New is_active input in allocation update baselines; media alternatives declared with explicit generator selection; fresh fixture bindings are required.",
               "applicable_consumption_complete": False}
    files = {
        "tests/team/generator/generate.py": source,
        "tests/team/generator/openapi.json": json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
        "tests/team/generator/bindings.json": json.dumps(bindings, indent=2) + "\n",
        "tests/team/generator/generated_cases.json": json.dumps(artifact, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        "tests/team/api/case_ledger.json": json.dumps(ledger, indent=2) + "\n",
        "tests/team/generator/test_generate.py": (TEAM / "generator/test_generate.py").read_text(encoding="utf-8").replace(
            'self.assertEqual(len(first["operations"]), 27)', 'self.assertEqual(len(first["operations"]), 34)'),
        "docs/team/finish-line/CONTRACT_LINEAGE.json": json.dumps(lineage, indent=2) + "\n",
    }
    for path, content in files.items():
        (output / Path(path).name).write_text(content, encoding="utf-8")
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        emit(path, content)
    print("CONTRACT_MIGRATION_SUMMARY " + json.dumps({k: v for k, v in lineage.items()
          if k not in ("preserved_ids", "added_ids", "retired_ids")}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    # This preparation modifies ONLY an explicitly disposable CI checkout.
    import os
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise SystemExit("Run only in a disposable GitHub Actions checkout; published candidates are reviewed before use.")
    build(Path(args.output))
