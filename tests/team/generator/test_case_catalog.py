"""Independent checks of scenario bookkeeping, not product-rule execution."""

import importlib.util
import json
import unittest
from pathlib import Path

TEAM = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("case_catalog", TEAM / "api/case_catalog.py")
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def test_complete_br02_truth_table_with_explicit_infeasibility(self):
        rows = catalog.decision_rows()
        self.assertEqual(len(rows), 32)
        self.assertEqual(len({tuple(row["conditions"].values()) for row in rows}), 32)
        self.assertEqual(sum(row["feasible"] for row in rows), 24)
        self.assertEqual(sum(row["expected_status"] == 201 for row in rows), 1)
        self.assertTrue(all(row["reason"] for row in rows if not row["feasible"]))

    def test_all_authorization_combinations_and_self_denial(self):
        rows = catalog.authorization_rows()
        self.assertEqual(len(rows), 8)
        self.assertEqual(sum(row["expected_status"] == 200 for row in rows), 3)
        self.assertTrue(all(row["expected_status"] == 403 for row in rows if row["owner"]))

    def test_each_state_has_allowed_or_explicit_terminal_and_invalid_action(self):
        rows = catalog.state_rows()
        self.assertEqual(len(rows), 50)
        self.assertEqual(len({row["id"] for row in rows}), 50)
        for kind, states in (("allocation", catalog.ALLOCATION_STATES), ("leave", catalog.LEAVE_STATES)):
            for state in states:
                entries = [row for row in rows if row["kind"] == kind and row["state"] == state]
                self.assertTrue(any(not row["allowed"] for row in entries), (kind, state))
                if state not in {"cancelled", "rejected"}:
                    self.assertTrue(any(row["allowed"] for row in entries))

    def test_cancellation_rejection_returns_approved_without_refund_state(self):
        row = next(row for row in catalog.state_rows() if row["id"] == "STATE-LEAVE-cancel_requested-cancellation-reject")
        self.assertEqual(row["target"], "approved")
        self.assertEqual(row["expected_status"], 200)

    def test_generated_selection_is_explicit_unique_and_excludes_binary(self):
        artifact = json.loads((TEAM / "generator/generated_cases.json").read_text(encoding="utf-8"))
        selected = catalog.selected_generated_cases(artifact)
        self.assertEqual(len(selected), len({case["id"] for case in selected}))
        self.assertTrue(selected)
        self.assertTrue(all(case["field"] != ["attachment"] and case["location"] == "body" for case in selected))
        self.assertEqual({case["operation"] for case in selected}, {"self_allocation_create", "self_leave_create"})

    def test_balance_oracle_cap_and_forecast_are_separate(self):
        self.assertEqual(catalog.effective_balance(2, 9, "carryforward", 3, 1), 6)
        self.assertEqual(catalog.effective_balance(2, 9, "no carryforward", 3, 1), 3)


if __name__ == "__main__":
    unittest.main()
