"""Verify the producer's failure propagation; no mocked HTTP/product tests."""

import importlib.util
import json
import os
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
        self.assertEqual([name for name, _ in commands], ["generator", "freshness", "schema", "django", "api-preflight", "api-first", "api-reversed", "complete-scope"])
        self.assertIn("--maxfail=1", commands[4][1])
        self.assertIn("--area2-reverse", commands[-2][1])
        self.assertIn("--require-complete", commands[-1][1])

    def test_existing_evidence_directory_is_not_overwritten(self):
        with tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
            marker = Path(temp) / "retained.txt"
            marker.write_text("retained", encoding="utf-8")
            result = subprocess.run([sys.executable, str(TEAM / "run_area2.py"), "--evidence", temp], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(marker.read_text(encoding="utf-8"), "retained")

    def test_failed_first_api_still_runs_reverse_and_scope_without_losing_failure(self):
        with tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
            folder = Path(temp)
            reverse = folder / "api-reversed.xml"
            write_xml = "from pathlib import Path; Path(" + repr(str(reverse)) + ").write_text('<testsuite><testcase/></testsuite>')"
            commands = [
                ("api-first", [sys.executable, "-c", "raise SystemExit(7)"]),
                ("api-reversed", [sys.executable, "-c", write_xml]),
                ("complete-scope", [sys.executable, "-c", "raise SystemExit(3)"]),
            ]
            results, failure, code = runner.run_stages(commands, folder, os.environ.copy())
            self.assertEqual([r["status"] for r in results], ["failed", "passed", "failed"])
            self.assertEqual((failure, code), ("api-first", 7))
            self.assertEqual(runner.xml_totals(reverse)["cases"], 1)

    def test_prerequisite_failure_blocks_dependent_application_stages(self):
        with tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
            commands = [("schema", [sys.executable, "-c", "raise SystemExit(2)"]),
                        ("api-first", [sys.executable, "-c", "raise SystemExit(8)"]),
                        ("api-reversed", [sys.executable, "-c", "raise SystemExit(8)"]),
                        ("complete-scope", [sys.executable, "-c", "raise SystemExit(8)"])]
            results, failure, code = runner.run_stages(commands, Path(temp), os.environ.copy())
            self.assertEqual((failure, code), ("schema", 2))
            self.assertTrue(all(r["status"] == "blocked" for r in results[1:]))

    def test_zero_exit_does_not_hide_invalid_or_failed_junit(self):
        documents = [None, "<not-xml", "<testsuite/>",
                     "<testsuite><testcase><failure/></testcase></testsuite>",
                     "<testsuite><testcase><error/></testcase></testsuite>",
                     "<testsuite><testcase><skipped/></testcase></testsuite>"]
        for document in documents:
            with self.subTest(document=document), tempfile.TemporaryDirectory(prefix="sqe-runner-") as temp:
                folder = Path(temp)
                if document is not None:
                    (folder / "api-first.xml").write_text(document, encoding="utf-8")
                results, failure, code = runner.run_stages(
                    [("api-first", [sys.executable, "-c", "pass"])], folder, os.environ.copy())
                self.assertEqual((failure, code), ("api-first", 4))
                self.assertEqual(results[0]["status"], "failed")
                totals = runner.manifest_totals(folder / "api-first.xml")
                if document == "<not-xml":
                    self.assertTrue(totals["invalid"])


if __name__ == "__main__":
    unittest.main()
