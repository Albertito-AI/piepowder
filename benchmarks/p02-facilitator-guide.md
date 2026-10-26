# P02 first-use facilitator guide and withheld key

Preparation version: `p02-session-kit/0.1`, 26 October 2026.
**NOT_PERFORMED. FACILITATOR ONLY.** Do not put this file, benchmark labels or
preflight answers in a participant's packet before saving their responses.

This kit makes the [existing protocol](p02-human-review.md) executable as a
bounded session preparation. It does not record a participant, authorise an
invitation or disclosure, establish input rights, or approve real customer work.
The permission to involve a particular person and disclose a particular private
package must already exist before arranging the session. Use the existing
development and private-record owners; create no second scheduler or ledger.

## Question, fixed design and limits

Can one permitted human who did not implement the software reconstruct its
supported acceptance findings, trace them to supplied bytes and explain the
limits without content coaching? Select the participant's role and disclose any
interest before recording the result. An AI agent is not that participant.

Use this order: manual M1, assisted S1, assisted S2, final explanation, then the
key and debrief. Do not select a different card because a participant struggles.
M1 uses the existing protocol's ambiguous 1,000-record baseline. S1 uses a fresh
explicit-denominator numerical case with the same sample size, threshold, flag
cap and record structure. S2 tests unavailable evidence in that supported
structure. The differing rule and evidence conditions are intentional.

These cards match the supported domain and basic record structure; they are not
equivalent difficulty or a controlled pair. Manual-first order creates learning
and carry-over effects. There is one manual card and two assisted cards. Keep
each card's actual time separate. Do not subtract or average these times to
claim software time savings, compare aggregate manual and assisted totals, or
claim causal benefit. This one-person descriptive session cannot estimate
population accuracy, demand or general usability. Any broader experiment needs
a separately fixed design and permission.

Predeclare a 45-minute maximum session: briefing up to 5 minutes, M1 up to 10,
S1 up to 12, S2 up to 8, and final explanation/debrief up to 10. These are
facilitator stopping limits, not performance targets. Preserve an incomplete
response when a limit is reached. Do not invent elapsed time or chargeable work.
Record the owner's actual human effort separately in the designated private
records; tool runtime is not owner effort.

## Freeze and prepare before inviting a participant

The intended engine baseline is the private repository commit:

`1ebdaf1b27c1ee7f3394bc4f973b5cba62437dc9`

Its `benchmarks/p02-labels.json` exact UTF-8 bytes have SHA-256:

`8c24436006d5b52d01669b9a914687ba7872ce1fccfdadf37d93160aa95fd169`

This kit will have its own later repository commit. Record both the actual engine
source commit and the actual kit commit. A source label hash alone does not bind
the engine, example files or instructions. Record the full runtime version and
platform, the actual label hash and an inventory of the exact files supplied.
Keep the label, key and preflight observations outside the participant directory.
An inventory digest detects changes relative to its retained bytes; it does not
authenticate a participant, certify truth or create an independent timestamp.

Before the session, verify the intended commit, source and labels using the
authorised checkout. If any engine, fixture, label or card bytes differ, stop
preparation and record the change. Use a new explicit kit revision and preflight;
do not silently substitute current main. Confirm the current privacy/disclosure
permission and an authorised local runtime. Do not ask a participant to clone the
whole private repository simply to obtain this exercise.

Prepare only copies of fictional cases. At the pinned engine checkout, the
following local preparation illustrates the exact predeclared mapping. Run it
only in an approved workspace. It creates a new directory and refuses reuse.
It performs no external access and supplies no operative customer agreement.

```python
from pathlib import Path
import hashlib
import json

from benchmarks.p02_benchmark import LABELS, labelled_cases, materialise_case
from piepowder.analysis import analyse_case

expected_label_hash = "8c24436006d5b52d01669b9a914687ba7872ce1fccfdadf37d93160aa95fd169"
assert hashlib.sha256(LABELS.read_bytes()).hexdigest() == expected_label_hash
root = Path("artifacts/p02-first-use-preparation")
root.mkdir(parents=True, exist_ok=False)
specs = {spec["id"]: spec for spec in labelled_cases()}
checks = []
for card, benchmark_id, expected_quality in (
    ("S1", "A02", "NOT_SATISFIED"),
    ("S2", "U08", "UNKNOWN"),
):
    folder = root / card / "inputs"
    folder.parent.mkdir()
    materialise_case(specs[benchmark_id], folder)
    neutral_id = "fictional-session-" + card.lower()
    for name in ("case.json", "evidence.json"):
        target = folder / name
        value = json.loads(target.read_text(encoding="utf-8"))
        value["case_id"] = neutral_id
        target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    result = analyse_case(folder)
    quality = next(x for x in result["checks"] if x["kind"] == "geocode_accuracy")
    checks.append({"card": card, "observed": result, "expected_quality": expected_quality})
    if (result["status"] != "HUMAN_REVIEW" or quality["result"] != expected_quality
            or result["work_allowed"] is not False
            or result["payment_authorised"] is not False):
        (root / "FACILITATOR-PREFLIGHT-FAILED.json").write_text(
            json.dumps(checks, indent=2) + "\n", encoding="utf-8")
        raise ValueError("Preflight mismatch: preserve this record; do not use the packet")
(root / "FACILITATOR-PREFLIGHT.json").write_text(
    json.dumps(checks, indent=2) + "\n", encoding="utf-8")
```

The two neutral case identifiers prevent an inherited example name such as
`geocode-explicit-pass` from suggesting an answer. The benchmark inputs and
expected outcomes remain unchanged apart from those linked case identifiers.
The preflight record is facilitator-only. Its success verifies preparation, not
human use. The code above is a preparation recipe; this document does not assert
that it has been run or that a trial packet has been issued.

After preparation, inventory SHA-256 for every exact input and each supplied
instruction/response-template file, using relative paths in sorted order and
retaining the inventory privately. Check that no symlink, unexpected file or
private source material enters the packet. Hash the inventory itself and retain
it with the source/kit commits and environment record. Include the absence of
S2's cited `evidence/sample.json` as an intentional condition. Preserve the
prepared folder and original input bytes unchanged throughout the exercise.

The participant receives the brief, a fresh response-template copy, the approved
local runtime/instructions and only the released card's input folder. Withhold
this guide, `p02-human-review.md` (which also contains a key), the full README
(which prints scenario answers), the label manifest, benchmark source/IDs and
preflight outputs. Supply only the command/environment excerpt needed for the
assisted task after M1; do not supply README result tables. Give only the M1 section initially;
release S1 then S2 after saving each preceding response. The facilitator must
not rewrite the cards or add hints during a session.

For assisted operation, use the supported command with an actual authorised
input path and a new output filename:

```text
PYTHONPATH=src python -m piepowder analyse PATH_TO_S1_INPUTS --output NEW_S1_REPORT.json
```

Use the equivalent command for S2. Replace the path placeholders before use and
provide the platform-appropriate environment instruction from the frozen README.
Do not type the participant's interpretation for them. Record installation/path
help separately from numerical, evidential or interpretive coaching. A failure
to run or understand the workflow is a retained result, not a blank success.

## Withheld key

### M1

- All-sampled reading: `972/1000 = 97.2%`, below 98 percent.
- Exclude-flagged reading: `972/983`, approximately `98.8809766%`, above 98 percent.
- Flagged share: `17/1000 = 1.7%`, within the 2 percent cap.
- The agreement leaves the denominator unspecified. A person cannot select the
  favourable reading as if it had been agreed. The supported quality observation
  remains unresolved. Neither count reading verifies the sample's factual truth.

### S1

Predeclared source: benchmark case `A02`, with linked case identifiers changed
only to `fictional-session-s1`. The supplied counts are 962 correct, 21 incorrect
and 17 flagged out of 1,000. The agreement explicitly excludes flagged records.

- Selected fraction: `962/983`, approximately `97.8636826%`.
- Exact threshold comparison: `962 * 10000 = 9620000`, which is less than
  `9800 * 983 = 9633400`; the 98 percent criterion is not satisfied.
- Flagged share: `17/1000 = 1.7%`, within the cap. A satisfied flag cap does not
  make the accuracy comparison pass.
- Expected quality: `NOT_SATISFIED`, with
  `RECORDED_ACCURACY_BELOW_THRESHOLD`; overall `HUMAN_REVIEW`.
- Matching evidence bytes and recorded time/mandates do not establish factual
  correctness, verified identity, actual delivery time or legal authority.

### S2

Predeclared source: benchmark case `U08`, with linked case identifiers changed
only to `fictional-session-s2`. The agreement uses the explicit exclude-flagged
profile, but the cited `evidence/sample.json` file is unavailable.

- Expected quality: `UNKNOWN`, with `SAMPLE_UNAVAILABLE_OR_UNVERIFIED`;
  overall `HUMAN_REVIEW`.
- There is no supported numerator, observed count or fraction to invent from the
  missing file. Missing evidence is not proof of poor numerical performance.
- The next step is to resolve the missing/unverified record through the
  accountable process, preserving the original record and this uncertainty.
  It is not to assume the previous card's counts or make a payment decision.

### Capability comprehension

The participant should distinguish overall review status, an individual numerical
comparison and a missing/contested evidential conclusion. A matching digest
establishes byte equality to the recorded digest under the local trust boundary;
it does not authenticate a person, agreement, permission, timestamp, sampling
method or geographical truth. The report is not a legal judgment. It leaves
`work_allowed` and `payment_authorised` false. An untrusted/absent input needs
review rather than an invented fact or automatic adverse legal finding.

## Predeclared scoring and next decision

Record original responses before revealing the key. In the private facilitator
record, mark each item `DEMONSTRATED`, `NOT_DEMONSTRATED` or `UNOBSERVED`, with
the participant's actual supporting answer and any assistance. Do not enter
zero for an unobserved error count or time.

| Item | Observation required before a retain recommendation |
| --- | --- |
| R1 | Participant generates and locates both assisted reports from the frozen folders; no numerical or interpretive coaching is needed. |
| R2 | S1 identifies the agreed denominator, correct fraction, below-threshold comparison and satisfied flag cap; it separates quality from the overall review result. |
| R3 | S2 identifies unavailable evidence and an unknown quality result without treating absence as failed performance or importing another card's counts. |
| R4 | Participant points to the relevant contract, manifest and report fields; explains what a digest can and cannot establish. |
| R5 | Final explanation preserves the identity, authority, factual-truth and legal limits and the absence of work/payment authorisation. |

**Retain this prepared workflow for the next bounded review:** all five items are
demonstrated before the key, no consequential issue is missed, and no substantive
content coaching or unrecorded intervention occurred. Report `5/5` only when all
five were actually observed. Minor navigation questions must still be reported;
they cannot be relabelled as unaided use. Manual M1 is a descriptive baseline;
its success is not required to manufacture an assisted success.

**Change and repeat after one specific correction:** any item is not demonstrated
or unobserved, a consequential problem is missed, content coaching is required,
or the participant cannot finish within the session limits. Retain the original
answers and failure, state the exact correction and prepare new predeclared
cards. Reusing a coached participant is a follow-up session, not fresh first use.
Do not add unrelated product features to hide the observed problem.

**Stop the session immediately:** the participant requests it, the agreed handling
permission is absent/withdrawn, real personal/client/bank/secret data appears, or
the workflow requires an unapproved disclosure, network action or external
execution. Preserve only material permitted by the agreed handling terms. Record
the reason and refer the scope or handling question to its accountable owner.
No stopped or incomplete session can be scored as a retained workflow.

Any claim that an engine result authorises payment/work or proves legal liability
is a material comprehension failure, requiring correction and a fresh review.
One successful descriptive session may support the human-first-use evidence
record; it cannot close minimum P03, establish product efficacy, approve a pilot,
activate a licence or release customer work. The accountable owner separately
reviews the evidence and every remaining readiness/commercial gate.

## Private record and handoff

Use the blank response template without filling outcome fields in advance.
It is a structured observation record, not a requirement that the participant
edit JSON. Accept ordinary written notes or a consented verbal response. Retain
the original notes or permitted verbatim transcription, record who transcribed
and any participant correction, and link that source in the structured record.
Do not improve an answer during transcription or score a facilitator's inference
as the participant's explanation.
Store participant references, permission, notes, raw responses, observation times,
help, errors, preflight and scoring in the designated private record, outside Git.
Collect only what the approved session needs. Record the permitted retention
period and disposal/withdrawal procedure before collecting notes. Do not claim
full anonymity if a facilitator can identify the participant.

The engineering log may record a non-identifying status and a private evidence
reference after actual observation. Hand the reference and next action to GitHub
Adoption, the existing sole operational-register/index writer. Do not edit the
financial workbook or treat participant time, a configured session or successful
software checks as paid demand, customer acceptance or independent human success.
