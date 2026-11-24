"""Meaningful media-reader refusal and deterministic selection regressions."""
import copy
import unittest
import generate


def document():
    schema = {"type": "object", "properties": {"value": {"type": "integer", "example": 2}}, "required": ["value"]}
    return {"openapi": "3.0.3", "info": {"title": "probe", "version": "1"},
            "paths": {"/sample/": {"post": {"operationId": "sample",
                "requestBody": {"content": {"application/json": {"schema": schema},
                                             "multipart/form-data": {"schema": copy.deepcopy(schema)}}}}}}}


class MediaReaderTests(unittest.TestCase):
    def test_multiple_media_without_explicit_choice_refuses(self):
        with self.assertRaises(generate.ContractError):
            generate.generate(document(), {})

    def test_explicit_choice_is_used_without_claiming_other_media_consumed(self):
        doc = document()
        doc["paths"]["/sample/"]["post"]["x-generator-media-type"] = "multipart/form-data"
        result = generate.generate(doc, {})
        self.assertTrue(result["cases"])
        self.assertEqual({c["media_type"] for c in result["cases"]}, {"multipart/form-data"})
        self.assertEqual(result, generate.generate(doc, {}))

    def test_distinct_schema_in_unselected_media_is_not_silently_ignored(self):
        doc = document()
        op = doc["paths"]["/sample/"]["post"]
        op["x-generator-media-type"] = "multipart/form-data"
        op["requestBody"]["content"]["application/json"]["schema"]["properties"]["value"]["minimum"] = 3
        with self.assertRaises(generate.ContractError):
            generate.generate(doc, {})

    def test_unsupported_alternative_media_is_not_hidden_by_preference(self):
        doc = document()
        op = doc["paths"]["/sample/"]["post"]
        op["x-generator-media-type"] = "multipart/form-data"
        op["requestBody"]["content"]["text/xml"] = copy.deepcopy(op["requestBody"]["content"]["application/json"])
        with self.assertRaises(generate.ContractError):
            generate.generate(doc, {})
