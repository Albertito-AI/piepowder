"""Read bounded local evidence and check bytes without claiming authenticity."""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path

from .contracts import (InputError, MAX_JSON_BYTES, SHA256_RE, closed, digest,
                        is_id, is_int, issue, parse_json, timestamp)

MAX_EVIDENCE_BYTES = 2_097_152
MAX_ITEMS = 32
_PATH_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,199}\Z")
_RESERVED = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}


def portable_path(value: object) -> bool:
    if type(value) is not str or not _PATH_RE.fullmatch(value):
        return False
    parts = value.split("/")
    return all(part not in ("", ".", "..") and not part.endswith((".", " "))
               and part.split(".")[0].upper() not in _RESERVED for part in parts)


def _link_or_reparse(metadata: os.stat_result) -> bool:
    return stat.S_ISLNK(metadata.st_mode) or bool(getattr(metadata, "st_file_attributes", 0) & 0x400)


def read_case_bytes(case_dir: Path, relative: str, max_bytes: int = MAX_JSON_BYTES) -> tuple[bytes, tuple[int, int]]:
    """Reject escaping paths and links; verify the opened inode before reading it.

    This is a local snapshot reader, not a trusted vault or concurrent filesystem
    transaction. The result binds the bytes actually read. It never follows a
    submitted URL or executes a file.
    """
    if not portable_path(relative):
        raise InputError("Unsafe or unsupported relative path.")
    case_dir = Path(case_dir)
    root_stat = case_dir.lstat()
    if _link_or_reparse(root_stat) or not stat.S_ISDIR(root_stat.st_mode):
        raise InputError("Case root must be a real directory, not a link.")
    root = case_dir.resolve(strict=True)
    target = root
    parts = relative.split("/")
    checked = None
    for index, part in enumerate(parts):
        target = target / part
        checked = target.lstat()
        if _link_or_reparse(checked):
            raise InputError("Symlinks and filesystem reparse points are unsupported.")
        if index < len(parts) - 1 and not stat.S_ISDIR(checked.st_mode):
            raise InputError("Evidence parent is not a directory.")
    if checked is None or not stat.S_ISREG(checked.st_mode):
        raise InputError("Only regular evidence files are supported.")
    if checked.st_size > max_bytes:
        raise InputError("File exceeds the size limit.")
    if not target.resolve(strict=True).is_relative_to(root):
        raise InputError("File is outside the case directory.")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(target, flags)
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (checked.st_dev, checked.st_ino):
            raise InputError("File changed between path inspection and open.")
        if opened.st_size > max_bytes:
            raise InputError("File exceeds the size limit.")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            raw = stream.read(max_bytes + 1)
            after = os.fstat(stream.fileno())
        if len(raw) > max_bytes:
            raise InputError("File exceeds the size limit.")
        if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns) or len(raw) != after.st_size:
            raise InputError("File changed while it was read.")
        return raw, (opened.st_dev, opened.st_ino)
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def validate_sample(document: dict) -> list[dict]:
    findings: list[dict] = []
    fields = {"schema_version", "sample_size", "correct", "incorrect", "flagged_unresolvable"}
    if not closed(document, fields, set(), "sample", findings):
        return findings
    if document.get("schema_version") != "piepowder.geocode-sample/0.1":
        findings.append(issue("UNSUPPORTED_SAMPLE_SCHEMA", "sample.schema_version", "Expected piepowder.geocode-sample/0.1.", "ERROR"))
    for field in ("sample_size", "correct", "incorrect", "flagged_unresolvable"):
        if not is_int(document.get(field), 1 if field == "sample_size" else 0, 1_000_000):
            findings.append(issue("INVALID_SAMPLE_COUNT", "sample." + field, "Counts must be bounded integers; booleans and floats are not counts.", "ERROR"))
    if not findings and document["correct"] + document["incorrect"] + document["flagged_unresolvable"] != document["sample_size"]:
        findings.append(issue("SAMPLE_TOTAL_MISMATCH", "sample", "Correct, incorrect and flagged counts must sum to sample_size.", "ERROR"))
    return findings


def verify_evidence(case_dir: Path, manifest: dict) -> dict:
    findings: list[dict] = []
    items: list[dict] = []
    if not closed(manifest, {"schema_version", "case_id", "items"}, set(), "evidence", findings):
        return {"status": "INVALID", "findings": findings, "items": items, "authenticity": "UNVERIFIED"}
    if manifest.get("schema_version") != "piepowder.evidence/0.1":
        findings.append(issue("UNSUPPORTED_SCHEMA", "evidence.schema_version", "Expected piepowder.evidence/0.1.", "ERROR"))
    if not is_id(manifest.get("case_id")):
        findings.append(issue("INVALID_CASE_ID", "evidence.case_id", "A valid case identifier is required.", "ERROR"))
    entries = manifest.get("items")
    if type(entries) is not list or len(entries) > MAX_ITEMS:
        findings.append(issue("INVALID_EVIDENCE_ITEMS", "evidence.items", "Evidence must be a bounded list of at most 32 items.", "ERROR"))
        entries = []
    seen_ids, seen_paths = set(), set()
    fields = {"evidence_id", "path", "sha256", "kind", "submitted_by", "recorded_at", "obligation_id"}
    for index, entry in enumerate(entries):
        path = f"evidence.items[{index}]"
        if not closed(entry, fields, set(), path, findings):
            continue
        for field in ("evidence_id", "submitted_by"):
            if not is_id(entry.get(field)):
                findings.append(issue("INVALID_IDENTIFIER", path + "." + field, "A valid identifier is required.", "ERROR"))
        identifier = entry.get("evidence_id")
        if is_id(identifier):
            if identifier in seen_ids:
                findings.append(issue("DUPLICATE_EVIDENCE_ID", path, "Evidence identifiers cannot be replayed or replaced within a manifest.", "ERROR"))
            seen_ids.add(identifier)
        relative = entry.get("path")
        if not portable_path(relative) or not relative.startswith("evidence/"):
            findings.append(issue("UNSAFE_EVIDENCE_PATH", path + ".path", "Use a portable relative file path under evidence/.", "ERROR"))
        elif relative.casefold() in seen_paths:
            findings.append(issue("DUPLICATE_EVIDENCE_PATH", path + ".path", "Each evidence path may appear once, including case-folded aliases.", "ERROR"))
        else:
            seen_paths.add(relative.casefold())
        if type(entry.get("sha256")) is not str or not SHA256_RE.fullmatch(entry["sha256"]):
            findings.append(issue("INVALID_EVIDENCE_DIGEST", path + ".sha256", "A complete lowercase SHA-256 digest is required.", "ERROR"))
        if entry.get("kind") not in ("geocode_sample", "quoted_text"):
            findings.append(issue("UNSUPPORTED_EVIDENCE_KIND", path + ".kind", "Only typed geocode samples and inert quoted text are supported.", "ERROR"))
        if timestamp(entry.get("recorded_at")) is None:
            findings.append(issue("INVALID_TIMESTAMP", path + ".recorded_at", "A recorded UTC timestamp is required; it is not independently trusted.", "ERROR"))
        if not is_id(entry.get("obligation_id")) and not (entry.get("kind") == "quoted_text" and entry.get("obligation_id") is None):
            findings.append(issue("INVALID_OBLIGATION_REFERENCE", path + ".obligation_id", "Typed samples must identify a duty.", "ERROR"))
    if any(x["severity"] == "ERROR" for x in findings):
        return {"status": "INVALID", "findings": findings, "items": items, "authenticity": "UNVERIFIED"}
    byte_total = 0
    seen_files = set()
    for index, entry in enumerate(entries):
        path = f"evidence.items[{index}]"
        item = {"evidence_id": entry["evidence_id"], "obligation_id": entry["obligation_id"],
                "kind": entry["kind"], "path": entry["path"], "submitted_by": entry["submitted_by"],
                "recorded_at": entry["recorded_at"], "recorded_sha256": entry["sha256"],
                "observed_sha256": None, "byte_status": "UNAVAILABLE", "data": None}
        items.append(item)
        try:
            raw, file_identity = read_case_bytes(case_dir, entry["path"])
            byte_total += len(raw)
            if byte_total > MAX_EVIDENCE_BYTES:
                raise InputError("Evidence exceeds the aggregate size limit.")
            if file_identity in seen_files:
                raise InputError("Multiple evidence paths refer to the same filesystem object.")
            seen_files.add(file_identity)
            item["observed_sha256"] = digest(raw)
            if item["observed_sha256"] != entry["sha256"]:
                item["byte_status"] = "MISMATCH"
                findings.append(issue("EVIDENCE_HASH_MISMATCH", path, "Observed bytes differ from the manifest commitment. No performance conclusion is drawn."))
                continue
            item["byte_status"] = "MATCH"
            if entry["kind"] == "geocode_sample":
                data = parse_json(raw)
                sample_findings = validate_sample(data)
                if sample_findings:
                    item["byte_status"] = "INVALID_DATA"
                    findings.extend(issue(x["code"], path + ".data", x["message"]) for x in sample_findings)
                else:
                    item["data"] = data
            else:
                # Intentionally do not expose text as instructions or execute/interpret it.
                findings.append(issue("QUOTED_TEXT_NOT_INTERPRETED", path, "Quoted text is retained by digest only and requires human review; it is not evaluated as an instruction or legal argument."))
        except FileNotFoundError:
            findings.append(issue("EVIDENCE_UNAVAILABLE", path, "The listed local file is unavailable. This is not failed performance and is not a live webpage check."))
        except (OSError, InputError):
            item["byte_status"] = "REJECTED"
            findings.append(issue("EVIDENCE_UNREADABLE_OR_UNSAFE", path, "The local file cannot be read safely within the supported limits; no performance conclusion is drawn."))
    states = {item["byte_status"] for item in items}
    if not items:
        findings.append(issue(
            "NO_EVIDENCE_ITEMS", "evidence.items",
            "No evidence items were supplied; a source-byte match cannot be established."
        ))
    # An empty collection vacuously satisfies a set-subset check, but must never
    # be reported as BYTE_MATCH. Missing evidence is unresolved, not performance failure.
    status = ("UNAVAILABLE" if not items else
              "BYTE_MATCH" if states <= {"MATCH"} else
              "UNAVAILABLE" if states <= {"MATCH", "UNAVAILABLE"} else "INTEGRITY_REVIEW")
    return {"status": status, "findings": findings, "items": items, "authenticity": "UNVERIFIED"}
