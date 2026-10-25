from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pathlib import Path
import json
import tempfile
import unittest

from piepowder.cli import main, run_demo

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class CliTests(unittest.TestCase):
    def test_demo_integrates_real_engine_reports_and_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "demo"
            summary = run_demo(EXAMPLES, output)
            self.assertEqual(len(summary["cases"]), 6)
            self.assertEqual(summary["cases"][0]["status"], "HUMAN_REVIEW")
            self.assertEqual(summary["cases"][1]["status"], "CHECKS_COMPLETE")
            self.assertEqual(summary["docket_phase"], "HUMAN_REVIEW_PENDING")
            self.assertFalse(summary["payment_authorised"])
            self.assertTrue((output / "dashboard.html").is_file())
            with redirect_stdout(StringIO()) as out:
                code = main(["verify-docket", str(output / "docket.json"), "--expected-sha256", summary["docket_head_sha256"]])
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(out.getvalue())["checkpoint_compared"])
            with redirect_stderr(StringIO()):
                self.assertEqual(main(["verify-docket", str(output / "docket.json"), "--expected-sha256", "f" * 64]), 2)

    def test_existing_outputs_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "demo"
            run_demo(EXAMPLES, output)
            original = (output / "summary.json").read_bytes()
            with self.assertRaises(FileExistsError):
                run_demo(EXAMPLES, output)
            self.assertEqual((output / "summary.json").read_bytes(), original)
            report = Path(tmp) / "report.json"
            report.write_text("owner record", encoding="utf-8")
            with redirect_stderr(StringIO()):
                code = main(["analyse", str(EXAMPLES / "geocode-ambiguous"), "--output", str(report)])
            self.assertEqual(code, 2)
            self.assertEqual(report.read_text(encoding="utf-8"), "owner record")

    def test_missing_input_is_invalid_and_creates_no_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "demo"
            with redirect_stderr(StringIO()):
                self.assertEqual(main(["demo", "--examples", str(Path(tmp) / "missing"), "--output", str(output)]), 2)
            self.assertFalse(output.exists())
            with redirect_stdout(StringIO()) as out:
                code = main(["analyse", str(Path(tmp) / "missing")])
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(out.getvalue())["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
