# Fictional cases

Every principal, agent, mandate, assertion and transaction in these directories is fictional. These files create no commercial agreement, signing authority, licence, payment permission or live arbitration. Amounts use integer currency minor units; percentages use integer basis points in the contract.

The six cases share the report's invented sample: 972 correct, 11 incorrect and 17 flagged records out of 1,000. Including every sampled record gives 97.2%. Excluding the flagged records gives 972/983, or approximately 98.880977%. The engine does not decide which interpretation the parties should have agreed.

| Case | Independently specified expected record-check outcome |
| --- | --- |
| `geocode-ambiguous` | Human review; acceptance result unknown because the denominator is unspecified. |
| `geocode-explicit-pass` | Deterministic checks complete; the expressly selected exclusion rule satisfies the recorded numerical conditions. |
| `geocode-explicit-fail` | Human review; the expressly selected full-sample rule does not satisfy the recorded threshold. |
| `geocode-contested` | Human review; the sample is explicitly contested. |
| `geocode-conflicting` | Human review; two parties have submitted different counts for the same duty. |
| `geocode-missing-evidence` | Human review; the listed local sample is unavailable. Missing evidence is not failed performance. |

`CHECKS_COMPLETE` means the supported checks of the recorded assertions completed. It does not establish identity, valid authority, factual truth, genuine delivery time or an enforceable result. Every output has `work_allowed: false` and `payment_authorised: false`.

Each case includes fixed `case.json`, `contract.json`, `mandates.json`, `policy.json` and `evidence.json` artifacts. The agreement digest binds the exact bytes of the contract, mandates and policy. The dossier digest additionally binds the case metadata, evidence manifest and observed byte-check results. Changing whitespace in an agreed artifact therefore changes its agreement digest. Digests detect differences relative to a retained commitment; they do not authenticate the commitment itself.

Mandates are labelled `authority_basis: recorded_claim`. Their declared limits are compared only for the `form_contract` action at `formed_at`; this sandbox has no signature or identity verifier and does not check authority for subsequent delivery, evidence submission, filing or settlement. The evidence manifest's `recorded_at` is a supplied timestamp assertion. The recorded submission-window comparison does not prove actual delivery or a trusted time source.

The absent sample in `geocode-missing-evidence` is intentional. No website is fetched, and no conclusion about any live external source follows from that case. Evidence paths remain inside each case directory. Submitted text, scripts and executable expressions are never run. Generated observations belong in the ignored `artifacts/` directory; expected outcomes are independently asserted in `tests/test_core.py`.
