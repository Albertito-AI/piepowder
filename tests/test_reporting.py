"""Boundary and injection checks for the offline record renderers."""

import base64
import hashlib
from html.parser import HTMLParser
import json
import re
import unittest

from piepowder.reporting import render_dashboard, render_markdown


class PageProbe(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.tags = []
        self.scripts = []
        self.style = ""
        self.policy = ""
        self.active = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script":
            self.scripts.append({"attrs": attrs, "text": ""})
            self.active = "script"
        elif tag == "style":
            self.active = "style"
        elif tag == "meta" and attrs.get("http-equiv") == "Content-Security-Policy":
            self.policy = attrs["content"]

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.active = None

    def handle_data(self, data):
        if self.active == "script":
            self.scripts[-1]["text"] += data
        elif self.active == "style":
            self.style += data


def sample(case_id="geocode-ambiguous"):
    return {
        "schema_version": "piepowder.analysis/0.1", "case_id": case_id,
        "status": "HUMAN_REVIEW", "work_allowed": False, "payment_authorised": False,
        "reasons": [{"code": "AMBIGUOUS_DENOMINATOR", "path": "contract.acceptance",
                     "message": "The denominator is unspecified.", "severity": "REVIEW"}],
        "lint": [], "evidence": {"status": "BYTE_MATCH", "items": [], "authenticity": "UNVERIFIED"},
        "bindings": {"agreement_sha256": "a" * 64},
        "assurance": {"identity": "UNVERIFIED", "authority": "UNVERIFIED", "legal_effect": "NONE"},
        "checks": [{"check_id": "quality", "obligation_id": "delivery", "kind": "geocode_accuracy",
                    "result": "UNKNOWN", "reason_codes": ["AMBIGUOUS_DENOMINATOR"],
                    "metrics": {"selected_denominator": "unspecified", "threshold_bps": 9800,
                                "readings": {
                                    "all_sampled": {"numerator": 972, "denominator": 1000,
                                                    "percentage": "97.200000", "threshold_satisfied": False},
                                    "exclude_flagged": {"numerator": 972, "denominator": 983,
                                                        "percentage": "98.880977", "threshold_satisfied": True}}}}],
    }


class ReportingTests(unittest.TestCase):
    def test_adversarial_values_remain_data_in_html_and_markdown(self):
        hostile = ('</script><svg onload="alert(1)"></svg><script src="https://invalid.example/x">'
                   '&\'"\u2028\u2029\n```\n# Forged decision\n[pay](javascript:alert(1))\n'
                   '````````\n__SCRIPT____CASE_DATA____CSP__')
        record = sample(hostile)
        record["reasons"][0]["message"] = hostile
        record["bindings"][hostile] = hostile
        page = render_dashboard([record])
        probe = PageProbe()
        probe.feed(page)
        self.assertEqual(len(probe.scripts), 2)
        payload = probe.scripts[0]["text"]
        self.assertEqual(json.loads(payload), [record])
        for character in ("<", ">", "&", "'", "\u2028", "\u2029"):
            self.assertNotIn(character, payload)
        self.assertFalse(any(tag in ("svg", "iframe", "img", "input", "form") for tag, _ in probe.tags))
        self.assertFalse(any(key.startswith("on") or key in ("src", "href")
                             for _, attrs in probe.tags for key in attrs))
        script = probe.scripts[1]["text"]
        self.assertNotIn("innerHTML", script)
        self.assertNotRegex(script, r"\beval\s*\(|new\s+Function\b|\bfetch\s*\(")
        for text in (script, probe.style):
            digest = base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()
            self.assertIn("'sha256-" + digest + "'", probe.policy)
        self.assertIn("connect-src 'none'", probe.policy)
        markdown = render_markdown(record)
        outside, fence = [], None
        for line in markdown.splitlines():
            if fence is None and re.fullmatch(r"`{3,}json", line):
                fence = line[:-4]
            elif fence is not None and line == fence:
                fence = None
            elif fence is None:
                outside.append(line)
        self.assertIsNone(fence)
        self.assertNotIn("Forged decision", "\n".join(outside))
        self.assertNotIn("javascript:", "\n".join(outside))
        self.assertNotIn("<svg", markdown)

    def test_boundaries_both_readings_and_empty_state_are_retained(self):
        record = sample()
        page = render_dashboard([record])
        probe = PageProbe()
        probe.feed(page)
        parsed = json.loads(probe.scripts[0]["text"])[0]
        self.assertEqual(parsed, record)
        self.assertFalse(parsed["work_allowed"])
        self.assertFalse(parsed["payment_authorised"])
        for text in ("Synthetic scenarios only", "No legal judgment.", "No work authorisation.",
                     "No payment authorisation.", "does not independently re-read or hash", "No case records supplied"):
            self.assertIn(text, page)
        self.assertFalse(any(tag == "button" for tag, _ in probe.tags))
        markdown = render_markdown(record)
        for text in ("97.200000", "98.880977", "all_sampled", "exclude_flagged", "UNKNOWN",
                     '"work_allowed": false', '"payment_authorised": false', "not a legal judgment"):
            self.assertIn(text, markdown)
        empty = PageProbe()
        empty.feed(render_dashboard([]))
        self.assertEqual(json.loads(empty.scripts[0]["text"]), [])
        self.assertIn("select.disabled = true", empty.scripts[1]["text"])


if __name__ == "__main__":
    unittest.main()
