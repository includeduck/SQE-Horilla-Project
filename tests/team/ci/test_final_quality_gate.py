"""Synthetic negative controls for the gate, never application/mutation results."""
import importlib.util, tempfile, unittest
from pathlib import Path
SPEC=importlib.util.spec_from_file_location("gate",Path(__file__).resolve().parents[3]/"scripts/team/final_quality_gate.py")
gate=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(gate)
class GateTests(unittest.TestCase):
    def test_wrong_sonar_revision_refused(self):
        with self.assertRaises(ValueError):gate.validate_sonar({"analyses":[{"revision":"old"}]},{}, "current")
    def test_first_scan_empty_conditions_not_acceptance(self):
        with self.assertRaises(ValueError):gate.validate_sonar({"analyses":[{"revision":"s","key":"a"}]},{"projectStatus":{"status":"OK","conditions":[]}},"s")
    def test_failed_server_gate_refused(self):
        with self.assertRaises(ValueError):gate.validate_sonar({"analyses":[{"revision":"s"}]},{"projectStatus":{"status":"ERROR"}},"s")
    def test_realistic_server_conditions_pass_but_weaker_threshold_fails(self):
        analyses={"analyses":[{"revision":"s","key":"actual-analysis-id"}]}
        conditions=[{"metricKey":key,"status":"OK","errorThreshold":str(limit)} for key,limit in
            (("new_duplicated_lines_density",3),("new_reliability_rating",1),("new_security_rating",1),
             ("new_blocker_violations",0),("new_critical_violations",0))]
        data={"projectStatus":{"status":"OK","conditions":conditions}}
        self.assertEqual(gate.validate_sonar(analyses,data,"s")["status"],"OK")
        conditions[0]["errorThreshold"]="10"
        with self.assertRaises(ValueError):gate.validate_sonar(analyses,data,"s")
    def test_missing_mutation_threshold_not_defaulted(self):
        with self.assertRaises(KeyError):gate.validate_mutation({"source_sha":"s","tool":"mutmut"},{}, "s")
    def test_wrong_mutation_source_refused(self):
        with self.assertRaises(ValueError):gate.validate_mutation({"source_sha":"other","tool":"mutmut"},{}, "s")
    def test_aggregate_dependency_failures_propagate(self):
        import os, subprocess, sys, json
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)/"gate.json";env=dict(os.environ,UNIT_RESULT="success",SONAR_RESULT="failure",MUTATION_RESULT="skipped")
            run=subprocess.run([sys.executable,SPEC.origin,"aggregate","--source","s","--output",str(target)],env=env,capture_output=True)
            self.assertEqual(run.returncode,1);data=json.loads(target.read_text())
            self.assertFalse(data["accepted"]);self.assertEqual(data["dependencies"]["SONAR_RESULT"],"failure")
if __name__=="__main__":unittest.main()
