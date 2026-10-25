"""Deterministic record review. Results never authorise work, money or legal relief."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from . import __version__
from .contracts import (InputError, canonical_bytes, check_mandates, closed,
                        compile_contract, digest, is_id, issue, parse_json,
                        timestamp, validate_policy)
from .evidence import read_case_bytes, verify_evidence

ARTIFACTS = ("case.json", "contract.json", "mandates.json", "policy.json", "evidence.json")
AGREED_ARTIFACTS = ("contract.json", "mandates.json", "policy.json")


def _result() -> dict:
    return {"schema_version": "piepowder.analysis/0.1", "engine_version": __version__,
            "case_id": None, "status": "INVALID", "reasons": [], "lint": [],
            "contract_graph": {"nodes": [], "edges": []}, "checks": [],
            "evidence": {"status": "NOT_RUN", "findings": [], "items": [], "authenticity": "UNVERIFIED"},
            "bindings": {"agreement_sha256": None, "dossier_sha256": None, "artifact_sha256": {}},
            "assurance": {"identity": "UNVERIFIED", "authority": "UNVERIFIED", "signatures": "NOT_VERIFIED",
                          "timestamps": "RECORDED_ASSERTIONS_ONLY", "sample_method_and_truth": "NOT_VERIFIED",
                          "external_append_only": "NOT_ESTABLISHED", "per_event_delegation": "NOT_CHECKED",
                          "model_panels": "NOT_IMPLEMENTED", "legal_effect": "NONE"},
            "work_allowed": False, "payment_authorised": False}


def _finish(result: dict, findings: list[dict]) -> dict:
    result["reasons"] = [finding for finding in findings if finding["severity"] in ("ERROR", "REVIEW")]
    if any(finding["severity"] == "ERROR" for finding in findings):
        result["status"] = "INVALID"
    elif result["reasons"] or any(check["result"] != "SATISFIED" for check in result["checks"]):
        result["status"] = "HUMAN_REVIEW"
    else:
        result["status"] = "CHECKS_COMPLETE"
    evidence_binding = [{"evidence_id": item["evidence_id"], "recorded_sha256": item["recorded_sha256"],
                         "observed_sha256": item["observed_sha256"], "byte_status": item["byte_status"]}
                        for item in result["evidence"]["items"]]
    result["bindings"]["dossier_sha256"] = digest(canonical_bytes({
        "schema_version": "piepowder.dossier-binding/0.1",
        "artifact_sha256": result["bindings"]["artifact_sha256"],
        "observed_evidence": evidence_binding,
    }))
    return result


def _case_findings(case: dict) -> list[dict]:
    findings: list[dict] = []
    if not closed(case, {"schema_version", "case_id", "contested_evidence_ids", "contested_obligation_ids"}, set(), "case", findings):
        return findings
    if case.get("schema_version") != "piepowder.case/0.1":
        findings.append(issue("UNSUPPORTED_SCHEMA", "case.schema_version", "Expected piepowder.case/0.1.", "ERROR"))
    if not is_id(case.get("case_id")):
        findings.append(issue("INVALID_CASE_ID", "case.case_id", "A valid case identifier is required.", "ERROR"))
    for field in ("contested_evidence_ids", "contested_obligation_ids"):
        values = case.get(field)
        if type(values) is not list or len(values) > 32 or any(not is_id(value) for value in values) or len(set(values)) != len(values):
            findings.append(issue("INVALID_CONTEST_REFERENCE", "case." + field, "Use a bounded list of distinct record identifiers.", "ERROR"))
        elif values:
            findings.append(issue("CONTESTED_RECORD", "case." + field, "The record includes an explicit contest requiring human review."))
    return findings


def _fraction(numerator: int, denominator: int, threshold_bps: int) -> dict:
    return {"numerator": numerator, "denominator": denominator,
            "percentage": None if denominator == 0 else format(Decimal(numerator) * 100 / Decimal(denominator), ".6f"),
            "threshold_satisfied": None if denominator == 0 else numerator * 10_000 >= threshold_bps * denominator}


def _quality_check(obligation: dict, entries: list[dict], case: dict) -> dict:
    identifier = obligation["obligation_id"]
    check = {"check_id": "quality-" + identifier, "obligation_id": identifier, "kind": "geocode_accuracy",
             "result": "UNKNOWN", "reason_codes": [], "metrics": {}}
    acceptance = obligation.get("acceptance")
    if type(acceptance) is not dict:
        check["reason_codes"].append("MISSING_ACCEPTANCE_TEST")
        return check
    if acceptance.get("kind") != "geocode_accuracy" or acceptance.get("assessor_id") != "offline-deterministic":
        check["result"] = "NOT_RUN"
        check["reason_codes"].append("UNSUPPORTED_OR_MISSING_ASSESSOR")
        return check
    primary = next((entry for entry in entries if entry["evidence_id"] == acceptance["evidence_id"]), None)
    associated = [entry for entry in entries if entry["obligation_id"] == identifier and entry["kind"] == "geocode_sample"]
    if primary is None or primary["obligation_id"] != identifier or primary["kind"] != "geocode_sample":
        check["reason_codes"].append("MISSING_OR_MISASSIGNED_SAMPLE")
        return check
    if primary["byte_status"] != "MATCH" or primary["data"] is None:
        check["reason_codes"].append("SAMPLE_UNAVAILABLE_OR_UNVERIFIED")
        return check
    data = primary["data"]
    sample_size = data["sample_size"]
    correct = data["correct"]
    flagged = data["flagged_unresolvable"]
    readings = {"all_sampled": _fraction(correct, sample_size, acceptance["threshold_bps"]),
                "exclude_flagged": _fraction(correct, sample_size - flagged, acceptance["threshold_bps"])}
    within_flag_limit = flagged * 10_000 <= acceptance["max_flagged_bps"] * sample_size
    selected = acceptance["denominator"]
    check["metrics"] = {"selected_denominator": selected, "threshold_bps": acceptance["threshold_bps"],
                        "max_flagged_bps": acceptance["max_flagged_bps"], "sample_size": sample_size,
                        "correct": correct, "incorrect": data["incorrect"], "flagged_unresolvable": flagged,
                        "readings": readings, "flagged_rate_within_limit": within_flag_limit,
                        "counts_are_recorded_assertions": True}
    if sample_size != acceptance["sample_size"]:
        check["reason_codes"].append("AGREED_SAMPLE_SIZE_MISMATCH")
    if identifier in case["contested_obligation_ids"] or any(entry["evidence_id"] in case["contested_evidence_ids"] for entry in associated):
        check["reason_codes"].append("CONTESTED_RECORD")
    if any(entry["byte_status"] != "MATCH" or entry["data"] is None for entry in associated):
        check["reason_codes"].append("UNRESOLVED_ASSOCIATED_EVIDENCE")
    if any(entry["data"] is not None and entry["data"] != data for entry in associated):
        check["reason_codes"].append("CONFLICTING_SUBMISSIONS")
    if selected == "unspecified":
        check["reason_codes"].append("AMBIGUOUS_DENOMINATOR")
    elif readings[selected]["denominator"] == 0:
        check["reason_codes"].append("ZERO_DENOMINATOR")
    if not check["reason_codes"]:
        check["result"] = "SATISFIED" if readings[selected]["threshold_satisfied"] and within_flag_limit else "NOT_SATISFIED"
        if not readings[selected]["threshold_satisfied"]:
            check["reason_codes"].append("RECORDED_ACCURACY_BELOW_THRESHOLD")
        if not within_flag_limit:
            check["reason_codes"].append("RECORDED_FLAG_RATE_ABOVE_LIMIT")
    return check


def _time_check(obligation: dict, entries: list[dict]) -> dict:
    check = {"check_id": "time-" + obligation["obligation_id"], "obligation_id": obligation["obligation_id"],
             "kind": "recorded_submission_window", "result": "UNKNOWN", "reason_codes": [], "metrics": {
                 "basis": "Comparison of recorded assertions only; does not establish actual delivery time.",
                 "timestamp_authenticity": "UNVERIFIED", "trigger_at": obligation.get("trigger_at"), "due_at": obligation.get("due_at")}}
    acceptance = obligation.get("acceptance")
    identifier = acceptance.get("evidence_id") if type(acceptance) is dict else None
    entry = next((item for item in entries if item["evidence_id"] == identifier), None)
    start, end = timestamp(obligation.get("trigger_at")), timestamp(obligation.get("due_at"))
    if entry is None or entry["byte_status"] != "MATCH":
        check["reason_codes"].append("NO_VERIFIED_SUBMISSION_BYTES")
    elif start is None or end is None or start > end:
        check["reason_codes"].append("INCOMPLETE_OR_INCONSISTENT_WINDOW")
    else:
        recorded = timestamp(entry["recorded_at"])
        check["metrics"]["recorded_at"] = entry["recorded_at"]
        within = start <= recorded <= end
        check["metrics"]["recorded_time_within_window"] = within
        check["result"] = "SATISFIED" if within else "NOT_SATISFIED"
        if not within:
            check["reason_codes"].append("RECORDED_TIME_OUTSIDE_WINDOW")
    return check


def analyse_case(case_dir: Path) -> dict:
    """Read a fixed set of case artifacts and return reproducible non-operative findings."""
    result = _result()
    findings: list[dict] = []
    documents = {}
    for filename in ARTIFACTS:
        try:
            raw, _identity = read_case_bytes(Path(case_dir), filename)
            result["bindings"]["artifact_sha256"][filename] = digest(raw)
            documents[filename] = parse_json(raw)
        except (OSError, InputError, ValueError):
            findings.append(issue("CASE_ARTIFACT_UNAVAILABLE_OR_INVALID", filename, "A required local artifact is missing, unsafe, oversized or invalid bounded JSON.", "ERROR"))
    artifact_hashes = result["bindings"]["artifact_sha256"]
    if all(name in artifact_hashes for name in AGREED_ARTIFACTS):
        result["bindings"]["agreement_sha256"] = digest(canonical_bytes({
            "schema_version": "piepowder.agreement-binding/0.1",
            "artifact_sha256": {name: artifact_hashes[name] for name in AGREED_ARTIFACTS},
        }))
    if len(documents) != len(ARTIFACTS):
        return _finish(result, findings)
    case = documents["case.json"]
    contract = documents["contract.json"]
    findings.extend(_case_findings(case))
    if is_id(case.get("case_id")):
        result["case_id"] = case["case_id"]
    compiled = compile_contract(contract)
    result["lint"] = compiled["findings"]
    result["contract_graph"] = compiled["graph"]
    findings.extend(compiled["findings"])
    findings.extend(validate_policy(documents["policy.json"], contract))
    if any(finding["severity"] == "ERROR" for finding in findings):
        return _finish(result, findings)
    mandates = check_mandates(contract, documents["mandates.json"])
    findings.extend(mandates["findings"])
    result["checks"].extend(mandates["checks"])
    verified = verify_evidence(Path(case_dir), documents["evidence.json"])
    result["evidence"] = verified
    findings.extend(verified["findings"])
    if documents["evidence.json"].get("case_id") != case["case_id"]:
        findings.append(issue("EVIDENCE_CASE_MISMATCH", "evidence.case_id", "The evidence manifest belongs to a different case.", "ERROR"))
    if verified["status"] == "INVALID":
        return _finish(result, findings)
    evidence_ids = {item["evidence_id"] for item in verified["items"]}
    obligation_ids = {obligation["obligation_id"] for obligation in contract["obligations"]}
    party_ids = {party["party_id"] for party in contract["parties"]}
    if not set(case["contested_evidence_ids"]).issubset(evidence_ids) or not set(case["contested_obligation_ids"]).issubset(obligation_ids):
        findings.append(issue("UNKNOWN_CONTEST_REFERENCE", "case", "Contested identifiers must exist in this case record.", "ERROR"))
    for item in verified["items"]:
        if item["submitted_by"] not in party_ids:
            findings.append(issue("UNKNOWN_EVIDENCE_SUBMITTER", "evidence", "Every recorded submitter must be a named contract party.", "ERROR"))
        if item["obligation_id"] is not None and item["obligation_id"] not in obligation_ids:
            findings.append(issue("UNKNOWN_EVIDENCE_OBLIGATION", "evidence", "Evidence must refer to an existing duty.", "ERROR"))
    if any(finding["severity"] == "ERROR" for finding in findings):
        return _finish(result, findings)
    for obligation in contract["obligations"]:
        for check in (_quality_check(obligation, verified["items"], case), _time_check(obligation, verified["items"])):
            result["checks"].append(check)
            findings.extend(issue(code, "checks." + check["check_id"], "The deterministic record check needs human review; it does not establish liability or authorise payment.") for code in check["reason_codes"])
    return _finish(result, findings)
