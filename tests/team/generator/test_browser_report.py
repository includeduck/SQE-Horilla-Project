"""A report must not convert missing/failed/skipped/extra browser results to acceptance."""

import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from browser_report import EXPECTED, render


class BrowserReportTests(unittest.TestCase):
    def test_only_all_ten_exact_passing_results_satisfy_completion(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, output = Path(temporary) / "input.xml", Path(temporary) / "report.html"
            root = ET.Element("testsuite")
            for key in EXPECTED:
                ET.SubElement(root, "testcase", name="test_flow[" + key + "]", time="1")
            ET.ElementTree(root).write(source)
            self.assertTrue(render(source, output))
            ET.SubElement(root, "testcase", name="unexpected")
            ET.ElementTree(root).write(source)
            self.assertFalse(render(source, output))
            self.assertIn("Overall: HOLD", output.read_text(encoding="utf-8"))

    def test_missing_failed_errored_and_skipped_results_do_not_become_passes(self):
        for tag in (None, "failure", "error", "skipped"):
            with self.subTest(tag=tag), tempfile.TemporaryDirectory() as temporary:
                source, output = Path(temporary) / "input.xml", Path(temporary) / "report.html"
                root = ET.Element("testsuite")
                if tag:
                    case = ET.SubElement(root, "testcase", name="test_flow[UC-RAY-01-MAIN]")
                    ET.SubElement(case, tag).text = "<script>untrusted failure text</script>"
                ET.ElementTree(root).write(source)
                self.assertFalse(render(source, output))
                text = output.read_text(encoding="utf-8")
                self.assertIn("Verified passes: 0/10", text)
                self.assertNotIn("<script>", text)
