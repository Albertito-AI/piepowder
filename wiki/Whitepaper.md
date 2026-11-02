<!-- atlas-whitepaper:managed:v1 -->

# Piepowder: preventing disputes by making disagreement explicit

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

## Inspected foundation

Baseline: [`f82ac8b08c681e184dfebbc05e885d8b2dd063c9`](https://github.com/Albertito-AI/piepowder/tree/f82ac8b08c681e184dfebbc05e885d8b2dd063c9). Sources: [README](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/README.md), [decisions](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/docs/decisions.md), [validation](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/docs/validation.md), [security](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/SECURITY.md) and [roadmap](https://github.com/Albertito-AI/piepowder/blob/f82ac8b08c681e184dfebbc05e885d8b2dd063c9/docs/roadmap.md). Existing reserved rights and customer-release gates remain in force. Public visibility does not grant an open-source licence.
