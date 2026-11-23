"""Verify the producer's failure propagation; no mocked HTTP/product tests."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TEAM = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("area2_runner", TEAM / "run_area2.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    def test_child_failure_preserves_exit_code_and_log(self):
        with tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
            folder = Path(temp)
            result = runner.execute_stage("probe", [sys.executable, "-c", "print('synthetic fail-propagation probe'); raise SystemExit(7)"], folder)
            self.assertEqual(result["exit_code"], 7)
            self.assertEqual(result["status"], "failed")
            self.assertIn("synthetic", (folder / "probe.txt").read_text())

    def test_child_success_and_missing_xml_are_distinct(self):
        with tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
            folder = Path(temp)
            result = runner.execute_stage("probe", [sys.executable, "-c", "print('synthetic success probe')"], folder)
            self.assertEqual(result["exit_code"], 0)
            self.assertIsNone(runner.xml_totals(folder / "absent.xml"))

    def test_xml_counts_skips_errors_and_failures(self):
        with tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
            path = Path(temp) / "result.xml"
            path.write_text('<testsuites><testsuite><testcase/><testcase><failure/></testcase><testcase><error/></testcase><testcase><skipped/></testcase></testsuite></testsuites>', encoding="utf-8")
            self.assertEqual(runner.xml_totals(path), {"cases": 4, "failures": 1, "errors": 1, "skipped": 1})

    def test_command_order_reverses_second_clean_api_run_and_keeps_gate(self):
        commands = runner.stage_commands(Path("synthetic-evidence"))
        self.assertEqual([name for name, _ in commands], ["generator", "freshness", "schema", "django", "api-first", "api-reversed", "complete-scope"])
        self.assertIn("--area2-reverse", commands[-2][1])
        self.assertIn("--require-complete", commands[-1][1])

    def test_existing_evidence_directory_is_not_overwritten(self):
        with tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
            marker = Path(temp) / "retained.txt"
            marker.write_text("retained", encoding="utf-8")
            result = subprocess.run([sys.executable, str(TEAM / "run_area2.py"), "--evidence", temp], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(marker.read_text(encoding="utf-8"), "retained")


if __name__ == "__main__":
    unittest.main()
