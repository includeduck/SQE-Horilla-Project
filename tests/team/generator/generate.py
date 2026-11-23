"""Rayyan Hassan (24I-3000): scoped OpenAPI 3.0 EP/BVA generation.

No application imports or third-party dependencies. JSON is used for OpenAPI
and output, so generator checks remain runnable without Django installed.
"""

import argparse
import copy
import hashlib
import json
import math
import re
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path


class ContractError(ValueError):
    """An unsupported or inconsistent input contract must fail visibly."""


def fingerprint(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def resolve(document, value, seen=()):
    if not isinstance(value, dict) or "$ref" not in value:
        return copy.deepcopy(value)
    ref = value["$ref"]
    if not ref.startswith("#/") or ref in seen or len(value) != 1:
        raise ContractError(f"Unsupported external/cyclic/ref-sibling reference: {ref}")
    target = document
    try:
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
    except (KeyError, TypeError) as error:
        raise ContractError(f"Unresolved reference: {ref}") from error
    return resolve(document, target, (*seen, ref))


SCHEMA_KEYS = {
    "type", "format", "title", "description", "default", "example", "nullable",
    "enum", "properties", "required", "items", "minimum", "maximum",
    "exclusiveMinimum", "exclusiveMaximum", "minLength", "maxLength",
    "minItems", "maxItems", "readOnly", "writeOnly", "additionalProperties",
    "x-binding", "x-source", "x-reference", "x-step", "x-date-minimum",
    "x-date-maximum", "x-filename-maxLength", "x-allow-empty-file",
    "x-wire-coercion",
    "x-trim-whitespace",
}


def check_schema(document, schema, seen=()):
    if isinstance(schema, dict) and "$ref" in schema:
        ref = schema["$ref"]
        if ref in seen:
            raise ContractError(f"Recursive input schemas are unsupported: {ref}")
        seen = (*seen, ref)
    schema = resolve(document, schema)
    unknown = set(schema) - SCHEMA_KEYS
    if unknown:
        raise ContractError(f"Unsupported relevant schema constraints: {sorted(unknown)}")
    kind = schema.get("type")
    if kind not in {"object", "array", "string", "integer", "number", "boolean"}:
        raise ContractError(f"Unsupported or absent schema type: {kind}")
    if schema.get("format") not in {None, "date", "binary", "float", "double", "int32", "int64"}:
        raise ContractError(f"Unsupported format: {schema['format']}")
    if schema.get("format") in {"date", "binary"} and kind != "string":
        raise ContractError("Date/binary format requires string type")
    if schema.get("additionalProperties") not in (None, True, False):
        raise ContractError("Typed additionalProperties is unsupported")
    if schema.get("readOnly"):
        raise ContractError("Read-only properties must not be listed as input fields")
    if kind == "object":
        properties = schema.get("properties", {})
        if set(schema.get("required", [])) - set(properties):
            raise ContractError("Required property missing from properties")
        for child in properties.values():
            check_schema(document, child, seen)
    if kind == "array":
        check_schema(document, schema.get("items", {}), seen)
    for low, high in (("minimum", "maximum"), ("minLength", "maxLength"),
                      ("minItems", "maxItems"), ("x-date-minimum", "x-date-maximum")):
        if low in schema and high in schema and schema[low] > schema[high]:
            raise ContractError(f"Inconsistent bounds: {low}, {high}")
    if any(key in schema for key in ("minimum", "maximum")) and kind == "number":
        if "x-step" not in schema:
            raise ContractError("Bounded number requires a justified x-step")
    if schema.get("x-step", 1) <= 0:
        raise ContractError("x-step must be positive")
    return schema


def accepts(document, raw_schema, value):
    """Schema predicate only; database/business outcomes are separate."""
    schema = check_schema(document, raw_schema)
    if value is None:
        return schema.get("nullable", False)
    kind = schema["type"]
    if schema.get("format") == "binary":
        return (
            isinstance(value, dict) and set(value) == {"filename", "text", "content_type"}
            and isinstance(value["filename"], str) and bool(value["filename"])
            and len(value["filename"]) <= schema.get("x-filename-maxLength", math.inf)
            and isinstance(value["text"], str)
            and (bool(value["text"]) or schema.get("x-allow-empty-file", False))
        )
    if kind == "boolean":
        valid_type = isinstance(value, bool)
    elif kind == "integer":
        valid_type = isinstance(value, int) and not isinstance(value, bool)
    elif kind == "number":
        valid_type = isinstance(value, (int, float)) and not isinstance(value, bool)
        valid_type = valid_type and math.isfinite(value)
    else:
        valid_type = isinstance(value, {"object": dict, "array": list, "string": str}[kind])
    if not valid_type or ("enum" in schema and value not in schema["enum"]):
        return False
    if kind == "object":
        properties = schema.get("properties", {})
        return (
            all(key in value for key in schema.get("required", []))
            and (schema.get("additionalProperties", True) or not set(value) - set(properties))
            and all(accepts(document, properties[key], child)
                    for key, child in value.items() if key in properties)
        )
    if kind == "array":
        return (schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", math.inf)
                and all(accepts(document, schema["items"], item) for item in value))
    if kind in {"number", "integer"}:
        for key, exclusive, compare in (
            ("minimum", "exclusiveMinimum", lambda a, b: a > b),
            ("maximum", "exclusiveMaximum", lambda a, b: a < b),
        ):
            if key in schema:
                boundary = schema[key]
                if schema.get(exclusive):
                    if not compare(value, boundary):
                        return False
                elif key == "minimum" and value < boundary:
                    return False
                elif key == "maximum" and value > boundary:
                    return False
    if kind == "string":
        length = len(value.strip() if schema.get("x-trim-whitespace") else value)
        if not schema.get("minLength", 0) <= length <= schema.get("maxLength", math.inf):
            return False
        if schema.get("format") == "date":
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    return False
                date.fromisoformat(value)
            except ValueError:
                return False
            if value < schema.get("x-date-minimum", value) or value > schema.get("x-date-maximum", value):
                return False
    return True


def representative(document, raw_schema, bindings):
    schema = check_schema(document, raw_schema)
    if "x-binding" in schema:
        try:
            result = copy.deepcopy(bindings[schema["x-binding"]])
        except KeyError as error:
            raise ContractError(f"Missing binding: {schema['x-binding']}") from error
    elif "example" in schema:
        result = copy.deepcopy(schema["example"])
    elif "enum" in schema:
        result = schema["enum"][0]
    elif "default" in schema:
        result = copy.deepcopy(schema["default"])
    elif schema["type"] == "object":
        result = {key: representative(document, child, bindings)
                  for key, child in schema.get("properties", {}).items()}
    elif schema["type"] == "array":
        result = [representative(document, schema["items"], bindings)
                  for _ in range(max(1, schema.get("minItems", 0)))]
    elif schema["type"] in {"integer", "number"}:
        result = schema.get("minimum", min(1, schema.get("maximum", 1)))
        if schema.get("exclusiveMinimum"):
            result = float(Decimal(str(result)) + Decimal(str(schema.get("x-step", 1))))
        if schema.get("exclusiveMaximum") and result >= schema["maximum"]:
            result = float(Decimal(str(schema["maximum"])) - Decimal(str(schema.get("x-step", 1))))
        if schema["type"] == "integer":
            result = int(result)
    elif schema["type"] == "boolean":
        result = True
    elif schema.get("format") == "binary":
        result = {"filename": "proof.txt", "text": "synthetic proof", "content_type": "text/plain"}
    elif schema.get("format") == "date":
        result = schema.get("x-date-minimum", schema.get("x-date-maximum", "2030-01-07"))
    else:
        result = "x" * max(schema.get("minLength", 0), min(1, schema.get("maxLength", 1)))
    if not accepts(document, schema, result):
        raise ContractError(f"Invalid baseline for schema {schema}: {result!r}")
    return result


def variations(document, raw_schema, required, baseline, bindings):
    schema = check_schema(document, raw_schema)
    yield "EP", "valid", baseline, False, "type"
    yield "EP", "missing", None, True, "required" if required else "optional"
    yield "EP", "null", None, False, "nullable"
    wrong = {"not": "a scalar"} if schema["type"] != "object" else []
    yield "EP", "wrong-type", wrong, False, "type"
    if "enum" in schema:
        for index, value in enumerate(schema["enum"]):
            yield "EP", f"enum-{index}", value, False, "enum"
        yield "EP", "outside-enum", "__not_a_choice__", False, "enum"
    if schema["type"] == "boolean":
        yield "EP", "false", False, False, "type"
    if schema["type"] in {"integer", "number"}:
        yield "EP", "nonnumeric", "not-a-number", False, "type"
        if "minimum" not in schema and "maximum" not in schema and "x-reference" not in schema:
            for label, value in (("negative", -1), ("zero", 0), ("positive", 1)):
                yield "EP", label, value, False, "type"
        if schema["type"] == "integer":
            yield "EP", "fraction", 1.5, False, "type"
    if schema.get("x-reference"):
        key = schema["x-reference"]["missing-binding"]
        if key not in bindings:
            raise ContractError(f"Missing reference binding: {key}")
        yield "EP", "missing-record", bindings[key], False, "x-reference"
    if schema["type"] == "string" and schema.get("format") != "binary":
        yield "EP", "empty", "", False, "minLength"
        if schema.get("x-trim-whitespace"):
            yield "EP", "whitespace", "   ", False, "x-trim-whitespace"
    if schema.get("format") == "date":
        yield "EP", "bad-date", "2030-02-30", False, "format"
    if schema["type"] == "array":
        yield "EP", "empty", [], False, "minItems"
        items = check_schema(document, schema["items"])
        invalid_item = [] if items["type"] == "object" else {"invalid": "item"}
        invalid_array = copy.deepcopy(baseline)
        if invalid_array:
            invalid_array[0] = invalid_item
            yield "EP", "invalid-item", invalid_array, False, "items"
    if schema.get("format") == "binary":
        empty = {**baseline, "text": ""}
        yield "EP", "empty-file", empty, False, "x-allow-empty-file"
        yield "EP", "empty-filename", {**baseline, "filename": ""}, False, "format"
    for key in ("minimum", "maximum", "minLength", "maxLength", "minItems", "maxItems",
                "x-date-minimum", "x-date-maximum", "x-filename-maxLength"):
        if key not in schema:
            continue
        limit = schema[key]
        for label, delta in (("below", -1), ("at", 0), ("above", 1)):
            if key.startswith("x-date-"):
                value = (date.fromisoformat(limit) + timedelta(days=delta)).isoformat()
            elif key == "x-filename-maxLength":
                value = {**baseline, "filename": "a" * (limit + delta)}
            elif key in {"minLength", "maxLength"}:
                if limit + delta < 0:
                    # There is no string with length -1: explicit N/A is recorded.
                    continue
                value = "x" * (limit + delta)
            elif key in {"minItems", "maxItems"}:
                if limit + delta < 0:
                    continue
                value = [representative(document, schema["items"], bindings)
                         for _ in range(limit + delta)]
            else:
                value = float(Decimal(str(limit)) + Decimal(delta) * Decimal(str(schema.get("x-step", 1))))
                if schema["type"] == "integer":
                    value = int(value)
            yield "BVA", f"{key}-{label}", value, False, key


def input_fields(document, schema, prefix=(), required=True):
    """Flatten nested object leaves; arrays remain one input with item predicates."""
    schema = check_schema(document, schema)
    if schema["type"] == "object" and schema.get("properties"):
        for key, child in schema["properties"].items():
            child_schema = check_schema(document, child)
            path = (*prefix, key)
            # Keep container omission/null/type cases as well as its leaves.
            if child_schema["type"] == "object":
                yield path, child_schema, key in schema.get("required", [])
            yield from input_fields(document, child, path, key in schema.get("required", []))
    else:
        yield prefix, schema, required


def set_value(request, location, path, value, omit=False):
    result = copy.deepcopy(request)
    target = result[location]
    for name in path[:-1]:
        target = target[name]
    if omit:
        target.pop(path[-1], None)
    else:
        target[path[-1]] = copy.deepcopy(value)
    return result


def generate(document, bindings):
    if document.get("openapi") != "3.0.3":
        raise ContractError("Supported dialect is OpenAPI 3.0.3 JSON")
    unknown_extensions = {key for key in document if key.startswith("x-")} - {"x-exclusions"}
    if unknown_extensions:
        raise ContractError(f"Unsupported root extensions: {sorted(unknown_extensions)}")
    cases, inventory, operations = [], [], []
    seen_ids = set()
    for path, path_item in sorted(document.get("paths", {}).items()):
        for method, operation in sorted(path_item.items()):
            if method == "parameters":
                continue
            if method not in {"get", "post", "put", "patch", "delete"}:
                raise ContractError(f"Unsupported path item: {method}")
            operation_id = operation.get("operationId")
            if not operation_id or operation_id in seen_ids:
                raise ContractError("Every operation needs a unique operationId")
            seen_ids.add(operation_id)
            operations.append(operation_id)
            if any(key.startswith("x-") and key not in {"x-role", "x-requirements", "x-source", "x-exclusions", "x-date-order"}
                   for key in operation):
                raise ContractError(f"Unsupported operation extension: {operation_id}")
            baseline = {"body": {}, "path": {}, "query": {}}
            fields = []
            parameters = {}
            for raw in path_item.get("parameters", []) + operation.get("parameters", []):
                parameter = resolve(document, raw)
                if set(parameter) - {"name", "in", "required", "description", "schema", "example", "deprecated"}:
                    raise ContractError("Unsupported relevant parameter options/serialization")
                parameters[(parameter["in"], parameter["name"])] = parameter
            for (location, name), parameter in sorted(parameters.items()):
                if location not in {"path", "query"}:
                    raise ContractError("Harness auth headers are not generated inputs")
                if location == "path" and not parameter.get("required"):
                    raise ContractError("Path parameters must be required")
                if parameter.get("style") or parameter.get("explode") is not None:
                    raise ContractError("Custom parameter serialization unsupported")
                schema = check_schema(document, parameter["schema"])
                baseline[location][name] = representative(document, schema, bindings)
                fields.append((location, (name,), schema, parameter.get("required", False)))
            placeholders = set(re.findall(r"\{([^}]+)\}", path))
            if placeholders != set(baseline["path"]):
                raise ContractError(f"Path placeholders/parameters disagree: {path}")
            media_type = None
            if "requestBody" in operation:
                body = resolve(document, operation["requestBody"])
                content = body.get("content", {})
                if len(content) != 1:
                    raise ContractError("Scoped operation must select exactly one request media type")
                media_type, media = next(iter(content.items()))
                if set(media) - {"schema", "example", "examples"}:
                    raise ContractError("Unsupported media encoding/options")
                if media_type not in {"application/json", "multipart/form-data"}:
                    raise ContractError(f"Unsupported request media: {media_type}")
                schema = check_schema(document, media["schema"])
                if schema["type"] != "object":
                    raise ContractError("Request body must be an object")
                baseline["body"] = representative(document, schema, bindings)
                fields += [("body", field, child, required)
                           for field, child, required in input_fields(document, schema)]
            for location, field, schema, required in fields:
                value = baseline[location]
                for part in field:
                    value = value[part]
                bounds = [key for key in schema if key in {
                    "minimum", "maximum", "minLength", "maxLength", "minItems", "maxItems",
                    "x-date-minimum", "x-date-maximum", "x-filename-maxLength"}]
                inventory.append({
                    "operation": operation_id, "location": location, "field": list(field),
                    "source": schema.get("x-source", operation.get("x-source")),
                    "bva_constraints": bounds,
                    "bva_na": [] if bounds else ["No ordered declared limit; enum/type/reference EP only"],
                    "unrepresentable": [f"{key}-below: negative length/cardinality has no wire value"
                                        for key in ("minLength", "minItems") if schema.get(key) == 0],
                    "wire_coercion": schema.get("x-wire-coercion"),
                })
                for technique, label, mutated, omit, constraint in variations(document, schema, required, value, bindings):
                    schema_valid = not required if omit else accepts(document, schema, mutated)
                    expected = "accept" if schema_valid else "reject"
                    oracle = "schema"
                    if label == "missing-record":
                        expected, oracle = "reject", "database-reference"
                    case_id = f"{operation_id}:{location}:{'.'.join(field)}:{technique}:{label}"
                    cases.append({
                        "id": case_id, "operation": operation_id, "method": method.upper(),
                        "route": path, "role": operation.get("x-role", "employee"),
                        "media_type": media_type, "location": location, "field": list(field),
                        "technique": technique, "class": label, "omitted": omit,
                        "value": None if omit else mutated, "baseline": baseline,
                        "request": set_value(baseline, location, field, mutated, omit),
                        "expected": {"predicate": expected, "oracle": oracle,
                                     "schema_valid": schema_valid},
                        "requirements": operation.get("x-requirements", []),
                        "provenance": {"constraint": constraint, "schema": schema,
                                       "source": schema.get("x-source", operation.get("x-source"))},
                    })
                    if technique == "BVA":
                        unit = ("calendar days" if constraint.startswith("x-date-") else
                                "filename characters" if constraint == "x-filename-maxLength" else
                                "characters after trim" if "Length" in constraint and schema.get("x-trim-whitespace") else
                                "characters" if "Length" in constraint else
                                "items" if "Items" in constraint else "numeric units")
                        exclusive = schema.get("exclusiveMinimum" if constraint == "minimum" else "exclusiveMaximum", False) if constraint in {"minimum", "maximum"} else False
                        cases[-1]["boundary"] = {"limit": schema[constraint], "unit": unit,
                                                 "step": schema.get("x-step", 1), "inclusive": not exclusive}
            if "x-date-order" in operation:
                relation = operation["x-date-order"]
                if set(relation) != {"start", "end", "source"}:
                    raise ContractError("x-date-order requires start, end, source")
                start, end = relation["start"], relation["end"]
                body_fields = {field[0]: child for location, field, child, _ in fields
                               if location == "body" and len(field) == 1}
                if any(name not in body_fields or body_fields[name].get("format") != "date"
                       for name in (start, end)):
                    raise ContractError("x-date-order fields must be declared top-level dates")
                anchor = date.fromisoformat(baseline["body"][start])
                if date.fromisoformat(baseline["body"][end]) < anchor:
                    raise ContractError("Baseline violates x-date-order")
                for entry in inventory:
                    if entry["operation"] == operation_id and entry["location"] == "body" and entry["field"] == [end]:
                        entry["bva_constraints"].append("x-date-order")
                        entry["bva_na"] = []
                for label, delta in (("below", -1), ("at", 0), ("above", 1)):
                    value = (anchor + timedelta(days=delta)).isoformat()
                    schema_valid = accepts(document, body_fields[end], value)
                    cases.append({
                        "id": f"{operation_id}:body:{end}:BVA:date-order-{label}",
                        "operation": operation_id, "method": method.upper(), "route": path,
                        "role": operation.get("x-role", "employee"), "media_type": media_type,
                        "location": "body", "field": [end], "technique": "BVA",
                        "class": f"date-order-{label}", "omitted": False, "value": value,
                        "baseline": baseline, "request": set_value(baseline, "body", [end], value),
                        "expected": {"predicate": "accept" if delta >= 0 and schema_valid else "reject",
                                     "oracle": "date-order", "schema_valid": schema_valid},
                        "requirements": operation.get("x-requirements", []),
                        "provenance": {"constraint": "x-date-order", "schema": body_fields[end],
                                       "source": relation["source"]},
                        "boundary": {"limit": anchor.isoformat(), "anchor_field": start,
                                     "unit": "calendar days", "step": 1, "inclusive": True},
                    })
    result = {
        "format_version": 1, "spec_sha256": fingerprint(document),
        "bindings_sha256": fingerprint(bindings), "operations": operations,
        "inventory": inventory, "cases": cases,
        "exclusions": document.get("x-exclusions", []),
        "coverage_complete": not document.get("x-exclusions"),
    }
    result["data_sha256"] = fingerprint(result)
    return result


def verify_fresh(artifact, document, bindings):
    expected = generate(document, bindings)
    if artifact != expected:
        raise ContractError("Stale or altered generated data: regenerate from current spec/bindings/code")
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--bindings", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--require-complete", action="store_true",
                        help="Exit 3 when the declared scope still has exclusions")
    args = parser.parse_args()
    try:
        document, bindings = load_json(args.spec), load_json(args.bindings)
        if args.check:
            result = verify_fresh(load_json(args.output), document, bindings)
        else:
            result = generate(document, bindings)
            Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
        print(json.dumps({"cases": len(result["cases"]), "operations": len(result["operations"]),
                          "spec_sha256": result["spec_sha256"], "data_sha256": result["data_sha256"],
                          "coverage_complete": result["coverage_complete"], "exclusions": result["exclusions"]}))
        if args.require_complete and not result["coverage_complete"]:
            parser.exit(3, "Coverage incomplete: resolve documented exclusions before a completion gate\n")
    except (ContractError, OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(2, f"Generation blocked: {error}\n")


if __name__ == "__main__":
    main()
