"""Independent experiment integrity checks, separate from HTTP assertions."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from demonstrate_regeneration import build_experiment
from generate import load_json


class RegenerationTests(unittest.TestCase):
    def test_two_constraint_changes_regenerate_boundaries_and_preserve_baseline(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / "experiment"
            report = build_experiment(folder)
            before = {case["id"]: case for case in load_json(folder / "baseline.cases.json")["cases"]}
            after = {case["id"]: case for case in load_json(folder / "variant.cases.json")["cases"]}
            for suffix, expected in (("below", 2), ("at", 3), ("above", 4)):
                key = "self_allocation_create:body:description:BVA:minLength-" + suffix
                self.assertEqual(len(after[key]["value"]), expected)
                self.assertEqual(len(before[key]["value"]), expected - 2)
            key = "self_allocation_create:body:attachment:BVA:x-filename-maxLength-above"
            self.assertEqual(len(before[key]["value"]["filename"]), 101)
            self.assertEqual(len(after[key]["value"]["filename"]), 81)
            self.assertTrue(report["stale_output"]["rejected"])
            self.assertTrue(report["canonical_baseline_preserved"])
            self.assertNotEqual(report["baseline_data_sha256"], report["variant_data_sha256"])
            self.assertTrue(report["unchanged_case_ids"])

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(FileExistsError):
                build_experiment(Path(temporary))


if __name__ == "__main__":
    unittest.main()
