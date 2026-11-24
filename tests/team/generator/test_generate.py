"""Focused independent generator regressions; runnable with Python unittest."""

import copy
import ast
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("area2_generate", ROOT / "generate.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def document(properties, required=()):
    return {
        "openapi": "3.0.3",
        "paths": {"/sample/": {"post": {
            "operationId": "sample", "x-requirements": ["R3", "R4", "R5"],
            "requestBody": {"content": {"application/json": {"schema": {
                "type": "object", "properties": properties, "required": list(required),
            }}}},
        }}},
    }


def cases_for(schema, required=True):
    return generator.generate(document({"value": schema}, ["value"] if required else []), {})["cases"]


class GeneratorTests(unittest.TestCase):
    def test_real_contract_deterministic_and_round_trips(self):
        doc = generator.load_json(ROOT / "openapi.json")
        bindings = generator.load_json(ROOT / "bindings.json")
        first = generator.generate(doc, bindings)
        second = generator.generate(copy.deepcopy(doc), dict(reversed(list(bindings.items()))))
        self.assertEqual(first, second)
        self.assertEqual(json.loads(json.dumps(first)), first)
        self.assertEqual(len(first["operations"]), 34)
        self.assertFalse(first["coverage_complete"])
        self.assertTrue(first["exclusions"])
        self.assertEqual(len(first["cases"]), len({c["id"] for c in first["cases"]}))

    def test_contract_operations_exist_in_current_source(self):
        repo = ROOT.parents[2]
        urls = ast.parse((repo / "horilla_api/api_urls/leave/urls.py").read_text(encoding="utf-8"))
        views = ast.parse((repo / "horilla_api/api_views/leave/views.py").read_text(encoding="utf-8"))
        methods = {node.name: {item.name.lower() for item in node.body if isinstance(item, ast.FunctionDef)}
                   for node in views.body if isinstance(node, ast.ClassDef)}
        bases = {node.name: [base.id for base in node.bases if isinstance(base, ast.Name)]
                 for node in views.body if isinstance(node, ast.ClassDef)}

        def inherited_methods(name):
            result = set(methods.get(name, set()))
            for base in bases.get(name, []):
                if base in methods:
                    result |= inherited_methods(base)
            return result

        routes = {}
        for node in ast.walk(urls):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "path":
                route = node.args[0].value.replace("<int:pk>", "{pk}")
                view = node.args[1].func.value.id
                routes["/api/v1/leave/" + route] = inherited_methods(view)
        doc = generator.load_json(ROOT / "openapi.json")
        for route, item in doc["paths"].items():
            self.assertIn(route, routes)
            for method in set(item) - {"parameters"}:
                self.assertIn(method, routes[route])

    def test_required_and_nullable_are_distinct(self):
        cases = cases_for({"type": "string", "nullable": True})
        outcomes = {c["class"]: c["expected"]["predicate"] for c in cases}
        self.assertEqual(outcomes["missing"], "reject")
        self.assertEqual(outcomes["null"], "accept")
        optional = cases_for({"type": "string"}, required=False)
        outcomes = {c["class"]: c["expected"]["predicate"] for c in optional}
        self.assertEqual(outcomes["missing"], "accept")
        self.assertEqual(outcomes["null"], "reject")

    def test_local_reference_resolution(self):
        doc = document({"value": {"$ref": "#/components/schemas/Count"}}, ["value"])
        doc["components"] = {"schemas": {"Count": {"type": "integer", "minimum": 3}}}
        values = [c["value"] for c in generator.generate(doc, {})["cases"] if c["technique"] == "BVA"]
        self.assertEqual(values, [2, 3, 4])

    def test_escaped_pointer_resolution(self):
        doc = {"a/b": {"~x": {"type": "boolean"}}}
        self.assertEqual(generator.resolve(doc, {"$ref": "#/a~1b/~0x"}), {"type": "boolean"})

    def test_bad_references_fail_visibly(self):
        for ref in ("https://example.invalid/schema", "#/absent"):
            with self.subTest(ref=ref), self.assertRaises(generator.ContractError):
                generator.resolve({}, {"$ref": ref})
        with self.assertRaises(generator.ContractError):
            generator.resolve({"loop": {"$ref": "#/loop"}}, {"$ref": "#/loop"})
        recursive = {"node": {"type": "object", "properties": {"child": {"$ref": "#/node"}}}}
        with self.assertRaisesRegex(generator.ContractError, "Recursive input"):
            generator.check_schema(recursive, {"$ref": "#/node"})

    def test_enum_all_members_and_outside_class(self):
        cases = cases_for({"type": "string", "enum": ["full", "half"]})
        enum = [c for c in cases if c["class"].startswith("enum-")]
        self.assertEqual([c["value"] for c in enum], ["full", "half"])
        self.assertTrue(all(c["expected"]["predicate"] == "accept" for c in enum))
        self.assertEqual(next(c for c in cases if c["class"] == "outside-enum")["expected"]["predicate"], "reject")

    def test_integer_limits_and_exclusivity(self):
        cases = cases_for({"type": "integer", "minimum": 2, "maximum": 5, "exclusiveMaximum": True})
        boundaries = {c["class"]: (c["value"], c["expected"]["predicate"]) for c in cases if c["technique"] == "BVA"}
        self.assertEqual(boundaries["minimum-below"], (1, "reject"))
        self.assertEqual(boundaries["minimum-at"], (2, "accept"))
        self.assertEqual(boundaries["maximum-at"], (5, "reject"))
        self.assertEqual(boundaries["maximum-below"], (4, "accept"))

    def test_exact_decimal_steps(self):
        cases = cases_for({"type": "number", "minimum": 0.3, "maximum": 0.9, "x-step": 0.1})
        self.assertEqual([c["value"] for c in cases if c["class"].startswith("minimum-")], [0.2, 0.3, 0.4])

    def test_exclusive_minimum_baseline(self):
        cases = cases_for({"type": "integer", "minimum": 0, "exclusiveMinimum": True})
        self.assertEqual(cases[0]["value"], 1)

    def test_exclusive_maximum_baseline(self):
        cases = cases_for({"type": "integer", "maximum": 0, "exclusiveMaximum": True})
        self.assertEqual(cases[0]["value"], -1)

    def test_bounded_float_requires_real_unit(self):
        with self.assertRaisesRegex(generator.ContractError, "justified x-step"):
            cases_for({"type": "number", "maximum": 5})

    def test_date_limits_and_invalid_calendar_day(self):
        cases = cases_for({"type": "string", "format": "date", "x-date-minimum": "2030-01-07"})
        bva = [(c["value"], c["expected"]["predicate"]) for c in cases if c["technique"] == "BVA"]
        self.assertEqual(bva, [("2030-01-06", "reject"), ("2030-01-07", "accept"), ("2030-01-08", "accept")])
        self.assertEqual(next(c for c in cases if c["class"] == "bad-date")["expected"]["predicate"], "reject")

    def test_date_order_uses_bound_start_and_changes_only_end(self):
        doc = document({"start": {"type": "string", "format": "date", "x-binding": "anchor"},
                        "end": {"type": "string", "format": "date", "x-binding": "end"}}, ["start", "end"])
        doc["paths"]["/sample/"]["post"]["x-date-order"] = {"start": "start", "end": "end", "source": "reviewed source"}
        artifact = generator.generate(doc, {"anchor": "2030-01-07", "end": "2030-01-09"})
        cases = [c for c in artifact["cases"] if c["expected"]["oracle"] == "date-order"]
        self.assertEqual([c["value"] for c in cases], ["2030-01-06", "2030-01-07", "2030-01-08"])
        self.assertEqual([c["expected"]["predicate"] for c in cases], ["reject", "accept", "accept"])
        inventory = next(item for item in artifact["inventory"] if item["field"] == ["end"])
        self.assertEqual(inventory["bva_constraints"], ["x-date-order"])
        self.assertEqual(inventory["bva_na"], [])
        for case in cases:
            self.assertEqual(case["request"]["body"]["start"], "2030-01-07")

    def test_length_limits_and_negative_length_na(self):
        cases = cases_for({"type": "string", "minLength": 1, "maxLength": 4})
        self.assertEqual([len(c["value"]) for c in cases if c["class"].startswith("maxLength-")], [3, 4, 5])
        artifact = generator.generate(document({"value": {"type": "string", "minLength": 0}}), {})
        self.assertTrue(artifact["inventory"][0]["unrepresentable"])

    def test_array_limits_and_single_invalid_item_preserve_count(self):
        cases = cases_for({"type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 4})
        self.assertEqual([len(c["value"]) for c in cases if c["class"].startswith("minItems-")], [1, 2, 3])
        invalid = next(c for c in cases if c["class"] == "invalid-item")
        self.assertEqual(len(invalid["value"]), 2)
        self.assertEqual(invalid["value"][1], invalid["baseline"]["body"]["value"][1])
        self.assertFalse(invalid["expected"]["schema_valid"])

    def test_nested_leaves_and_container_omission(self):
        nested = {"type": "object", "properties": {"name": {"type": "string", "minLength": 1}}, "required": ["name"]}
        artifact = generator.generate(document({"nested": nested}, ["nested"]), {})
        self.assertTrue(any(c["field"] == ["nested"] and c["omitted"] for c in artifact["cases"]))
        self.assertTrue(any(c["field"] == ["nested", "name"] for c in artifact["cases"]))

    def test_one_mutated_dimension_and_valid_baselines(self):
        doc = generator.load_json(ROOT / "openapi.json")
        artifact = generator.generate(doc, generator.load_json(ROOT / "bindings.json"))
        for case in artifact["cases"]:
            with self.subTest(case=case["id"]):
                baseline = copy.deepcopy(case["baseline"])
                candidate = copy.deepcopy(case["request"])
                parent_a, parent_b = baseline[case["location"]], candidate[case["location"]]
                for key in case["field"][:-1]:
                    parent_a, parent_b = parent_a[key], parent_b[key]
                key = case["field"][-1]
                parent_b[key] = copy.deepcopy(parent_a[key])
                self.assertEqual(candidate, baseline)
                self.assertTrue(generator.accepts(doc, case["provenance"]["schema"], parent_a[key]))

    def test_binary_filename_real_three_point_set(self):
        cases = cases_for({"type": "string", "format": "binary", "x-filename-maxLength": 100, "x-allow-empty-file": False})
        bva = [c for c in cases if c["technique"] == "BVA"]
        self.assertEqual([len(c["value"]["filename"]) for c in bva], [99, 100, 101])
        self.assertEqual([c["expected"]["predicate"] for c in bva], ["accept", "accept", "reject"])
        self.assertEqual(next(c for c in cases if c["class"] == "empty-file")["expected"]["predicate"], "reject")
        self.assertEqual([c["boundary"]["unit"] for c in bva], ["filename characters"] * 3)

    def test_whitespace_normalization_is_explicit(self):
        cases = cases_for({"type": "string", "minLength": 1, "x-trim-whitespace": True})
        self.assertEqual(next(c for c in cases if c["class"] == "whitespace")["expected"]["predicate"], "reject")

    def test_unbounded_numeric_partitions_do_not_invent_limits(self):
        cases = cases_for({"type": "number"})
        self.assertEqual([c["value"] for c in cases if c["class"] in {"negative", "zero", "positive"}], [-1, 0, 1])
        self.assertFalse(any(c["technique"] == "BVA" for c in cases))

    def test_pagination_cap_clamps_instead_of_rejecting_above_limit(self):
        cases = cases_for({"type": "integer", "minimum": 1, "default": 20, "x-clamp-maximum": 100})
        boundary = [c for c in cases if c["class"].startswith("x-clamp-maximum-")]
        self.assertEqual([c["value"] for c in boundary], [99, 100, 101])
        self.assertEqual([c["expected"]["predicate"] for c in boundary], ["accept"] * 3)
        self.assertEqual([c["expected"]["normalized_value"] for c in boundary], [99, 100, 100])
        self.assertEqual(boundary[-1]["boundary"]["unit"], "items per page")

    def test_stale_spec_binding_data_and_code_are_detected(self):
        doc = document({"value": {"type": "integer", "minimum": 2}}, ["value"])
        artifact = generator.generate(doc, {})
        self.assertEqual(generator.verify_fresh(artifact, doc, {}), artifact)
        changed = copy.deepcopy(doc)
        changed["paths"]["/sample/"]["post"]["requestBody"]["content"]["application/json"]["schema"]["properties"]["value"]["minimum"] = 3
        with self.assertRaises(generator.ContractError): generator.verify_fresh(artifact, changed, {})
        with self.assertRaises(generator.ContractError): generator.verify_fresh(artifact, doc, {"new": 1})
        artifact["cases"][0]["expected"]["predicate"] = "reject"
        with self.assertRaises(generator.ContractError): generator.verify_fresh(artifact, doc, {})

    def test_supported_constraint_mutation_changes_derived_values(self):
        first = cases_for({"type": "string", "maxLength": 7})
        second = cases_for({"type": "string", "maxLength": 9})
        self.assertEqual([len(c["value"]) for c in first if c["technique"] == "BVA"], [6, 7, 8])
        self.assertEqual([len(c["value"]) for c in second if c["technique"] == "BVA"], [8, 9, 10])

    def test_unknown_constraints_fail_instead_of_silent_coverage(self):
        for extra in ({"pattern": "x+"}, {"allOf": []}, {"x-rule": "invented"}):
            with self.subTest(extra=extra), self.assertRaises(generator.ContractError):
                cases_for({"type": "string", **extra})
        doc = document({"value": {"type": "integer"}})
        doc["x-unimplemented-business-rule"] = {"minimum": 1}
        with self.assertRaises(generator.ContractError): generator.generate(doc, {})

    def test_missing_bindings_and_invalid_binding_fail(self):
        with self.assertRaises(generator.ContractError): cases_for({"type": "integer", "x-binding": "absent"})
        with self.assertRaises(generator.ContractError):
            generator.generate(document({"value": {"type": "integer", "x-binding": "id"}}), {"id": "wrong"})

    def test_invalid_dialect_and_duplicate_ids_fail(self):
        doc = document({"value": {"type": "integer"}})
        doc["openapi"] = "3.1.0"
        with self.assertRaises(generator.ContractError): generator.generate(doc, {})
        doc["openapi"] = "3.0.3"
        doc["paths"]["/other/"] = copy.deepcopy(doc["paths"]["/sample/"])
        with self.assertRaises(generator.ContractError): generator.generate(doc, {})

    def test_query_and_path_are_separate_and_required(self):
        doc = document({"value": {"type": "boolean"}})
        item = doc["paths"].pop("/sample/")
        item["parameters"] = [{"name": "pk", "in": "path", "required": True, "schema": {"type": "integer"}}, {"name": "page", "in": "query", "schema": {"type": "integer", "minimum": 1}}]
        doc["paths"]["/sample/{pk}/"] = item
        artifact = generator.generate(doc, {})
        self.assertEqual({c["location"] for c in artifact["cases"]}, {"body", "query", "path"})
        self.assertEqual(next(c for c in artifact["cases"] if c["location"] == "query" and c["omitted"])["expected"]["predicate"], "accept")

    def test_boolean_false_and_nonfinite_values(self):
        self.assertTrue(generator.accepts({}, {"type": "boolean"}, False))
        self.assertFalse(generator.accepts({}, {"type": "number"}, float("nan")))
        self.assertFalse(generator.accepts({}, {"type": "number"}, True))

    def test_cli_generate_and_check(self):
        with tempfile.TemporaryDirectory(prefix="sqe-generator-") as temp:
            output = str(Path(temp) / "cases.json")
            command = [sys.executable, str(ROOT / "generate.py"), "--spec", str(ROOT / "openapi.json"), "--bindings", str(ROOT / "bindings.json"), "--output", output]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = Path(output).read_bytes()
            self.assertEqual(subprocess.run(command + ["--check"], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(command + ["--check", "--require-complete"], capture_output=True).returncode, 3)
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(Path(output).read_bytes(), original)
            Path(output).write_text("{}", encoding="utf-8")
            self.assertEqual(subprocess.run(command + ["--check"], capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
