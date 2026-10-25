"""Closed, bounded JSON and structural checks. No legal interpretation is performed."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any

MAX_JSON_BYTES = 262_144
MAX_INTEGER = 9_007_199_254_740_991
ID_RE = re.compile(r"[a-z][a-z0-9._-]{0,63}\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
TIME_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")


class InputError(ValueError):
    """An input is outside this intentionally small data language."""


def canonical_bytes(value: Any) -> bytes:
    """Deterministic encoding for this restricted JSON language, not general JCS."""
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode("ascii")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def issue(code: str, path: str, message: str, severity: str = "REVIEW") -> dict:
    return {"code": code, "path": path, "message": message, "severity": severity}


def _object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("Duplicate JSON object key.")
        result[key] = value
    return result


def _integer(value: str) -> int:
    if len(value.lstrip("-")) > 16:
        raise InputError("Integer exceeds the supported exact range.")
    result = int(value)
    if abs(result) > MAX_INTEGER:
        raise InputError("Integer exceeds the supported exact range.")
    return result


def _not_integer(_value: str) -> None:
    raise InputError("Only integer JSON numbers are supported.")


def parse_json(raw: bytes, max_bytes: int = MAX_JSON_BYTES) -> dict:
    if len(raw) > max_bytes:
        raise InputError("JSON document exceeds the size limit.")
    try:
        text = raw.decode("utf-8", errors="strict")
        result = json.loads(text, object_pairs_hook=_object, parse_int=_integer,
                            parse_float=_not_integer, parse_constant=_not_integer)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError("Invalid UTF-8 JSON document.") from exc
    if type(result) is not dict:
        raise InputError("Top-level JSON value must be an object.")
    stack = [(result, 0)]
    count = 0
    while stack:
        value, depth = stack.pop()
        count += 1
        if depth > 16 or count > 8192:
            raise InputError("JSON nesting or item count exceeds the limit.")
        if type(value) is str:
            if len(value) > 8192:
                raise InputError("JSON string exceeds the limit.")
            try:
                value.encode("utf-8", errors="strict")
            except UnicodeError as exc:
                raise InputError("Invalid Unicode scalar value.") from exc
        elif type(value) is dict:
            stack.extend((v, depth + 1) for v in value.values())
            stack.extend((k, depth + 1) for k in value)
        elif type(value) is list:
            stack.extend((v, depth + 1) for v in value)
    return result


def timestamp(value: Any) -> datetime | None:
    if type(value) is not str or not TIME_RE.fullmatch(value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def is_id(value: Any) -> bool:
    return type(value) is str and bool(ID_RE.fullmatch(value))


def is_int(value: Any, minimum: int = 0, maximum: int = MAX_INTEGER) -> bool:
    return type(value) is int and minimum <= value <= maximum


def closed(value: Any, required: set[str], optional: set[str], path: str, findings: list) -> bool:
    if type(value) is not dict:
        findings.append(issue("EXPECTED_OBJECT", path, "Expected a JSON object.", "ERROR"))
        return False
    if set(value) - required - optional:
        findings.append(issue("UNKNOWN_FIELD", path, "Unsupported fields are present.", "ERROR"))
    if required - set(value):
        findings.append(issue("MISSING_FIELD", path, "Required fields are missing.", "ERROR"))
    return True


def _id(value: Any, path: str, findings: list) -> None:
    if not is_id(value):
        findings.append(issue("INVALID_IDENTIFIER", path, "Use a bounded lowercase identifier.", "ERROR"))


def _text(value: Any, path: str, findings: list, maximum: int = 512) -> None:
    if type(value) is not str or not value.strip() or len(value) > maximum:
        findings.append(issue("INVALID_TEXT", path, "A nonempty bounded string is required.", "ERROR"))


def compile_contract(contract: dict) -> dict:
    """Compile explicitly typed duties; prose is retained as untrusted uninterpreted data."""
    findings: list[dict] = []
    graph = {"nodes": [], "edges": []}
    required = {"schema_version", "contract_id", "parties", "formed_at", "currency", "price_minor", "policy", "obligations"}
    if not closed(contract, required, {"mandate_ids", "prose"}, "contract", findings):
        return {"schema_valid": False, "ready_for_checks": False, "findings": findings, "graph": graph}
    if contract.get("schema_version") != "piepowder.contract/0.1":
        findings.append(issue("UNSUPPORTED_SCHEMA", "contract.schema_version", "Expected piepowder.contract/0.1.", "ERROR"))
    _id(contract.get("contract_id"), "contract.contract_id", findings)
    formed = timestamp(contract.get("formed_at"))
    if formed is None:
        findings.append(issue("INVALID_TIMESTAMP", "contract.formed_at", "A UTC second-resolution timestamp is required.", "ERROR"))
    currency = contract.get("currency")
    if type(currency) is not str or not re.fullmatch(r"[A-Z]{3}", currency):
        findings.append(issue("INVALID_CURRENCY", "contract.currency", "Use an explicit three-letter currency code.", "ERROR"))
    if not is_int(contract.get("price_minor"), 0, 10**12):
        findings.append(issue("INVALID_PRICE", "contract.price_minor", "Price must be a bounded nonnegative integer in minor units.", "ERROR"))
    policy = contract.get("policy")
    if closed(policy, {"policy_id", "version"}, set(), "contract.policy", findings):
        _id(policy.get("policy_id"), "contract.policy.policy_id", findings)
        _text(policy.get("version"), "contract.policy.version", findings, 64)
    parties = contract.get("parties")
    party_ids: set[str] = set()
    roles: list[str] = []
    agents: set[str] = set()
    if type(parties) is not list or len(parties) != 2:
        findings.append(issue("UNSUPPORTED_PARTIES", "contract.parties", "This sandbox requires exactly one buyer and one seller.", "ERROR"))
        parties = []
    for i, party in enumerate(parties):
        path = f"contract.parties[{i}]"
        if not closed(party, {"party_id", "role", "principal_name", "agent_id"}, set(), path, findings):
            continue
        _id(party.get("party_id"), path + ".party_id", findings)
        _id(party.get("agent_id"), path + ".agent_id", findings)
        _text(party.get("principal_name"), path + ".principal_name", findings)
        if party.get("role") not in ("buyer", "seller"):
            findings.append(issue("INVALID_ROLE", path + ".role", "Only buyer and seller roles are supported.", "ERROR"))
        else:
            roles.append(party["role"])
        for key, seen in (("party_id", party_ids), ("agent_id", agents)):
            value = party.get(key)
            if is_id(value):
                if value in seen:
                    findings.append(issue("DUPLICATE_IDENTIFIER", path + "." + key, "Party and agent identifiers must be unique within their kind.", "ERROR"))
                seen.add(value)
        if is_id(party.get("party_id")):
            graph["nodes"].append({"party_id": party["party_id"], "role": party.get("role")})
    if sorted(roles) != ["buyer", "seller"]:
        findings.append(issue("PARTY_ROLE_COVERAGE", "contract.parties", "Exactly one buyer and one seller must be named.", "ERROR"))
    mandate_ids = contract.get("mandate_ids")
    if mandate_ids is None or mandate_ids == []:
        findings.append(issue("MISSING_MANDATE", "contract.mandate_ids", "Each party must identify its recorded agent mandate."))
    elif type(mandate_ids) is not list or len(mandate_ids) != 2 or any(not is_id(x) for x in mandate_ids):
        findings.append(issue("INVALID_MANDATE_REFERENCE", "contract.mandate_ids", "Two valid mandate identifiers are required.", "ERROR"))
    elif len(set(mandate_ids)) != len(mandate_ids):
        findings.append(issue("DUPLICATE_MANDATE_REFERENCE", "contract.mandate_ids", "Mandate references must be unique.", "ERROR"))
    obligations = contract.get("obligations")
    if type(obligations) is not list or not 1 <= len(obligations) <= 16:
        findings.append(issue("INVALID_OBLIGATIONS", "contract.obligations", "Supply between one and sixteen typed duties.", "ERROR"))
        obligations = []
    seen_obligations = set()
    for i, obligation in enumerate(obligations):
        path = f"contract.obligations[{i}]"
        if not closed(obligation, {"obligation_id", "debtor", "creditor"}, {"trigger_at", "due_at", "acceptance"}, path, findings):
            continue
        _id(obligation.get("obligation_id"), path + ".obligation_id", findings)
        obligation_id = obligation.get("obligation_id")
        if is_id(obligation_id):
            if obligation_id in seen_obligations:
                findings.append(issue("DUPLICATE_OBLIGATION", path, "Obligation identifiers must be unique.", "ERROR"))
            seen_obligations.add(obligation_id)
        for key in ("debtor", "creditor"):
            if not is_id(obligation.get(key)) or obligation.get(key) not in party_ids:
                findings.append(issue("UNKNOWN_PARTY", path + "." + key, "Duty endpoints must name contract parties.", "ERROR"))
        if obligation.get("debtor") == obligation.get("creditor"):
            findings.append(issue("SELF_DUTY", path, "This sandbox requires distinct duty bearer and holder.", "ERROR"))
        times = {}
        for field, code in (("trigger_at", "MISSING_TRIGGER"), ("due_at", "MISSING_DEADLINE")):
            value = obligation.get(field)
            if value is None:
                findings.append(issue(code, path + "." + field, "The duty needs an explicit UTC trigger and deadline."))
            elif timestamp(value) is None:
                findings.append(issue("INVALID_TIMESTAMP", path + "." + field, "A UTC second-resolution timestamp is required.", "ERROR"))
            else:
                times[field] = timestamp(value)
        if len(times) == 2 and times["due_at"] < times["trigger_at"]:
            findings.append(issue("DEADLINE_PRECEDES_TRIGGER", path, "The stated deadline occurs before its trigger."))
        acceptance = obligation.get("acceptance")
        if acceptance is None:
            findings.append(issue("MISSING_ACCEPTANCE_TEST", path + ".acceptance", "No measurable acceptance test has been agreed."))
        elif closed(acceptance, {"kind", "evidence_id", "sample_size", "threshold_bps", "denominator", "max_flagged_bps"}, {"assessor_id"}, path + ".acceptance", findings):
            if acceptance.get("kind") != "geocode_accuracy":
                findings.append(issue("UNSUPPORTED_ACCEPTANCE_TEST", path + ".acceptance.kind", "Only the fixed geocode count check is supported."))
            _id(acceptance.get("evidence_id"), path + ".acceptance.evidence_id", findings)
            assessor = acceptance.get("assessor_id")
            if assessor is None:
                findings.append(issue("MISSING_ASSESSOR", path + ".acceptance.assessor_id", "The acceptance test must name its assessor."))
            elif assessor != "offline-deterministic":
                findings.append(issue("UNSUPPORTED_ASSESSOR", path + ".acceptance.assessor_id", "The named assessor cannot be run by this offline engine."))
            for key, low, high in (("sample_size", 1, 1_000_000), ("threshold_bps", 0, 10_000), ("max_flagged_bps", 0, 10_000)):
                if not is_int(acceptance.get(key), low, high):
                    findings.append(issue("INVALID_ACCEPTANCE_NUMBER", path + ".acceptance." + key, "Acceptance numbers must be integers within their stated range.", "ERROR"))
            denominator = acceptance.get("denominator")
            if denominator not in ("unspecified", "all_sampled", "exclude_flagged"):
                findings.append(issue("INVALID_DENOMINATOR", path + ".acceptance.denominator", "Choose a supported denominator policy.", "ERROR"))
            elif denominator == "unspecified":
                findings.append(issue("AMBIGUOUS_DENOMINATOR", path + ".acceptance.denominator", "The parties have not agreed whether flagged records count in the denominator."))
        graph["edges"].append({"kind": "duty", "obligation_id": obligation_id,
                               "bearer": obligation.get("debtor"), "holder": obligation.get("creditor"),
                               "trigger_at": obligation.get("trigger_at"), "due_at": obligation.get("due_at"),
                               "acceptance_kind": acceptance.get("kind") if type(acceptance) is dict else None})
    prose = contract.get("prose", "")
    if type(prose) is not str or len(prose) > 8192:
        findings.append(issue("INVALID_PROSE", "contract.prose", "Prose must be a bounded string.", "ERROR"))
    elif prose:
        findings.append(issue("PROSE_NOT_INTERPRETED", "contract.prose", "Prose is stored as data; this compiler does not resolve its legal meaning.", "INFO"))
        if any(term in prose.lower() for term in ("reasonable", "best efforts", "clean data", "high quality", "timely", "appropriate")):
            findings.append(issue("VAGUE_LANGUAGE_INDICATOR", "contract.prose", "A simple wording heuristic found language requiring human interpretation; this is not a model ambiguity score.", "INFO"))
    return {"schema_valid": not any(x["severity"] == "ERROR" for x in findings),
            "ready_for_checks": not any(x["severity"] in ("ERROR", "REVIEW") for x in findings),
            "findings": findings, "graph": graph}


def validate_policy(policy: dict, contract: dict) -> list[dict]:
    findings: list[dict] = []
    required = {"schema_version", "policy_id", "version", "automatic_legal_effects", "default_acceptance", "timeout_consequence"}
    if not closed(policy, required, set(), "policy", findings):
        return findings
    if policy.get("schema_version") != "piepowder.policy/0.1":
        findings.append(issue("UNSUPPORTED_SCHEMA", "policy.schema_version", "Expected piepowder.policy/0.1.", "ERROR"))
    expected = contract.get("policy")
    if type(expected) is not dict or policy.get("policy_id") != expected.get("policy_id") or policy.get("version") != expected.get("version"):
        findings.append(issue("POLICY_MISMATCH", "policy", "The supplied policy does not match the exact policy reference in the contract.", "ERROR"))
    if policy.get("automatic_legal_effects") is not False or policy.get("default_acceptance") != "none" or policy.get("timeout_consequence") != "human_review":
        findings.append(issue("UNSUPPORTED_POLICY", "policy", "This sandbox permits no automatic legal effects, default acceptance or timeout disposition.", "ERROR"))
    return findings


def check_mandates(contract: dict, document: dict) -> dict:
    findings: list[dict] = []
    checks: list[dict] = []
    if not closed(document, {"schema_version", "mandates"}, set(), "mandates", findings):
        return {"findings": findings, "checks": checks}
    if document.get("schema_version") != "piepowder.mandates/0.1":
        findings.append(issue("UNSUPPORTED_SCHEMA", "mandates.schema_version", "Expected piepowder.mandates/0.1.", "ERROR"))
    mandates = document.get("mandates")
    if type(mandates) is not list or len(mandates) > 16:
        findings.append(issue("INVALID_MANDATES", "mandates.mandates", "A bounded list of recorded mandates is required.", "ERROR"))
        return {"findings": findings, "checks": checks}
    by_id = {}
    required = {"mandate_id", "principal_party_id", "agent_id", "valid_from", "valid_until", "revoked_at", "currency", "maximum_price_minor", "allowed_counterparties", "allowed_actions", "authority_basis"}
    for i, mandate in enumerate(mandates):
        path = f"mandates.mandates[{i}]"
        if not closed(mandate, required, set(), path, findings):
            continue
        for key in ("mandate_id", "principal_party_id", "agent_id"):
            _id(mandate.get(key), path + "." + key, findings)
        identifier = mandate.get("mandate_id")
        if is_id(identifier):
            if identifier in by_id:
                findings.append(issue("DUPLICATE_MANDATE", path, "Mandate identifiers must be unique.", "ERROR"))
            by_id[identifier] = mandate
        for key in ("valid_from", "valid_until"):
            if timestamp(mandate.get(key)) is None:
                findings.append(issue("INVALID_TIMESTAMP", path + "." + key, "Recorded mandate validity requires UTC timestamps.", "ERROR"))
        start, end = timestamp(mandate.get("valid_from")), timestamp(mandate.get("valid_until"))
        if start is not None and end is not None and end <= start:
            findings.append(issue("INVALID_MANDATE_INTERVAL", path, "The mandate validity interval must be nonempty.", "ERROR"))
        if mandate.get("revoked_at") is not None and timestamp(mandate.get("revoked_at")) is None:
            findings.append(issue("INVALID_TIMESTAMP", path + ".revoked_at", "Revocation must be a UTC timestamp or null.", "ERROR"))
        if mandate.get("authority_basis") != "recorded_claim":
            findings.append(issue("UNSUPPORTED_AUTHORITY_CLAIM", path + ".authority_basis", "This engine cannot verify signatures or independent principal authority.", "ERROR"))
        if type(mandate.get("currency")) is not str or not re.fullmatch(r"[A-Z]{3}", mandate["currency"]):
            findings.append(issue("INVALID_CURRENCY", path + ".currency", "An explicit currency is required.", "ERROR"))
        if not is_int(mandate.get("maximum_price_minor"), 0, 10**12):
            findings.append(issue("INVALID_MANDATE_LIMIT", path + ".maximum_price_minor", "The limit must be an integer in currency minor units.", "ERROR"))
        counterparties = mandate.get("allowed_counterparties")
        if type(counterparties) is not list or not 1 <= len(counterparties) <= 16 or any(not is_id(x) for x in counterparties) or len(set(counterparties)) != len(counterparties):
            findings.append(issue("INVALID_COUNTERPARTIES", path + ".allowed_counterparties", "Supply a bounded list of distinct counterparty identifiers.", "ERROR"))
        actions = mandate.get("allowed_actions")
        supported_actions = {"form_contract", "deliver", "submit_evidence", "file_dispute"}
        if type(actions) is not list or not 1 <= len(actions) <= 4 or any(type(x) is not str or x not in supported_actions for x in actions) or len(set(actions)) != len(actions):
            findings.append(issue("INVALID_ACTIONS", path + ".allowed_actions", "Only explicitly supported mandate actions are accepted.", "ERROR"))
    if any(x["severity"] == "ERROR" for x in findings):
        return {"findings": findings, "checks": checks}
    references = contract.get("mandate_ids")
    if type(references) is not list or not references:
        findings.append(issue("MISSING_MANDATE", "contract.mandate_ids", "No complete set of mandate references was supplied."))
        return {"findings": findings, "checks": checks}
    if set(by_id) != set(references):
        findings.append(issue("MANDATE_REFERENCE_MISMATCH", "mandates", "Supplied mandates must exactly match the contract's mandate references."))
    formed = timestamp(contract.get("formed_at"))
    parties = contract.get("parties", [])
    party_ids = {p["party_id"] for p in parties}
    for party in parties:
        candidates = [by_id[key] for key in references if key in by_id and by_id[key]["principal_party_id"] == party["party_id"]]
        codes = []
        if len(candidates) != 1:
            codes.append("MANDATE_PARTY_COVERAGE")
        else:
            mandate = candidates[0]
            if mandate["agent_id"] != party["agent_id"]:
                codes.append("MANDATE_AGENT_MISMATCH")
            if formed is None or not timestamp(mandate["valid_from"]) <= formed < timestamp(mandate["valid_until"]):
                codes.append("MANDATE_OUTSIDE_VALIDITY")
            revoked = timestamp(mandate["revoked_at"])
            if revoked is not None and formed is not None and revoked <= formed:
                codes.append("MANDATE_RECORDED_REVOKED")
            if mandate["currency"] != contract.get("currency") or mandate["maximum_price_minor"] < contract.get("price_minor", 0):
                codes.append("MANDATE_VALUE_OUTSIDE_SCOPE")
            if not party_ids.difference({party["party_id"]}).issubset(mandate["allowed_counterparties"]):
                codes.append("MANDATE_COUNTERPARTY_OUTSIDE_SCOPE")
            if "form_contract" not in mandate["allowed_actions"]:
                codes.append("MANDATE_ACTION_OUTSIDE_SCOPE")
        checks.append({"check_id": "mandate-" + party["party_id"], "obligation_id": None,
                       "kind": "recorded_mandate_scope", "result": "SATISFIED" if not codes else "UNKNOWN",
                       "reason_codes": codes, "metrics": {"party_id": party["party_id"], "action": "form_contract",
                                                            "at": contract.get("formed_at"), "authority_verified": False}})
        findings.extend(issue(code, "mandates", "Recorded mandate scope is incomplete or does not cover the stated contract; independent authority remains unverified.") for code in codes)
    return {"findings": findings, "checks": checks}
