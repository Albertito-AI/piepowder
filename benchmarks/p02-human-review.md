# P02: human first-use reconstruction protocol (not yet run)

**Facilitator document: contains an answer key.** For a prepared session use the
[facilitator guide](p02-facilitator-guide.md). Give the participant only the
[participant brief](p02-participant-brief.md), its specified fictional inputs and
the [blank response record](p02-participant-response.json). Do not distribute this
protocol or the expected labels before the original responses are retained.
Apply the [local operator procedure](../docs/operator-readiness.md) to the actual
exercise environment. The prepared kit does not record a completed human session.

**Status on 26 October 2026: internal preparation only.** No participant, independent review, human reconstruction time, benefit, legal assessment or demand is represented by this file. These fictional scenarios describe recorded counts, not real geocoding accuracy. The prototype never authorises work, money or a legal disposition.

## Before involving a participant

Obtain a permitted non-implementing human participant with an identifiable role and a disclosed interest in the project. Obtain appropriate voluntary participation and instructions for permitted handling of any notes. Do not use private counterparties, student records, identities, client data or actual geocoding datasets in the trial. The facilitator must record any personal coaching, advance exposure to labels or help from a model. The participant must not be treated as an independent assessor merely for running a different AI agent.

Freeze the exact repository commit, Python environment, P02 label-manifest SHA-256 and trial cards before the session. Keep the expected labels and answer key separate until the participant has completed their independent response. Each respondent receives equivalent factual conditions and the same definition of the result. No external validator may supply the answers as if from an independent person. The P02 label file is an internal engineering oracle, not a blinded professional ground truth.

## Task and comparison

Ask the participant to reconstruct, from a fictional contract and supplied sample record, (a) the rule and denominator, (b) the fraction and exact threshold comparison, (c) whether an exception cap is satisfied, (d) any missing, contested, contradictory or altered evidence, and (e) the point at which an accountable human decision remains necessary. Do not ask them to determine real geographic correctness or legal liability.

For one planned manual-first sequence, use a fresh baseline card with 1,000 sampled fictional records, 972 correct and 17 flagged, an explicitly unspecified denominator, a 98 percent threshold and a 2 percent flag cap. The participant records both 972/1000 and 972/983 before seeing an engine report. Use separate matched cards for the product-assisted reconstruction, including an explicit denominator and one adverse or unknown condition. Record the actual card IDs and any differences. This sequential pilot is **not randomised or controlled** and cannot establish a causal time saving. A later comparative experiment requires an appropriate design and a sufficient, recorded sample.

Measure the entire workflow: opening files, reading the specification, identifying the denominator, computing values, locating the evidence, interpreting the flags, consulting assistance and correcting mistakes. Record start/end time for every step with observed timestamps or UNKNOWN; do not substitute benchmark runtime for human time. Count consequential mistakes, correctly raised concerns, false alarms, omitted material problems, explanations sought and completion without help. If no independent participant is available, this gate remains BLOCKED_PENDING_HUMAN and software testing may continue without changing that state.

## Facilitator record (complete privately after actual observation)

Record: date and location; participant role, interests and consent reference; facilitator and any AI assistance; exact project commit and fixture/label hashes; permitted task order; whether participant previously saw the labels; manual baseline inputs, answers and times; product-assisted inputs, answers and times; help, false alarms, missed issues and corrections; adverse or incomplete outcomes; qualitative observations; confidentiality limits; participant's own account of usability; assessor disagreements; and the next evidence/decision gate.

Proposed evaluation: retain, revise or stop after the original responses, unresolved concerns and actual costs are documented. A blank record cannot be scored as success. Two funded pilots are an upper bound on initial commercial learning, not current customer evidence.

## Numerical answer key for manual baseline (withhold until response is recorded)

All sampled: 972/1000 = 97.2 percent, below 98 percent.
Exclude flagged: 972/(1000-17) = 972/983 = approximately 98.8809766 percent, above 98 percent.
Flagged: 17/1000 = 1.7 percent, below the 2 percent cap.
Without an agreed denominator the quality outcome is UNKNOWN, irrespective of whether one of those numerical readings passes. Neither reading authenticates the sample, reviewer, contract, identity or evidence. Only actual participant observation can close human first use.
