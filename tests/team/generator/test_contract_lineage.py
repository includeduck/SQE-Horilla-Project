"""Historical smoke evidence must not become a pass on a changed contract."""
import copy
import importlib.util
import unittest
from pathlib import Path

TEAM=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("contract_inventory",TEAM/"contract/inventory.py")
inventory=importlib.util.module_from_spec(spec);spec.loader.exec_module(inventory)


class ContractLineageTests(unittest.TestCase):
    def inputs(self):
        read=inventory.read;finish=inventory.FINISH
        return [read(TEAM/"generator/generated_cases.json"),read(TEAM/"generator/openapi.json"),
            read(finish/"PROMPT_01_VERIFICATION.json"),read(finish/"PROMPT03_EXCLUSION_RECONCILIATION.json"),
            read(finish/"PROMPT03_PREVIOUS_OPENAPI.json"),read(TEAM/"generator/bindings.json")]

    def test_proven_metadata_lineage_keeps_old_passes_historical(self):
        self.assertEqual(inventory.historical_verified_ids(*self.inputs()),set())

    def test_api_constraint_changes_cannot_use_metadata_only_proof(self):
        args=self.inputs();doc=args[1]
        body=doc["paths"]["/api/v1/leave/user-request/"]["post"]["requestBody"]
        body["required"]=not body.get("required",False)
        with self.assertRaisesRegex(AssertionError,"API constraints"):
            inventory.historical_verified_ids(*args)
