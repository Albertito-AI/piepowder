"""A local, non-binding docket simulator. Actor names are unverified labels.

The hash chain checks consistency against retained checkpoints. It is not a
signature service, trusted clock, immutable store or proof that notice arrived.
No transition can authorise work, payment, a settlement or an arbitral award.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import re


class DocketError(ValueError):
    """Malformed or impermissible local simulation event."""


def _text(value, label, maximum=4000):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise DocketError(f"{label} must be non-empty text of at most {maximum} characters")
    return value


def _digest(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise DocketError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _instant(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise DocketError("timestamps must use whole-second UTC YYYY-MM-DDTHH:MM:SSZ")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise DocketError("invalid timestamp") from exc


def _hash(value):
    try:
        content = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError, RecursionError) as exc:
        raise DocketError("event is not bounded JSON data") from exc
    if len(content) > 2_000_000:
        raise DocketError("docket JSON exceeds the local limit")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def new_docket(case_id, agreement_sha256, claimant_id, respondent_id,
               answer_due_at, known_evidence):
    """Create a synthetic record; supplied identity, authority and time are claims."""
    header = {
        "schema_version": "piepowder.docket/0.1",
        "case_id": case_id,
        "agreement_sha256": agreement_sha256,
        "claimant_id": claimant_id,
        "respondent_id": respondent_id,
        "answer_due_at": answer_due_at,
        "known_evidence": deepcopy(known_evidence),
        "mode": "synthetic_local_simulation",
    }
    _validate_header(header)
    return {"header": header, "events": []}


def _validate_header(h):
    required = {"schema_version", "case_id", "agreement_sha256", "claimant_id", "respondent_id", "answer_due_at", "known_evidence", "mode"}
    if not isinstance(h, dict) or set(h) != required:
        raise DocketError("invalid docket header fields")
    if h["schema_version"] != "piepowder.docket/0.1" or h["mode"] != "synthetic_local_simulation":
        raise DocketError("unsupported docket version or mode")
    for key in ("case_id", "claimant_id", "respondent_id"):
        _text(h[key], key, 160)
    parties = {h["claimant_id"], h["respondent_id"]}
    if len(parties) != 2 or parties & {"case_manager", "engine"}:
        raise DocketError("two distinct party labels are required")
    _digest(h["agreement_sha256"], "agreement_sha256")
    _instant(h["answer_due_at"])
    evidence = h["known_evidence"]
    if not isinstance(evidence, dict) or len(evidence) > 200:
        raise DocketError("invalid evidence index")
    for evidence_id, item in evidence.items():
        _text(evidence_id, "evidence ID", 160)
        if not isinstance(item, dict) or set(item) != {"sha256", "submitted_by"}:
            raise DocketError("invalid evidence index item")
        _digest(item["sha256"], "evidence digest")
        if not isinstance(item["submitted_by"], str) or item["submitted_by"] not in parties:
            raise DocketError("evidence submitter must be a recorded party")


def _projection():
    return {"phase": "DRAFT", "requires_human_review": False, "admitted_evidence_ids": [],
            "assessment_sha256": None, "assessment_status": None, "notice_verified": False,
            "authority_verified": False, "work_allowed": False, "payment_authorised": False,
            "legal_effect": "none", "flags": []}


def _apply(h, p, event):
    if not isinstance(event, dict) or set(event) != {"event_id", "kind", "actor_id", "at", "data"}:
        raise DocketError("invalid event fields")
    _text(event["event_id"], "event_id", 160)
    _text(event["kind"], "kind", 80)
    _text(event["actor_id"], "actor_id", 160)
    at = _instant(event["at"])
    data = event["data"]
    if not isinstance(data, dict):
        raise DocketError("event data must be an object")
    kind, actor, phase = event["kind"], event["actor_id"], p["phase"]
    parties = {h["claimant_id"], h["respondent_id"]}

    def require(condition, message):
        if not condition:
            raise DocketError(message)

    if kind == "FILE":
        require(phase == "DRAFT" and actor == h["claimant_id"], "only the claimant label may file a new case")
        require(set(data) == {"notice_recorded_to"}, "FILE needs the recorded notice recipients")
        recipients = data["notice_recorded_to"]
        require(isinstance(recipients, list) and all(isinstance(x, str) for x in recipients)
                and len(recipients) == 2 and set(recipients) == parties, "record notices to both principals")
        p["phase"] = "FILED"
    elif kind == "ANSWER":
        require(phase == "FILED" and actor == h["respondent_id"], "only respondent may answer a filed case")
        require(not data, "ANSWER has no payload")
        if at >= _instant(h["answer_due_at"]):
            p["requires_human_review"] = True
            p["flags"].append("LATE_ANSWER_RECORDED_WITHOUT_FORFEITURE")
        p["phase"] = "ANSWERED"
    elif kind == "TIMEOUT":
        require(phase == "FILED" and actor == "case_manager", "timeout applies to an unanswered case")
        require(not data and at >= _instant(h["answer_due_at"]), "response deadline has not elapsed")
        p["requires_human_review"] = True
        if "RESPONSE_TIMEOUT_REQUIRES_REVIEW" not in p["flags"]:
            p["flags"].append("RESPONSE_TIMEOUT_REQUIRES_REVIEW")
    elif kind == "ADD_EVIDENCE":
        require(phase in {"FILED", "ANSWERED"} and actor in parties, "evidence intake is closed or actor is unknown")
        require(set(data) == {"evidence_id"}, "ADD_EVIDENCE needs one indexed evidence ID")
        eid = _text(data["evidence_id"], "evidence_id", 160)
        require(eid in h["known_evidence"], "evidence must exist in the committed index")
        require(h["known_evidence"][eid]["submitted_by"] == actor, "submitter label mismatch")
        require(eid not in p["admitted_evidence_ids"], "evidence already admitted")
        p["admitted_evidence_ids"].append(eid)
    elif kind == "CLOSE_EVIDENCE":
        require(phase == "ANSWERED" and actor == "case_manager", "answer must be recorded before evidence closes")
        require(set(data) == {"acknowledged_by"}, "record both parties' claimed acknowledgements")
        acks = data["acknowledged_by"]
        require(isinstance(acks, list) and all(isinstance(x, str) for x in acks)
                and len(acks) == 2 and set(acks) == parties, "both party acknowledgements must be recorded")
        require(set(p["admitted_evidence_ids"]) == set(h["known_evidence"]), "indexed evidence remains unadmitted")
        p["phase"] = "EVIDENCE_CLOSED"
    elif kind == "REOPEN_EVIDENCE":
        require(phase in {"EVIDENCE_CLOSED", "REVIEW_READY", "HUMAN_REVIEW_PENDING"}
                and actor == "case_manager", "reopening requires a recorded case-manager action")
        require(set(data) == {"reason"}, "reopening needs a reason")
        _text(data["reason"], "reopening reason")
        p["phase"] = "ANSWERED"
        p["requires_human_review"] = True
        p["assessment_sha256"] = None
        p["assessment_status"] = None
        p["flags"].append("EVIDENCE_REOPENED_PRIOR_ASSESSMENT_SUPERSEDED")
    elif kind == "RECORD_ASSESSMENT":
        require(phase == "EVIDENCE_CLOSED" and actor == "engine", "assessment needs a closed record")
        require(set(data) == {"assessment_sha256", "status", "cited_evidence_ids"}, "invalid assessment reference")
        _digest(data["assessment_sha256"], "assessment digest")
        require(isinstance(data["status"], str) and data["status"] in {"INVALID", "HUMAN_REVIEW", "CHECKS_COMPLETE"}, "invalid assessment status")
        refs = data["cited_evidence_ids"]
        require(isinstance(refs, list) and all(isinstance(x, str) for x in refs)
                and len(refs) == len(set(refs)) and set(refs) <= set(p["admitted_evidence_ids"]), "assessment cites unavailable evidence")
        p["assessment_sha256"] = data["assessment_sha256"]
        p["assessment_status"] = data["status"]
        p["requires_human_review"] |= data["status"] != "CHECKS_COMPLETE"
        p["phase"] = "REVIEW_READY"
    elif kind == "REFER_HUMAN":
        require(phase in {"FILED", "ANSWERED", "EVIDENCE_CLOSED", "REVIEW_READY"}
                and actor == "case_manager", "invalid human-review referral")
        require(set(data) == {"reason"}, "referral needs a reason")
        _text(data["reason"], "referral reason")
        p["requires_human_review"] = True
        p["phase"] = "HUMAN_REVIEW_PENDING"
    elif kind == "CLOSE_SIMULATION":
        require(phase == "HUMAN_REVIEW_PENDING" and actor == "case_manager", "close only a referred simulation")
        require(set(data) == {"note"}, "closing a simulation requires a note")
        _text(data["note"], "closing note")
        p["phase"] = "CLOSED_IN_SIMULATION"
    else:
        raise DocketError(f"unsupported action {kind}; no awards, settlements or funds execution exist")


def verify_docket(docket, expected_final_hash=None):
    """Replay the history; optionally compare a checkpoint retained elsewhere."""
    if not isinstance(docket, dict) or set(docket) != {"header", "events"}:
        raise DocketError("invalid docket envelope")
    h, events = docket["header"], docket["events"]
    _validate_header(h)
    if not isinstance(events, list) or len(events) > 1000:
        raise DocketError("invalid event count")
    p, head, seen, previous_time = _projection(), _hash(h), set(), None
    for i, entry in enumerate(events, 1):
        if not isinstance(entry, dict) or set(entry) != {"sequence", "previous_hash", "event", "event_hash"}:
            raise DocketError("invalid log entry")
        if type(entry["sequence"]) is not int or entry["sequence"] != i or entry["previous_hash"] != head:
            raise DocketError("broken log sequence or previous hash")
        hash_payload = {k: entry[k] for k in ("sequence", "previous_hash", "event")}
        if entry["event_hash"] != _hash(hash_payload):
            raise DocketError("event digest mismatch")
        event = entry["event"]
        _apply(h, p, event)
        when = _instant(event["at"])
        if previous_time is not None and when < previous_time:
            raise DocketError("recorded time moved backwards")
        if event["event_id"] in seen:
            raise DocketError("event ID replay")
        seen.add(event["event_id"])
        previous_time, head = when, entry["event_hash"]
    if expected_final_hash is not None:
        _digest(expected_final_hash, "expected_final_hash")
        if head != expected_final_hash:
            raise DocketError("retained checkpoint mismatch")
    return {"schema_version": "piepowder.docket_projection/0.1", "case_id": h["case_id"],
            "head_sha256": head, "event_count": len(events), "checkpoint_compared": expected_final_hash is not None,
            "integrity": "internally_consistent", "timestamps_authenticated": False, **p}


def append_event(docket, event, expected_head):
    """Return a new history. Exact event retries are idempotent; conflicts fail."""
    current = verify_docket(docket)
    _digest(expected_head, "expected_head")
    if not isinstance(event, dict):
        raise DocketError("event must be an object")
    for entry in docket["events"]:
        if entry["event"].get("event_id") == event.get("event_id"):
            if entry["event"] == event:
                return deepcopy(docket)
            raise DocketError("conflicting retry of an event ID")
    if expected_head != current["head_sha256"]:
        raise DocketError("stale docket checkpoint")
    result = deepcopy(docket)
    entry = {"sequence": len(result["events"]) + 1, "previous_hash": current["head_sha256"], "event": deepcopy(event)}
    entry["event_hash"] = _hash(entry)
    result["events"].append(entry)
    verify_docket(result)
    return result
