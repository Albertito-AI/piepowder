<!-- atlas-whitepaper:managed:v1 -->

# Piepowder: preventing disputes by making disagreement explicit


## Abstract and research position

Piepowder investigates how a small deterministic engine can expose disagreement about acceptance criteria before a system attempts adjudication. Its working contribution is a typed agreement and evidence dossier that separates invalid input, missing information, contested premises and completed checks. The central example shows that a denominator choice changes the result of a 98% requirement. The paper develops a source-linked method for reproducing that distinction and an evaluation of reviewer understanding. It makes no claim that deterministic checks constitute legal authority or that a live agent judiciary exists.

This revision, prepared on 15 November 2026, examines the exact source revision below. Commands are provided for reproduction; no new test execution, participant study or independent legal review was conducted for this revision.

## A small arithmetic problem with a large institutional lesson

An agreement promises 98% accuracy. A sample contains 972 correct records, 11 incorrect records and 17 flagged as unresolved. Counting every record gives 97.2%; excluding the unresolved records gives approximately 98.881%. Both calculations are easy. The difficult question is which calculation the parties agreed to use.

Piepowder begins here. Its thesis is that many disputes should be made more intelligible before anyone attempts to automate their resolution. A useful system exposes the acceptance rule, its missing assumptions, the evidence and the questions requiring judgement. It should not manufacture agreement by selecting whichever denominator produces a convenient answer.

Prepared for Albert Tan Sin Hon with AI assistance, 2 November 2026. This original design synthesis extends the project's stated ambitions. It is not independent human review, a binding institutional charter, a legal determination or evidence that an agent judiciary operates today.

## First principles: procedure cannot repair an undefined bargain

A contract is more than a collection of numbers. Its practical meaning depends on who is bound, which duty is triggered, which performance counts, who assesses it and what happens when evidence is incomplete. The first principle is therefore explicitness before automation. A typed duty graph makes these dependencies visible without pretending to extract an authoritative agreement from arbitrary prose.

The second principle is that absence, disagreement and failure are different states. Missing evidence does not prove defective performance. Contested evidence does not become authentic because its checksum matches. A missed procedural deadline does not by itself grant legal authority to award damages. Retaining these distinctions makes the system less decisive in some cases and more useful to a responsible reviewer.

The third principle is contestability. A person affected by a result should be able to identify the input, calculation, rule and unresolved premise behind it. A dossier that supports reconstruction is more valuable than a confidence score without an inspectable basis.

## Fundamental logic of the present engine

The local compiler accepts explicitly typed duties, tests, assessors, parties, triggers, deadlines and recorded mandates. The evidence reader checks bounded local files, exact-byte digests and typed counts. The acceptance profile performs exact numerical comparisons, avoiding a rounded display value becoming the decision rule. Contract, mandate, policy and observed-evidence versions are bound into a dossier.

The procedural simulator records filing, answering, evidence closure, reopening, technical assessment and referral for human review. It preserves late answers and does not silently use new evidence after closure. These are simulated procedural semantics, not service of legal process. Actor labels, recorded authority and acknowledgements are not authenticated identities or trusted timestamps.

Its output states are deliberately modest. `INVALID` concerns the supported format; `HUMAN_REVIEW` identifies unresolved, contested or unsatisfied checks; `CHECKS_COMPLETE` means the supported deterministic checks completed. The retained `work_allowed: false` and `payment_authorised: false` are essential boundaries. A complete calculation is not a permission slip.

## Definitions and exact worked example

A **typed duty** identifies a party, obligation, trigger and supported acceptance test. A **recorded mandate** is input describing asserted scope and authority, not authenticated agency. **Byte integrity** concerns the supplied file's agreement with a digest. **Performance assessment** applies the selected rule to admitted counts. **Legal effect** is outside the engine. These distinctions prevent a checksum or a status label from silently answering a different question.

For the paper's fictional sample, let correct = 972, incorrect = 11 and flagged = 17. At a 98% threshold, compare integer products before formatting percentages:

| Stated denominator rule | Comparison | Supported numerical result |
| --- | --- | --- |
| All sampled records | 972 × 100 < 98 × 1000 | 97.2%, below threshold |
| Exclude flagged records | 972 × 100 ≥ 98 × 983 | Approximately 98.880977%, above threshold |
| Rule not agreed | Both calculations remain possible | `HUMAN_REVIEW`, quality `UNKNOWN` |

The missing rule cannot be repaired by choosing the more favourable percentage. Nor does a matching evidence hash establish that 972 records were actually correct. The executable expectations in [tests/test_core.py](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/tests/test_core.py) preserve both readings and keep `work_allowed` and `payment_authorised` false.

A second counterexample concerns an empty evidence manifest. It contains no mismatching files, but it contains no matched files either. Treating that as success would confuse absence of contradiction with positive evidence. The current regression `test_empty_evidence_manifest_is_unavailable_not_byte_matched` specifies `UNAVAILABLE`, `NO_EVIDENCE_ITEMS`, quality `UNKNOWN` and human review. This is a meaningful boundary test, not a claim that every omission is detected.

## Reproducing the argument and locating its evidence

Select source revision `8368bf1032dcfa7258da3deff7cb458bc894494f` in a separate checkout. Python 3.10 or later and the standard library support the core commands. From the repository root:

```sh
PYTHONPATH=src python -m piepowder analyse examples/geocode-ambiguous
PYTHONPATH=src python -m piepowder analyse examples/geocode-explicit-pass
PYTHONPATH=src python -m piepowder analyse examples/geocode-explicit-fail
PYTHONPATH=src python -m piepowder demo --output artifacts/paper-review
PYTHONPATH=src python -m unittest discover -s tests -v
```

Use a new output directory. The expected fixture distinctions are `UNKNOWN` for ambiguity, `SATISFIED` for the explicit passing rule and `NOT_SATISFIED` for the explicit failing rule. All remain unauthorised to initiate work or payment. Record the exact commit, Python version, inputs, exit status and any differences. Existing dated results in [docs/validation.md](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/docs/validation.md) are historical observations, not a new run performed for this paper.

| Claim | Source of support | What it cannot establish |
| --- | --- | --- |
| Denominator selection and integer comparison remain explicit | [src/piepowder/analysis.py](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/src/piepowder/analysis.py); worked-denominator and rounding tests in [tests/test_core.py](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/tests/test_core.py) | Representative sampling or ground-truth accuracy |
| Empty or altered evidence does not silently become successful performance | [src/piepowder/evidence.py](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/src/piepowder/evidence.py); empty-manifest and tampering tests in [tests/test_core.py](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/tests/test_core.py) | Independent authenticity of the original evidence |
| Procedure retains late answers and a reopening history | [src/piepowder/docket.py](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/src/piepowder/docket.py); [tests/test_docket.py](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/tests/test_docket.py) | Valid service, waiver, consent or an enforceable award |
| Human comprehension can be evaluated separately | [benchmarks/p02-participant-brief.md](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/benchmarks/p02-participant-brief.md); [benchmarks/p02-facilitator-guide.md](https://github.com/Albertito-AI/piepowder/blob/8368bf1032dcfa7258da3deff7cb458bc894494f/benchmarks/p02-facilitator-guide.md) | Completed independent first use or measured benefit |

## Related work and research limits

[Moreau and Missier, PROV-DM (W3C Recommendation, 30 April 2013)](https://www.w3.org/TR/2013/REC-prov-dm-20130430/), section 2, provides a model for entities, activities, derivation and responsibility. Its relevance is to reconstructing how a dossier was produced. Piepowder uses its own format and makes no PROV-conformance claim. Recording a provenance statement remains distinct from verifying its truth.

[UNCITRAL's Technical Notes on Online Dispute Resolution (2016)](https://uncitral.un.org/en/texts/onlinedispute/explanatorytexts/technical_notes) provide a useful institutional comparison. UNCITRAL describes them as descriptive and non-binding guidance for developing ODR systems. This revision verified that limited characterisation in the official indexed description; direct page and PDF retrieval returned HTTP 403. It does not claim a fresh full-text review or infer that Piepowder complies with the Notes. In particular, a local technical dossier supplies neither an institution nor a dispute-resolution mandate.

The source-level contribution here is deliberately narrower than deciding a dispute: it makes an unresolved premise inspectable. Whether this improves fairness or access must be evaluated with participants, rather than inferred from deterministic output. Jurisdiction-specific legal propositions in older project research remain separately dated research and require their own current authority checks before operational use.

## Why the prevention-first architecture matters

Suppose an agent buys geocoding work. Before delivery, the parties can specify whether flags are excluded, a maximum flag rate, the sampling method and who may amend the reference set. After delivery, the same record helps distinguish a calculation dispute from a dispute about sample truth or contractual interpretation. Each requires a different next action.

This separation also prevents automation from laundering power. A verifier should not be able to redefine a denominator, declare its own evidence authoritative and execute a financial sanction in one opaque step. A future system could connect independent functions, but authority, independence and appeal must be supplied by an accountable institution. They cannot be inferred from a chain of software states.

The project remains distinct from Symbolon's TEST transaction accounting and RegNav's evidence tracing. A proposed read-only handover could reuse a pinned export. It must not silently make one project's diagnostic result an operative instruction in another.

## Aim and hope: more cooperative commerce

The near-term aim is an affordable way to discover ambiguous acceptance criteria and assemble a useful review record. The larger hope is that increasingly automated commerce becomes less adversarial: disagreements become precise, parties can correct misunderstandings early, and small participants can present their case without expensive reconstruction.

Social value depends on accessibility and power. A machine-readable contract should have a comprehensible human explanation. Parties need a meaningful chance to contest assumptions, obtain their evidence and use another reviewer. A small supplier should not face impossible documentation burdens merely because the buyer controls the software. Systems must accommodate language, disability and differing technical resources.

The best case is not the elimination of disagreement. It is the preservation of legitimate disagreement in a form that supports fair resolution, while preventable disputes become rarer. Cheap automated adverse decisions without accessible recourse would contradict that purpose.

## Ideal progression

The current fictional engine should first be evaluated by someone who did not write it. Can that person reconstruct the denominator issue, recognise missing evidence and explain why a completed check has no legal effect? The existing prelabelled benchmark and first-use materials are useful preparation; they are not a completed independent study.

Next comes a minimum accountable operating boundary: named operator, permitted inputs, retention rules, access controls and a defined human handoff. Only then should a tightly scoped, authorised pilot examine real workflow value. The question is total effort and quality of understanding, including preparation and false alarms, rather than the engine's execution speed alone.

The ideal wishlist includes versioned acceptance-profile libraries; multilingual explanations; independently retained checkpoints; selective disclosure; authenticated operation-specific mandates; better ways to express exceptions; and interfaces to accountable dispute-resolution institutions. A later legally operative service would need explicit jurisdictional, procedural, professional and financial authority. This paper does not activate that service.

## Research programme and stopping rules

| Question | Useful observation | Reason to change course |
| --- | --- | --- |
| Does explicit specification prevent disagreement? | Ambiguities found before performance, with participant explanation | More paperwork without better understanding |
| Can a reviewer reconstruct a result? | Correct independent reconstruction of input, rule and uncertainty | Readers interpret `CHECKS_COMPLETE` as legal approval |
| Is the process fair to both parties? | Separate burdens, correction opportunities and challenge outcomes | One party can conceal evidence or dominate review |
| Is the supported profile worth using? | Fully costed effort and error comparison with ordinary review | Automation shifts rather than reduces avoidable work |

Useful negative results should be retained. If a prose checklist works better for a task, preserve that route. If a numerical rule fails to represent the parties' actual objective, revise the specification rather than making the engine more confident. The institution's responsibility is to clarify a disagreement, not to hide it behind technical precision.

## A study that could disconfirm the thesis

The existing first-use kit is a fixed-order descriptive exercise. Its manual and assisted cards differ in conditions and difficulty; learning effects prevent their times from establishing causal savings. Preserve that protocol rather than treating it as a controlled comparison. A subsequent, separately designed study could compare a dossier with an ordinary prose checklist on matched fictional cases. Before collecting responses, specify scoring for identifying the denominator, distinguishing missing from adverse evidence, locating a contested premise and explaining why a completed check has no legal effect. Preserve misunderstandings and assistance given. Separate author-labelled benchmark agreement from independently reasoned expected outcomes, and compare total reading and preparation effort, not just calculation time.

Teaching prompts follow directly from the design: explain both percentages without choosing a winner; construct evidence whose bytes match but whose asserted facts are false; and identify the missing institutional steps between `CHECKS_COMPLETE` and a binding disposition. An advanced exercise asks when a fixed numerical criterion fails to represent the parties' actual purpose. The learner should be able to recommend human clarification and a simpler checklist where appropriate.

## Inspected foundation

Current implementation assessment: [`8368bf1032dcfa7258da3deff7cb458bc894494f`](https://github.com/Albertito-AI/piepowder/tree/8368bf1032dcfa7258da3deff7cb458bc894494f), inspected 15 November 2026. The original foundation baseline below is retained as a historical record. Links in the added claim-evidence map identify the current assessed source. This documentation revision changes no implementation, licence, operating permission or release gate.

Baseline: [`f82ac8b08c681e184dfebbc05e885d8b2dd063c9`](https://github.com/Albertito-AI/piepowder/tree/f82ac8b08c681e184dfebbc05e885d8b2dd063c9). Sources: [README](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/README.md), [decisions](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/docs/decisions.md), [validation](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/docs/validation.md), [security](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/SECURITY.md) and [roadmap](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/docs/roadmap.md). Existing reserved rights and customer-release gates remain in force. Public visibility does not grant an open-source licence.
