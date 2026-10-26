"""Reproduce prelabelled fictional P02 cases. These are engineering assertions only."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from piepowder.analysis import analyse_case

ROOT = Path(__file__).resolve().parents[1]
LABELS = ROOT / "benchmarks" / "p02-labels.json"
EXAMPLES = ROOT / "examples"


def labelled_cases() -> list[dict]:
    data = json.loads(LABELS.read_text(encoding="utf-8"))
    if data["schema_version"] != "piepowder.p02-labelled-cases/0.1":
        raise ValueError("Unsupported P02 label file")
    cases = data["cases"]
    ids = [c["id"] for c in cases]
    if len(cases) < 24 or len(ids) != len(set(ids)):
        raise ValueError("Expected at least 24 distinct prelabelled cases")
    return cases


def _parent_at(document: object, pointer: str) -> tuple[object, str]:
    if not pointer.startswith("/"):
        raise ValueError("Only explicit JSON pointers are supported")
    parts = pointer.split("/")[1:]
    cursor = document
    for part in parts[:-1]:
        key = part.replace("~1", "/").replace("~0", "~")
        cursor = cursor[int(key)] if isinstance(cursor, list) else cursor[key]
    return cursor, parts[-1].replace("~1", "/").replace("~0", "~")


def materialise_case(spec: dict, dest: Path) -> None:
    """Create a distinct complete disposable case; never alter repository examples."""
    base = spec["base"]
    if base not in ("geocode-explicit-pass", "geocode-conflicting"):
        raise ValueError("Unapproved fixture base")
    shutil.copytree(EXAMPLES / base, dest)
    changed_sample_json = False
    for edit in spec["edits"]:
        relative = edit["file"]
        if relative not in ("case.json", "contract.json", "mandates.json", "policy.json",
                            "evidence.json", "evidence/sample.json"):
            raise ValueError("Unapproved fixture path")
        file = dest / relative
        op = edit["op"]
        if op == "remove_file":
            file.unlink()
        elif op == "append_bytes":
            with file.open("ab") as stream:
                stream.write(edit["suffix"].encode("utf-8"))
        elif op in ("set", "delete"):
            document = json.loads(file.read_text(encoding="utf-8"))
            parent, key = _parent_at(document, edit["pointer"])
            if op == "delete":
                if isinstance(parent, list):
                    del parent[int(key)]
                else:
                    del parent[key]
            elif isinstance(parent, list):
                parent[int(key)] = copy.deepcopy(edit["value"])
            else:
                parent[key] = copy.deepcopy(edit["value"])
            file.write_text(json.dumps(document, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
            changed_sample_json |= relative == "evidence/sample.json"
        else:
            raise ValueError("Unapproved fixture operation")
    if changed_sample_json:
        manifest = json.loads((dest / "evidence.json").read_text(encoding="utf-8"))
        primary = next(item for item in manifest["items"] if item["evidence_id"] == "sample-results")
        primary["sha256"] = hashlib.sha256((dest / "evidence/sample.json").read_bytes()).hexdigest()
        (dest / "evidence.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def evaluate(spec: dict) -> dict:
    with tempfile.TemporaryDirectory(prefix="piepowder-p02-") as tmp:
        folder = Path(tmp) / "case"
        materialise_case(spec, folder)
        result = analyse_case(folder)
    quality = next((check for check in result["checks"] if check["kind"] == "geocode_accuracy"), None)
    codes = {finding["code"] for finding in result["reasons"]}
    codes.update(finding["code"] for finding in result["lint"])
    codes.update(finding["code"] for finding in result["evidence"]["findings"])
    if quality:
        codes.update(quality["reason_codes"])
    actual = {"overall": result["status"], "quality": quality["result"] if quality else None}
    expected = spec["expected"]
    passed = (actual["overall"] == expected["overall"] and
              actual["quality"] == expected["quality"] and
              set(expected["reason_codes"]) <= codes and
              result["work_allowed"] is False and result["payment_authorised"] is False and
              result["assurance"]["identity"] == "UNVERIFIED")
    return {"id": spec["id"], "group": spec["group"], "pass": passed,
            "expected": expected, "actual": actual,
            "observed_reason_codes": sorted(codes),
            "work_allowed": result["work_allowed"],
            "payment_authorised": result["payment_authorised"]}


def run() -> dict:
    cases = labelled_cases()
    rows = [evaluate(spec) for spec in cases]
    return {"kind": "internal_prelabelled_fictional_P02_benchmark",
            "labels_sha256": hashlib.sha256(LABELS.read_bytes()).hexdigest(),
            "cases": len(rows), "passed": sum(row["pass"] for row in rows),
            "independent_human_first_use": "NOT_PERFORMED",
            "empirical_accuracy_or_efficiency": "NOT_MEASURED",
            "observations": rows}


if __name__ == "__main__":
    import sys
    report = run()
    print(json.dumps(report, indent=2, ensure_ascii=True))
    sys.exit(0 if report["passed"] == report["cases"] else 1)
