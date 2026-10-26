"""P02 acceptance labels were written before execution, not inferred from engine output."""
from __future__ import annotations

import json
import unittest

from benchmarks.p02_benchmark import LABELS, evaluate, labelled_cases, run


class PrelabelledBenchmarkTests(unittest.TestCase):
    def test_labels_are_distinct_complete_and_separate_from_shipped_examples(self):
        cases = labelled_cases()
        groups = {category: [x for x in cases if x["group"] == category]
                  for category in ("good", "adverse", "unknown", "adversarial")}
        self.assertEqual(len(cases), 27)
        self.assertTrue(all(len(part) >= 6 for part in groups.values()))
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["edits"])
                self.assertIn(case["expected"]["overall"], ("CHECKS_COMPLETE", "HUMAN_REVIEW", "INVALID"))
                self.assertIn(case["expected"]["quality"], ("SATISFIED", "NOT_SATISFIED", "UNKNOWN", "NOT_RUN", None))
                self.assertTrue(case["description"])
                self.assertTrue(case["id"].startswith(("G", "A", "U", "X")))
        self.assertEqual(json.loads(LABELS.read_text())["prepared_date"], "2026-10-26")

    def test_all_prelabelled_engine_outcomes_and_nonoperative_guards(self):
        for case in labelled_cases():
            with self.subTest(case=case["id"], description=case["description"]):
                row = evaluate(case)
                self.assertTrue(row["pass"], json.dumps(row, indent=2))

    def test_receipt_is_deterministic_and_keeps_independent_review_unknown(self):
        report = run()
        self.assertEqual(report["cases"], 27)
        self.assertEqual(report["passed"], report["cases"])
        self.assertEqual(report["independent_human_first_use"], "NOT_PERFORMED")
        self.assertEqual(report["empirical_accuracy_or_efficiency"], "NOT_MEASURED")


if __name__ == "__main__":
    unittest.main()
