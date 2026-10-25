from copy import deepcopy
import unittest

from piepowder.docket import DocketError, append_event, new_docket, verify_docket


class DocketTests(unittest.TestCase):
    def setUp(self):
        self.d = new_docket("fictional-1", "a" * 64, "seller", "buyer", "2026-10-27T12:00:00Z",
                            {"sample": {"sha256": "b" * 64, "submitted_by": "seller"}})
        self.count = 0

    def add(self, kind, actor, data=None, at="2026-10-26T12:00:00Z"):
        self.count += 1
        event = {"event_id": f"e{self.count}", "kind": kind, "actor_id": actor, "at": at, "data": data or {}}
        self.d = append_event(self.d, event, verify_docket(self.d)["head_sha256"])
        return event

    def file(self):
        self.add("FILE", "seller", {"notice_recorded_to": ["seller", "buyer"]})

    def close_evidence(self):
        self.file()
        self.add("ANSWER", "buyer")
        self.add("ADD_EVIDENCE", "seller", {"evidence_id": "sample"})
        self.add("CLOSE_EVIDENCE", "case_manager", {"acknowledged_by": ["buyer", "seller"]})

    def assess(self, status="HUMAN_REVIEW"):
        self.add("RECORD_ASSESSMENT", "engine", {"assessment_sha256": "c" * 64, "status": status,
                                                 "cited_evidence_ids": ["sample"]})

    def test_closed_record_routes_to_human_without_legal_or_financial_effect(self):
        self.close_evidence()
        self.assess()
        self.add("REFER_HUMAN", "case_manager", {"reason": "Denominator remains contested."})
        result = verify_docket(self.d)
        self.assertEqual(result["phase"], "HUMAN_REVIEW_PENDING")
        for k in ("work_allowed", "payment_authorised", "authority_verified", "notice_verified", "timestamps_authenticated"):
            self.assertFalse(result[k])
        self.assertEqual(result["legal_effect"], "none")

    def test_timeout_preserves_late_response_and_requires_review(self):
        self.file()
        self.add("TIMEOUT", "case_manager", at="2026-10-27T12:00:00Z")
        self.assertEqual(verify_docket(self.d)["phase"], "FILED")
        self.add("ANSWER", "buyer", at="2026-10-28T12:00:00Z")
        result = verify_docket(self.d)
        self.assertEqual(result["phase"], "ANSWERED")
        self.assertTrue(result["requires_human_review"])
        self.assertIn("LATE_ANSWER_RECORDED_WITHOUT_FORFEITURE", result["flags"])

    def test_early_timeout_is_rejected(self):
        self.file()
        with self.assertRaises(DocketError):
            self.add("TIMEOUT", "case_manager")

    def test_no_evidence_admission_after_closure(self):
        self.close_evidence()
        before = deepcopy(self.d)
        with self.assertRaises(DocketError):
            self.add("ADD_EVIDENCE", "seller", {"evidence_id": "sample"})
        self.assertEqual(self.d, before)

    def test_unknown_evidence_and_false_submitter_are_rejected(self):
        self.file()
        for actor, evidence in (("seller", "invented"), ("buyer", "sample")):
            with self.subTest(actor=actor), self.assertRaises(DocketError):
                self.add("ADD_EVIDENCE", actor, {"evidence_id": evidence})

    def test_missing_answer_or_acknowledgement_cannot_close_evidence(self):
        self.file()
        with self.assertRaises(DocketError):
            self.add("CLOSE_EVIDENCE", "case_manager", {"acknowledged_by": ["buyer", "seller"]})
        self.add("ANSWER", "buyer")
        self.add("ADD_EVIDENCE", "seller", {"evidence_id": "sample"})
        with self.assertRaises(DocketError):
            self.add("CLOSE_EVIDENCE", "case_manager", {"acknowledged_by": ["buyer"]})

    def test_no_fictional_citations(self):
        self.close_evidence()
        with self.assertRaises(DocketError):
            self.add("RECORD_ASSESSMENT", "engine", {"assessment_sha256": "c" * 64,
                     "status": "CHECKS_COMPLETE", "cited_evidence_ids": ["imaginary"]})

    def test_reopening_retains_history_and_invalidates_prior_assessment(self):
        self.close_evidence()
        self.assess()
        count = len(self.d["events"])
        self.add("REOPEN_EVIDENCE", "case_manager", {"reason": "Review the same committed index again."})
        result = verify_docket(self.d)
        self.assertEqual(len(self.d["events"]), count + 1)
        self.assertEqual(result["phase"], "ANSWERED")
        self.assertIsNone(result["assessment_sha256"])
        self.assertTrue(result["requires_human_review"])

    def test_stale_head_and_conflicting_retry_fail_exact_retry_is_idempotent(self):
        head = verify_docket(self.d)["head_sha256"]
        event = self.add("FILE", "seller", {"notice_recorded_to": ["seller", "buyer"]})
        self.assertEqual(append_event(self.d, event, head), self.d)
        conflict = deepcopy(event)
        conflict["at"] = "2026-10-26T13:00:00Z"
        with self.assertRaises(DocketError):
            append_event(self.d, conflict, head)
        fresh = {"event_id": "new", "kind": "ANSWER", "actor_id": "buyer", "at": event["at"], "data": {}}
        with self.assertRaises(DocketError):
            append_event(self.d, fresh, head)

    def test_tampering_and_retained_checkpoint_detect_changes(self):
        self.file()
        head = verify_docket(self.d)["head_sha256"]
        tampered = deepcopy(self.d)
        tampered["events"][0]["event"]["actor_id"] = "buyer"
        with self.assertRaises(DocketError):
            verify_docket(tampered)
        truncated = deepcopy(self.d)
        truncated["events"] = []
        self.assertEqual(verify_docket(truncated)["phase"], "DRAFT")
        with self.assertRaises(DocketError):
            verify_docket(truncated, expected_final_hash=head)
        self.assertTrue(verify_docket(self.d, expected_final_hash=head)["checkpoint_compared"])

    def test_backwards_time_and_naive_dates_are_rejected(self):
        self.file()
        for at in ("2026-10-25T12:00:00Z", "2026-10-26T13:00:00", "2026-13-26T13:00:00Z"):
            with self.subTest(at=at), self.assertRaises(DocketError):
                self.add("ANSWER", "buyer", at=at)

    def test_disallowed_money_and_award_actions_are_rejected(self):
        self.close_evidence()
        self.assess("CHECKS_COMPLETE")
        for action in ("EXECUTE", "SETTLE", "AWARD", "RELEASE_FUNDS", "APPROVE_WORK"):
            with self.subTest(action=action), self.assertRaises(DocketError):
                self.add(action, "case_manager")
        result = verify_docket(self.d)
        self.assertFalse(result["payment_authorised"])
        self.assertFalse(result["work_allowed"])

    def test_malformed_status_is_a_domain_error(self):
        self.close_evidence()
        with self.assertRaises(DocketError):
            self.assess(status=[])

    def test_only_simulation_closure_and_no_further_events(self):
        self.file()
        self.add("REFER_HUMAN", "case_manager", {"reason": "Authority requires a human."})
        self.add("CLOSE_SIMULATION", "case_manager", {"note": "Fictional exercise ended; no decision made."})
        self.assertEqual(verify_docket(self.d)["phase"], "CLOSED_IN_SIMULATION")
        with self.assertRaises(DocketError):
            self.add("ANSWER", "buyer")


if __name__ == "__main__":
    unittest.main()
