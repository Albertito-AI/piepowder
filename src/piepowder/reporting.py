"""Inert, local views of analysis records; never a decision or an action surface.

These renderers do not read evidence files, fetch resources, interpret a legal
term, or authorise work or payment. Supplied fields are displayed as data.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re


def _json(value: object, *, pretty: bool = False) -> str:
    """JSON with HTML-significant characters inert even in a script data block."""
    encoded = json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
    )
    # ensure_ascii also escapes U+2028/U+2029. Do not HTML-entity-encode JSON:
    # script data blocks do not resolve entities, and round-tripping matters.
    return (encoded.replace("&", "\\u0026").replace("<", "\\u003c")
            .replace(">", "\\u003e").replace("'", "\\u0027"))


def _json_block(value: object) -> str:
    encoded = _json(value, pretty=True)
    longest = max((len(m.group()) for m in re.finditer(r"`+", encoded)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}json\n{encoded}\n{fence}\n"


def render_markdown(result: dict) -> str:
    """Return a plain technical record with all untrusted values inside fences."""
    if not isinstance(result, dict):
        raise TypeError("An analysis result must be a dictionary.")
    summary = {key: result[key] for key in (
        "schema_version", "engine_version", "case_id", "status",
        "work_allowed", "payment_authorised",
    ) if key in result}
    parts = [
        "# Piepowder case record\n",
        "**Private alpha · For synthetic exercises · Technical record only.**\n",
        "This record is not a legal judgment, arbitral award, authenticity certificate, "
        "or permission to start work or move money. A satisfied check describes only "
        "its stated test on the supplied record.\n",
        "## Record\n", _json_block(summary),
        "## Recorded checks\n",
        "SATISFIED and NOT_SATISFIED are test results. UNKNOWN and NOT_RUN do not "
        "establish either performance or breach. Recorded mandate and timestamp "
        "checks do not verify a person's authority or the real time of delivery.\n",
        _json_block(result.get("checks", [])),
    ]
    alternatives = []
    checks = result.get("checks", [])
    for check in checks if isinstance(checks, list) else []:
        if not isinstance(check, dict):
            continue
        metrics = check.get("metrics")
        if isinstance(metrics, dict) and isinstance(metrics.get("readings"), dict):
            alternatives.append({
                "check_id": check.get("check_id"),
                **{key: metrics[key] for key in (
                    "selected_denominator", "threshold_bps", "max_flagged_bps",
                    "readings", "flagged_rate_within_limit",
                    "counts_are_recorded_assertions",
                ) if key in metrics},
            })
    if alternatives:
        parts.extend([
            "## Alternative denominator readings\n",
            "Both calculations are retained below. Displaying an alternative does "
            "not select it as the agreed rule. These calculations do not verify the "
            "underlying sample or establish substantive geocoding accuracy.\n",
            _json_block(alternatives),
        ])
    for heading, key, fallback in (
        ("Reasons for this status", "reasons", []),
        ("Contract findings", "lint", []),
        ("Evidence and recorded provenance", "evidence", {}),
        ("Integrity bindings", "bindings", {}),
        ("Typed relationships", "contract_graph", {}),
        ("Assurance limitations", "assurance", {}),
    ):
        parts.extend([f"## {heading}\n", _json_block(result.get(key, fallback))])
    parts.extend([
        "## Boundary\n",
        "Work and payment are not authorised by this viewer. The permission fields "
        "above are supplied data, not executable instructions. Hash agreement "
        "establishes a relationship between recorded and observed bytes, not identity, "
        "authority, trusted time, evidence truth, or a legal outcome. Paths and "
        "identifiers are displayed only as supplied; no external source is opened.\n",
    ])
    return "\n".join(parts)


_CSS = r"""
:root{color-scheme:light;--paper:#f5f3ee;--panel:#fff;--ink:#182c34;--muted:#52666d;--line:#dce3e1;--teal:#176a63;--tealwash:#e9f3ef;--amber:#8c560f;--amberwash:#fff3db;--red:#a14136;--redwash:#fbeeea;--mono:ui-monospace,SFMono-Regular,Consolas,monospace}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,select{font:inherit}button,select,summary{touch-action:manipulation}a{color:inherit}main:focus{outline:none}[hidden]{display:none!important}.shell{max-width:1180px;margin:auto;padding:30px 36px 48px}.masthead{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-bottom:25px;border-bottom:1px solid var(--line)}.brand{display:flex;align-items:center;gap:12px;font-size:21px;font-weight:760;letter-spacing:-.7px}.monogram{display:grid;place-items:center;width:36px;height:36px;background:var(--ink);color:white;border-radius:10px;font:italic 29px Georgia,serif}.edition{font:650 11px/1.4 var(--mono);text-transform:uppercase;letter-spacing:1px;color:var(--muted);text-align:right}.hero{display:grid;grid-template-columns:1.4fr 1fr;gap:48px;align-items:center;padding:37px 0 32px}.eyebrow{font:700 11px/1.5 var(--mono);letter-spacing:1.7px;color:var(--teal);text-transform:uppercase;margin:0 0 12px}h1{font-size:clamp(32px,4.1vw,47px);line-height:1.13;letter-spacing:-1.9px;margin:0 0 14px;max-width:650px}h2{font-size:23px;line-height:1.3;letter-spacing:-.55px;margin:0 0 10px}h3{font-size:17px;line-height:1.4;margin:0 0 8px}p{margin:0 0 12px}.lead{color:var(--muted);max-width:560px;margin:0;font-size:16px}.boundary{border:1px solid #c8d9d5;background:#edf4f0;border-radius:16px;padding:22px 24px}.boundary h2{font-size:16px;letter-spacing:0}.boundary p{font-size:13px;margin-bottom:12px}.boundary p:last-child{margin-bottom:0}.boundary strong{color:#214b43}.toolbar{display:grid;grid-template-columns:minmax(240px,1fr) auto;align-items:end;gap:22px;background:var(--ink);color:white;border-radius:16px;padding:19px 23px;margin-bottom:24px}.toolbar label{display:block;font:650 11px/1.5 var(--mono);letter-spacing:1px;text-transform:uppercase;margin-bottom:7px;color:#bcd1d1}select{width:100%;max-width:560px;border:1px solid #526d73;border-radius:8px;padding:10px 35px 10px 12px;background:#233d46;color:#fff;cursor:pointer}select:focus-visible,summary:focus-visible{outline:3px solid #2eaaa1;outline-offset:4px}.scenario-count{font-size:12px;color:#c1d0d2;margin:0 0 12px;white-space:nowrap}.overview{display:flex;align-items:flex-start;justify-content:space-between;gap:28px;padding:5px 2px 22px}.case-title{overflow-wrap:anywhere}.summary{max-width:750px;color:var(--muted);margin:0;font-size:14px}.badge{display:inline-block;border-radius:6px;padding:4px 8px;font:700 10px/1.5 var(--mono);letter-spacing:.25px;overflow-wrap:anywhere}.badge.neutral{background:#eaf0f2;color:#3d5963}.badge.review{background:var(--amberwash);color:var(--amber)}.badge.error{background:var(--redwash);color:var(--red)}.badge.good{background:var(--tealwash);color:var(--teal)}.overview>.badge{margin-top:5px;flex-shrink:0}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-bottom:22px}.stat{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:14px 18px}.stat-value{display:block;font-size:25px;font-weight:700;letter-spacing:-.6px}.stat-label{color:var(--muted);font-size:12px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:15px;margin-bottom:20px;padding:23px 25px}.section-label{font:650 10px/1.5 var(--mono);letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin-bottom:8px}.panel h2{font-size:20px}.note{font-size:13px;color:var(--muted);max-width:850px}.readings{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin:17px 0 11px}.reading{background:#f8faf9;border:1px solid var(--line);border-radius:12px;padding:18px 20px}.reading .value{font-size:32px;line-height:1.25;font-weight:720;letter-spacing:-1px;margin:10px 0 4px;overflow-wrap:anywhere}.reading .fraction{font-family:var(--mono);font-size:12px;color:var(--muted);margin-bottom:11px}.reading h3{font-size:14px}.reading .badge{margin-top:1px}.reading-note{font:11px/1.7 var(--mono);color:var(--muted);overflow-wrap:anywhere}.reading-group+.reading-group{border-top:1px solid var(--line);padding-top:20px;margin-top:20px}.table-scroll{overflow-x:auto}table{width:100%;border-collapse:collapse;text-align:left}th{font:650 10px/1.5 var(--mono);letter-spacing:.5px;text-transform:uppercase;color:var(--muted);padding:9px 12px;border-bottom:1px solid var(--line)}td{vertical-align:top;padding:14px 12px;border-bottom:1px solid #e9eeec;font-size:13px}th:first-child,td:first-child{padding-left:0}th:last-child,td:last-child{padding-right:0}tbody tr:last-child td{border-bottom:0}.check-name{display:block;font-weight:650;overflow-wrap:anywhere}.subtle{color:var(--muted);font-size:12px;overflow-wrap:anywhere}.mono{font-family:var(--mono)}.check-kind{display:block;color:var(--muted);font:11px/1.7 var(--mono);margin-top:3px}.check-details{min-width:200px}.check-details summary{font-size:12px;color:var(--teal);cursor:pointer}.check-details pre{max-width:370px;font-size:11px;line-height:1.65;padding:12px;background:#f3f6f5;border-radius:8px;margin:10px 0 0}.split{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}.findings-list{display:grid;gap:12px}.finding{border-left:3px solid #c3d6d1;padding:2px 0 2px 13px}.finding.error{border-color:#d59d94}.finding.review{border-color:#d9b579}.finding-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px}.finding-code{font:650 11px/1.6 var(--mono);overflow-wrap:anywhere}.finding p{font-size:13px;margin:7px 0 0;white-space:pre-wrap;overflow-wrap:anywhere}.path{display:block;font:11px/1.6 var(--mono);color:var(--muted);overflow-wrap:anywhere}.empty{padding:14px 0;color:var(--muted);font-size:13px}.disclosure{padding:0}.disclosure>summary{padding:19px 24px;cursor:pointer;font-weight:650;font-size:15px;list-style-position:inside}.disclosure[open]>summary{border-bottom:1px solid var(--line)}.disclosure-body{padding:20px 24px}.disclosure-body>p:last-child{margin-bottom:0}.record-list{display:grid;gap:13px;margin-top:15px}.record-list details{border:1px solid var(--line);border-radius:9px}.record-list summary{padding:12px 14px;cursor:pointer;font:650 12px/1.6 var(--mono);overflow-wrap:anywhere}.record-list pre{margin:0;padding:15px;border-top:1px solid var(--line);background:#f7f9f8;font-size:11px;line-height:1.75;border-radius:0 0 9px 9px}pre{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-family:var(--mono);font-size:12px;line-height:1.8;margin:0}.assurance-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 25px}.assurance-row{padding:10px 0;border-bottom:1px solid var(--line)}.assurance-row dt{font-size:12px;color:var(--muted);margin-bottom:3px}.assurance-row dd{margin:0;font:600 11px/1.7 var(--mono);overflow-wrap:anywhere}.alert{border:1px solid #dbb7a9;background:var(--redwash);padding:14px 18px;border-radius:10px;margin-bottom:18px;color:var(--red);font-size:13px}.empty-view{text-align:center;padding:70px 25px;background:white;border:1px solid var(--line);border-radius:16px}.footer{padding:18px 2px 0;color:var(--muted);font-size:11px;display:flex;justify-content:space-between;gap:25px}.footer p{margin:0;max-width:760px}.footer .stamp{font:650 10px/1.7 var(--mono);text-transform:uppercase;white-space:nowrap}.noscript{padding:20px;border:1px solid var(--line);background:white;margin-bottom:20px;border-radius:12px}
@media(max-width:800px){.shell{padding:22px 20px 32px}.hero{grid-template-columns:1fr;gap:22px;padding:28px 0}.boundary{padding:18px 20px}.split{grid-template-columns:1fr;gap:0}.overview{gap:15px}.panel{padding:20px}.disclosure{padding:0}.disclosure-body{padding:18px 20px}.disclosure>summary{padding:18px 20px}.footer{flex-direction:column;gap:12px}}
@media(max-width:520px){.shell{padding:18px 13px 26px}.edition{max-width:150px}.hero h1{font-size:35px}.toolbar{grid-template-columns:1fr;gap:6px;padding:17px}.scenario-count{margin:3px 0 0}.overview{flex-direction:column;gap:10px}.overview>.badge{margin:0}.readings{grid-template-columns:1fr}.stats{gap:7px}.stat{padding:11px}.stat-label{font-size:11px}.stat-value{font-size:22px}.assurance-grid{grid-template-columns:1fr}.panel{padding:18px}.disclosure{padding:0}td,th{padding-right:9px;padding-left:9px}.footer .stamp{white-space:normal}}
@media print{body{background:white}.shell{max-width:none;padding:0}.toolbar,.edition{display:none}.hero{padding-top:5px;gap:25px}.panel,.boundary,.stat,.reading{break-inside:avoid}.footer{display:block}.check-details{min-width:0}}
"""


_SCRIPT = r"""
"use strict";
(() => {
  const records = JSON.parse(document.getElementById("case-data").textContent);
  const byId = id => document.getElementById(id);
  const list = value => Array.isArray(value) ? value : [];
  const object = value => value && typeof value === "object" && !Array.isArray(value) ? value : {};
  const show = value => value === undefined ? "Not provided" : typeof value === "string" ? value : JSON.stringify(value);
  const pretty = value => JSON.stringify(value === undefined ? null : value, null, 2);
  const classes = new Map([["SATISFIED", "good"], ["NOT_SATISFIED", "error"], ["UNKNOWN", "review"], ["NOT_RUN", "neutral"], ["INVALID", "error"], ["HUMAN_REVIEW", "review"], ["CHECKS_COMPLETE", "neutral"], ["ERROR", "error"], ["REVIEW", "review"], ["INFO", "neutral"]]);
  const statusCopy = new Map([
    ["INVALID", "The supplied record is outside the supported input rules. No performance or legal conclusion follows."],
    ["HUMAN_REVIEW", "An unresolved question, failed test or evidence limitation needs review. Read the reasons before interpreting a check."],
    ["CHECKS_COMPLETE", "The supported record checks are complete. This does not verify authority, establish real-world performance, or authorise work or payment."]
  ]);
  const kindNames = new Map([["recorded_mandate_scope", "Recorded mandate scope"], ["geocode_accuracy", "Geocode count calculation"], ["recorded_submission_window", "Recorded submission window"]]);
  const assuranceNames = new Map([["identity", "Identity"], ["authority", "Authority"], ["signatures", "Signatures"], ["timestamps", "Timestamps"], ["sample_method_and_truth", "Sample method and truth"], ["external_append_only", "Independent append-only log"], ["model_panels", "Model panels"], ["legal_effect", "Legal effect"]]);
  function node(tag, className, value) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (value !== undefined) element.textContent = show(value);
    return element;
  }
  function badge(value) { return node("span", "badge " + (classes.get(value) || "neutral"), value); }
  function detail(label, value) {
    const element = node("details", "");
    element.append(node("summary", "", label), node("pre", "", pretty(value)));
    return element;
  }
  function findings(target, values, emptyText) {
    const parent = byId(target);
    parent.replaceChildren();
    if (!list(values).length) { parent.append(node("p", "empty", emptyText)); return; }
    for (const raw of list(values)) {
      const finding = object(raw);
      const item = node("div", "finding " + (classes.get(finding.severity) || "neutral"));
      const head = node("div", "finding-head");
      head.append(node("span", "finding-code", finding.code), badge(finding.severity || "UNSPECIFIED"));
      item.append(head, node("span", "path", finding.path), node("p", "", finding.message));
      parent.append(item);
    }
  }
  function denominatorReadings(checks) {
    const target = byId("reading-groups");
    target.replaceChildren();
    let count = 0;
    for (const raw of checks) {
      const check = object(raw);
      const metrics = object(check.metrics);
      const readings = object(metrics.readings);
      if (!Object.keys(readings).length) continue;
      count += 1;
      const group = node("div", "reading-group");
      group.append(node("p", "reading-note", "Check: " + show(check.check_id) + " · Declared denominator: " + show(metrics.selected_denominator)));
      const cards = node("div", "readings");
      for (const [key, title] of [["all_sampled", "Count every sampled record"], ["exclude_flagged", "Exclude flagged records"]]) {
        const reading = object(readings[key]);
        const card = node("article", "reading");
        card.append(node("h3", "", title));
        const percentage = reading.percentage === undefined || reading.percentage === null ? "Not provided" : show(reading.percentage) + "%";
        card.append(node("div", "value", percentage));
        card.append(node("p", "fraction", show(reading.numerator) + " / " + show(reading.denominator) + " recorded counts"));
        const decision = reading.threshold_satisfied === true ? "MEETS NUMERIC THRESHOLD" : reading.threshold_satisfied === false ? "BELOW NUMERIC THRESHOLD" : "THRESHOLD RESULT UNKNOWN";
        card.append(node("span", "badge " + (reading.threshold_satisfied === true ? "good" : reading.threshold_satisfied === false ? "error" : "neutral"), decision));
        cards.append(card);
      }
      group.append(cards);
      const threshold = typeof metrics.threshold_bps === "number" && Number.isFinite(metrics.threshold_bps) ? String(metrics.threshold_bps / 100) + "%" : "Not provided";
      group.append(node("p", "reading-note", "Recorded threshold: " + threshold + " · Flagged rate within recorded limit: " + show(metrics.flagged_rate_within_limit)));
      target.append(group);
    }
    byId("denominator-panel").hidden = count === 0;
  }
  function render(index) {
    const record = object(records[index]);
    const checks = list(record.checks);
    const evidence = object(record.evidence);
    const evidenceItems = list(evidence.items);
    byId("case-title").textContent = show(record.case_id);
    byId("case-summary").textContent = statusCopy.get(record.status) || "The record has no recognised overall status. Inspect the supplied fields; no conclusion is inferred.";
    byId("case-status").replaceChildren(badge(record.status === undefined ? "STATUS NOT PROVIDED" : record.status));
    byId("check-count").textContent = String(checks.length);
    byId("attention-count").textContent = String(checks.filter(item => object(item).result !== "SATISFIED").length);
    byId("evidence-count").textContent = String(evidenceItems.length);
    const unexpected = record.work_allowed !== false || record.payment_authorised !== false;
    byId("permission-alert").hidden = !unexpected;
    byId("permission-fields").textContent = "Supplied work_allowed: " + show(record.work_allowed) + " · supplied payment_authorised: " + show(record.payment_authorised);
    const rows = byId("check-rows");
    rows.replaceChildren();
    for (const raw of checks) {
      const check = object(raw);
      const row = node("tr", "");
      const identity = node("td", "");
      identity.append(node("span", "check-name", kindNames.get(check.kind) || check.kind), node("span", "check-kind", check.check_id));
      const duty = node("td", "mono subtle", check.obligation_id === null ? "No duty ID" : show(check.obligation_id));
      const state = node("td", "");
      state.append(badge(check.result === undefined ? "NOT PROVIDED" : check.result));
      const more = node("td", "check-details");
      more.append(detail("Inspect result and metrics", check));
      row.append(identity, duty, state, more);
      rows.append(row);
    }
    byId("checks-empty").hidden = checks.length !== 0;
    denominatorReadings(checks);
    findings("case-findings", record.reasons, "No case reasons were supplied. This is not independent clearance.");
    findings("lint-findings", record.lint, "No contract findings were supplied.");
    findings("evidence-findings", evidence.findings, "No evidence findings were supplied.");
    byId("evidence-summary").textContent = "Recorded byte status: " + show(evidence.status) + " · Authenticity: " + show(evidence.authenticity);
    const items = byId("evidence-records");
    items.replaceChildren();
    for (const raw of evidenceItems) {
      const item = object(raw);
      items.append(detail(show(item.evidence_id) + " · " + show(item.byte_status), item));
    }
    if (!evidenceItems.length) items.append(node("p", "empty", "No evidence item records were supplied."));
    const assurance = byId("assurance-records");
    assurance.replaceChildren();
    for (const [key, value] of Object.entries(object(record.assurance))) {
      const row = node("div", "assurance-row");
      row.append(node("dt", "", assuranceNames.get(key) || key), node("dd", "", value));
      assurance.append(row);
    }
    if (!assurance.children.length) assurance.append(node("p", "empty", "No assurance fields were supplied. Nothing is treated as verified."));
    byId("binding-record").textContent = pretty(record.bindings);
    byId("graph-record").textContent = pretty(record.contract_graph);
    byId("complete-record").textContent = pretty(record);
  }
  const select = byId("scenario-select");
  records.forEach((raw, index) => {
    const record = object(raw);
    const option = node("option", "", show(record.case_id));
    option.value = String(index);
    select.append(option);
  });
  byId("scenario-count").textContent = records.length + (records.length === 1 ? " supplied record" : " supplied records") + " · local view";
  select.addEventListener("change", () => render(select.selectedIndex));
  if (records.length) render(0);
  else {
    select.disabled = true;
    select.append(node("option", "", "No case records"));
    byId("case-view").hidden = true;
    byId("empty-view").hidden = false;
  }
})();
"""


_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="__CSP__">
<meta name="referrer" content="no-referrer">
<title>Piepowder · Private case viewer</title><style>__CSS__</style></head>
<body><div class="shell">
<header class="masthead"><div class="brand"><span class="monogram" aria-hidden="true">p.</span>Piepowder</div><div class="edition">Private alpha<br>Synthetic scenarios only</div></header>
<section class="hero"><div><p class="eyebrow">Agreement &amp; evidence review</p><h1>Clarity before<br>a dispute.</h1><p class="lead">Trace a recorded agreement, compare the checks, and see the questions that still need a person.</p></div><aside class="boundary" aria-label="Limits of this viewer"><h2>A technical record, with clear limits.</h2><p>For internal synthetic exercises. Supplied records are displayed, not independently authenticated.</p><p><strong>No legal judgment. No work authorisation. No payment authorisation.</strong> A satisfied check is not permission to act.</p></aside></section>
<div class="toolbar"><div><label for="scenario-select">Explore a scenario</label><select id="scenario-select" aria-controls="case-view"></select></div><p class="scenario-count" id="scenario-count"></p></div>
<noscript><div class="noscript">This local viewer needs JavaScript to display its embedded records. Use the accompanying Markdown case record if scripts are disabled. No network access is required.</div></noscript>
<div class="empty-view" id="empty-view" hidden><h2>No case records supplied</h2><p>The viewer has no results to display. No checks or conclusions are inferred.</p></div>
<main id="case-view" tabindex="-1">
<section class="overview" aria-live="polite"><div><p class="section-label">Selected record</p><h2 class="case-title" id="case-title"></h2><p class="summary" id="case-summary"></p></div><div id="case-status"></div></section>
<div id="permission-alert" class="alert" hidden>The supplied permission fields are missing or outside this alpha's expected false values. The viewer grants no permission; review the original record.</div>
<div class="stats"><div class="stat"><span class="stat-value" id="check-count"></span><span class="stat-label">Recorded checks</span></div><div class="stat"><span class="stat-value" id="attention-count"></span><span class="stat-label">Checks not satisfied</span></div><div class="stat"><span class="stat-value" id="evidence-count"></span><span class="stat-label">Evidence item records</span></div></div>
<section class="panel" id="denominator-panel" hidden><p class="section-label">One sample · Different readings</p><h2>The denominator changes the answer.</h2><p class="note">These are alternative calculations on recorded counts. Displaying both does not choose the agreed rule or verify the underlying sample.</p><div id="reading-groups"></div></section>
<section class="panel"><p class="section-label">What the engine actually checked</p><h2>Results, with their basis attached.</h2><p class="note">SATISFIED describes the stated record check only. UNKNOWN and NOT_RUN establish neither performance nor breach. Recorded mandate and time checks do not authenticate authority or actual delivery.</p><div class="table-scroll"><table><thead><tr><th scope="col">Check</th><th scope="col">Duty</th><th scope="col">Result</th><th scope="col">Record</th></tr></thead><tbody id="check-rows"></tbody></table></div><p id="checks-empty" class="empty" hidden>No check records were supplied.</p></section>
<div class="split"><section class="panel"><p class="section-label">Why this status</p><h2>Case reasons</h2><div class="findings-list" id="case-findings"></div></section><section class="panel"><p class="section-label">Before performance</p><h2>Contract findings</h2><div class="findings-list" id="lint-findings"></div></section></div>
<details class="panel disclosure" open><summary>Evidence &amp; provenance</summary><div class="disclosure-body"><p class="note" id="evidence-summary"></p><p class="note">A matching digest concerns bytes. It does not prove identity, authority, trusted time, sample truth or a legally effective outcome. Paths and identifiers below are displayed only as supplied.</p><div id="evidence-findings" class="findings-list"></div><div id="evidence-records" class="record-list"></div></div></details>
<details class="panel disclosure" open><summary>Authority &amp; assurance limits</summary><div class="disclosure-body"><p class="note">The checks cannot promote self-declared facts into verified facts. These are the engine's recorded limitations.</p><dl id="assurance-records" class="assurance-grid"></dl><p class="reading-note" id="permission-fields"></p></div></details>
<details class="panel disclosure"><summary>Integrity bindings &amp; digests</summary><div class="disclosure-body"><p class="note">These are the supplied bindings. This viewer does not independently re-read or hash the source files.</p><pre id="binding-record"></pre></div></details>
<details class="panel disclosure"><summary>Typed contract relationships</summary><div class="disclosure-body"><p class="note">Explicitly recorded duties and parties. This is not an interpretation of unstated legal rights.</p><pre id="graph-record"></pre></div></details>
<details class="panel disclosure"><summary>Complete supplied analysis record</summary><div class="disclosure-body"><p class="note">Read-only data, including all fields supplied by the analysis engine.</p><pre id="complete-record"></pre></div></details>
</main>
<footer class="footer"><p>Self-contained local view. No external assets, network requests, telemetry, storage, file uploads or automatic actions. This page is a technical record, not a legal judgment or a live dispute service.</p><p class="stamp">Piepowder / private alpha</p></footer>
</div><script type="application/json" id="case-data">__CASE_DATA__</script><script>__SCRIPT__</script></body></html>
"""


def render_dashboard(results: list[dict]) -> str:
    """Return one offline HTML file; all dynamic DOM content uses textContent."""
    if not isinstance(results, list) or any(not isinstance(result, dict) for result in results):
        raise TypeError("Dashboard results must be a list of dictionaries.")
    data = _json(results)
    script_hash = base64.b64encode(hashlib.sha256(_SCRIPT.encode("utf-8")).digest()).decode("ascii")
    style_hash = base64.b64encode(hashlib.sha256(_CSS.encode("utf-8")).digest()).decode("ascii")
    policy = (
        "default-src 'none'; "
        f"script-src 'sha256-{script_hash}'; style-src 'sha256-{style_hash}'; "
        "connect-src 'none'; img-src 'none'; font-src 'none'; object-src 'none'; "
        "base-uri 'none'; form-action 'none'; frame-src 'none'"
    )
    # Insert untrusted data last so a marker inside a value is never substituted.
    return (_PAGE.replace("__CSP__", policy, 1).replace("__CSS__", _CSS, 1)
            .replace("__SCRIPT__", _SCRIPT, 1).replace("__CASE_DATA__", data, 1))
