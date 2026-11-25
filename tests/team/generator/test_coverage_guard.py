"""Gate failure probes are independent of the required real application tests."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
TEAM=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("coverage_guard",TEAM/"generator/coverage_guard.py")
guard=importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)


class CoverageGuardTests(unittest.TestCase):
    def small(self):
        return ({"cases":[{"id":"G","field":["description"],"expected":{"oracle":"schema"}}],
                 "spec_sha256":"SPEC","data_sha256":"DATA","exclusions":["mandatory business"]},
                {"spec_sha256":"SPEC","data_sha256":"DATA","unconsumed_generated_case_ids":[],
                 "entries":[{"case_id":"G","generated":True,"file":"api.py"}]},
                {"cases":[],"mandatory_input_families":1})

    def check_xml(self,xml,mutate=None,source=None):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"actual.xml"; path.write_text(xml,encoding="utf-8")
            a,l,w=self.small()
            if mutate: mutate(a,l,w)
            return guard.validate(a,l,w,[path],stage2=True,expected_source=source)

    def xml(self,extra="",spec="SPEC",source="SOURCE"):
        return f'<testsuite><testcase><properties><property name="case_id" value="G"/><property name="spec_sha256" value="{spec}"/><property name="source_sha" value="{source}"/><property name="data_sha256" value="BOUND-DATA"/></properties>{extra}</testcase></testsuite>'

    def test_missing_malformed_and_empty_junit_fail(self):
        for xml in ("<broken","<testsuites/>"):
            with self.assertRaises(Exception): self.check_xml(xml)
        with self.assertRaises(ValueError): guard.results([])

    def test_counters_and_unmapped_pass_do_not_hide_missing_case(self):
        report=self.check_xml('<testsuite tests="999"><testcase name="other"/></testsuite>')
        self.assertFalse(report["stage2_accepted"]); self.assertEqual(report["missing_ids"],["G"])

    def test_skip_failure_error_never_pass(self):
        for tag in ("failure","error","skipped"):
            self.assertFalse(self.check_xml(self.xml(f"<{tag}/>"))["stage2_accepted"])

    def test_wrong_source_or_spec_are_not_passes(self):
        self.assertFalse(self.check_xml(self.xml(spec="OLD"))["stage2_accepted"])
        self.assertFalse(self.check_xml(self.xml(),source="OTHER")["stage2_accepted"])

    def test_stage_acceptance_is_distinct_from_whole_scope(self):
        report=self.check_xml(self.xml(),source="SOURCE")
        self.assertTrue(report["stage2_accepted"]); self.assertFalse(report["complete_scope_accepted"])

    def test_missing_bound_lineage_and_unknown_results_are_refused(self):
        xml=self.xml().replace('<property name="data_sha256" value="BOUND-DATA"/>',"")
        self.assertFalse(self.check_xml(xml)["stage2_accepted"])
        xml=self.xml().replace("</testsuite>",'<testcase><properties><property name="case_id" value="UNKNOWN"/></properties></testcase></testsuite>')
        self.assertFalse(self.check_xml(xml)["stage2_accepted"])

    def test_wire_identity_requires_matching_input_family(self):
        def wire(a,l,w):
            l["entries"][0]["file"]="test_runtime_wire.py"
            w["cases"]=[{"id":"G","input_id":"INPUT:mandatory"}]
        self.assertFalse(self.check_xml(self.xml(),wire)["stage2_accepted"])
        xml=self.xml().replace("</properties>",'<property name="input_family" value="INPUT:mandatory"/></properties>')
        self.assertTrue(self.check_xml(xml,wire)["stage2_accepted"])

    def test_duplicate_missing_consumer_and_invented_na_refused(self):
        with self.assertRaises(ValueError): self.check_xml(self.xml(),lambda a,l,w:l["entries"].append(dict(l["entries"][0])))
        with self.assertRaises(ValueError): self.check_xml(self.xml(),lambda a,l,w:w["cases"].append({"id":"WIRE:mandatory"}))
        with self.assertRaises(ValueError): self.check_xml(self.xml(),lambda a,l,w:l["entries"][0].update(applicability="not_applicable"))

    def test_stale_ledger_and_unsupported_reader_refused(self):
        with self.assertRaises(ValueError): self.check_xml(self.xml(),lambda a,l,w:l.update(data_sha256="OLD"))
        with self.assertRaises(ValueError): self.check_xml(self.xml(),lambda a,l,w:l["entries"][0].update(implementation_status="unsupported"))

    def test_all_stage2_families_materialize_deterministically(self):
        from wire_catalog import build,source_inventory,supplements
        inventory=source_inventory(); actual=build(inventory)
        self.assertEqual(actual,build(copy.deepcopy(inventory)))
        expected={r["id"] for r in inventory["inputs"]+supplements(inventory) if r["stage"]==2}
        self.assertEqual({r["input_id"] for r in actual["cases"]},expected)
        self.assertEqual(len(actual["cases"]),len({r["id"] for r in actual["cases"]}))
        changed=copy.deepcopy(inventory); changed["inputs"][0]["category"]="unsupported"
        with self.assertRaises(ValueError): build(changed)

    def test_business_registration_cannot_be_dropped_even_with_passing_xml(self):
        a,l,w=self.small()
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"actual.xml";path.write_text(self.xml(),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"business reader"):
                guard.validate(a,l,w,[path],stage2=True,required_business=["G"])
            l["entries"][0]["file"]="test_business_rules.py"
            self.assertTrue(guard.validate(a,l,w,[path],stage2=True,required_business=["G"])["stage2_accepted"])
            with self.assertRaisesRegex(ValueError,"business reader"):
                guard.validate(a,l,w,[path],stage2=True,required_business=["G","REQUIRED"])

    def test_all_stage3_input_families_have_specific_business_consumers(self):
        import json,sys
        sys.path.insert(0,str(TEAM/"api"))
        from business_catalog import business_entries
        from wire_catalog import source_inventory,supplements
        artifact=json.loads((TEAM/"generator/generated_cases.json").read_text(encoding="utf-8"))
        entries=business_entries(artifact)
        inventory=source_inventory()
        required={r["id"] for r in inventory["inputs"]+supplements(inventory) if r["stage"]==3}
        self.assertLessEqual(required,{r.get("input_family") for r in entries})
        self.assertEqual(len(entries),len({r["case_id"] for r in entries}))

