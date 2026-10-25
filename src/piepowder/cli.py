"""Local commands. No network, external tools, model calls or payment operations."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys

from . import __version__
from .analysis import analyse_case
from .contracts import InputError, compile_contract, parse_json
from .docket import DocketError, append_event, new_docket, verify_docket
from .evidence import read_case_bytes
from .reporting import render_dashboard, render_markdown

EXAMPLE_NAMES = ("geocode-ambiguous", "geocode-explicit-pass", "geocode-explicit-fail",
                 "geocode-contested", "geocode-conflicting", "geocode-missing-evidence")


def json_text(value):
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n"


def _write_new(path, text):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def _read_document(path):
    path = Path(path)
    raw, _ = read_case_bytes(path.parent, path.name, max_bytes=2_000_000)
    return parse_json(raw, max_bytes=2_000_000)


def demonstration_docket(analysis):
    """Exercise procedural safeguards using fictional actor labels and times."""
    known = {item["evidence_id"]: {"sha256": item["observed_sha256"], "submitted_by": item["submitted_by"]}
             for item in analysis["evidence"]["items"] if item["byte_status"] == "MATCH"}
    docket = new_docket(analysis["case_id"], analysis["bindings"]["agreement_sha256"],
                        "seller", "buyer", "2026-01-05T12:00:00Z", known)
    actions = [("FILE", "seller", {"notice_recorded_to": ["seller", "buyer"]}),
               ("ANSWER", "buyer", {})]
    actions.extend(("ADD_EVIDENCE", item["submitted_by"], {"evidence_id": eid}) for eid, item in known.items())
    actions.extend([
        ("CLOSE_EVIDENCE", "case_manager", {"acknowledged_by": ["seller", "buyer"]}),
        ("RECORD_ASSESSMENT", "engine", {
            "assessment_sha256": hashlib.sha256(json_text(analysis).encode("utf-8")).hexdigest(),
            "status": analysis["status"], "cited_evidence_ids": list(known)}),
        ("REFER_HUMAN", "case_manager", {"reason": "The fictional parties have not agreed the denominator. No legal determination is made."}),
    ])
    start = datetime(2026, 1, 4, 12, tzinfo=timezone.utc)
    for i, (kind, actor, data) in enumerate(actions, 1):
        event = {"event_id": f"demo-event-{i}", "kind": kind, "actor_id": actor,
                 "at": (start + timedelta(seconds=i)).strftime("%Y-%m-%dT%H:%M:%SZ"), "data": data}
        docket = append_event(docket, event, verify_docket(docket)["head_sha256"])
    return docket


def run_demo(examples, output):
    examples, output = Path(examples), Path(output)
    if output.exists():
        raise FileExistsError("Demo output already exists; choose a new directory to preserve the earlier record.")
    results = [analyse_case(examples / name) for name in EXAMPLE_NAMES]
    if any(result["status"] == "INVALID" for result in results):
        raise InputError("A demonstration fixture is invalid or unavailable; no demo output was created.")
    docket = demonstration_docket(results[0])
    projection = verify_docket(docket)
    summary = {"schema_version": "piepowder.demo/0.1", "engine_version": __version__,
               "mode": "fictional_local_examples", "cases": [
                   {"case_id": result["case_id"], "status": result["status"],
                    "checks": [{"kind": check["kind"], "result": check["result"]} for check in result["checks"]],
                    "agreement_sha256": result["bindings"]["agreement_sha256"],
                    "dossier_sha256": result["bindings"]["dossier_sha256"]}
                   for result in results],
               "docket_head_sha256": projection["head_sha256"],
               "docket_phase": projection["phase"], "work_allowed": False, "payment_authorised": False}
    output.mkdir(parents=True, exist_ok=False)
    for result in results:
        _write_new(output / (result["case_id"] + ".json"), json_text(result))
        _write_new(output / (result["case_id"] + ".md"), render_markdown(result))
    _write_new(output / "dashboard.html", render_dashboard(results))
    _write_new(output / "docket.json", json_text(docket))
    _write_new(output / "docket-projection.json", json_text(projection))
    _write_new(output / "summary.json", json_text(summary))
    _write_new(output / "README.txt", "Piepowder fictional demonstration\n\nOpen dashboard.html locally to inspect the six computed cases.\nAll inputs, names, prices, times and procedural events are synthetic.\nThe report contains technical observations; it grants no authority, rights or payment instruction.\nThe hashes detect some changes only relative to a separately retained trusted checkpoint.\nNo evidence is sent over a network.\n")
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description="Piepowder local contract and evidence review")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    analyse = commands.add_parser("analyse", help="analyse one local case directory")
    analyse.add_argument("case_dir", type=Path)
    analyse.add_argument("--output", type=Path, help="write a new JSON report; existing files are preserved")
    compile_parser = commands.add_parser("compile", help="check a typed contract and generate its duty graph")
    compile_parser.add_argument("contract", type=Path)
    demo = commands.add_parser("demo", help="write six fictional analyses, a docket and a local HTML viewer")
    demo.add_argument("--output", type=Path, required=True)
    demo.add_argument("--examples", type=Path, default=Path(__file__).resolve().parents[2] / "examples")
    verify = commands.add_parser("verify-docket", help="replay a saved synthetic docket")
    verify.add_argument("file", type=Path)
    verify.add_argument("--expected-sha256", help="optional head digest retained independently from the docket")
    args = parser.parse_args(argv)
    try:
        if args.command == "analyse":
            result = analyse_case(args.case_dir)
            if args.output is not None:
                _write_new(args.output, json_text(result))
            else:
                print(json_text(result), end="")
            return 2 if result["status"] == "INVALID" else 0
        if args.command == "compile":
            result = compile_contract(_read_document(args.contract))
            print(json_text(result), end="")
            return 0 if result["schema_valid"] else 2
        if args.command == "demo":
            print(json_text(run_demo(args.examples, args.output)), end="")
            return 0
        if args.command == "verify-docket":
            print(json_text(verify_docket(_read_document(args.file), args.expected_sha256)), end="")
            return 0
    except (OSError, InputError, DocketError, ValueError) as exc:
        print(f"piepowder: {exc}", file=sys.stderr)
        return 2
    return 2
