"""Negative controls for requirement evidence, not mocked application tests."""
import copy
import unittest
import requirement_evidence as trace


class RequirementEvidenceTests(unittest.TestCase):
    def data(self):
        case="STATE-ALLOC-requested-approve"
        return ({"cases":[],"spec_sha256":"SPEC"},
                {"entries":[{"case_id":case,"file":"test_states_and_decisions.py"}]},
                [{"expected_source_sha":"SOURCE","results":{case:[{"status":"passed","source_sha":"SOURCE","spec_sha256":"SPEC"}]}}])

    def test_missing_or_failed_assertion_keeps_requirement_partial(self):
        artifact,ledger,reports=self.data()
        row=lambda result:next(r for r in result["requirements"] if r["requirement"]=="FR-02")
        self.assertEqual(row(trace.build(artifact,ledger,reports,"SOURCE"))["status"],"verified-on-recorded-source")
        failed=copy.deepcopy(reports);next(iter(failed[0]["results"].values()))[0]["status"]="failure"
        self.assertEqual(row(trace.build(artifact,ledger,failed,"SOURCE"))["status"],"partial")
        reports[0]["results"].clear()
        self.assertEqual(row(trace.build(artifact,ledger,reports,"SOURCE"))["status"],"partial")

    def test_wrong_source_and_empty_populations_cannot_claim_acceptance(self):
        artifact,ledger,reports=self.data()
        with self.assertRaises(ValueError):trace.build(artifact,ledger,reports,"WRONG")
        with self.assertRaises(ValueError):trace.build(artifact,ledger,[],"SOURCE")
        self.assertFalse(trace.build(artifact,{"entries":[]},reports,"SOURCE")["all_requirements_verified"])
