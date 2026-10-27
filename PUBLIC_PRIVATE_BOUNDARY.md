# Public reference and private operational boundary

## Public repository purpose

Piepowder is the inspectable reference layer for making acceptance criteria explicit, preserving evidence and identifying decisions that require human review in commerce between agents. Public material may include original code, typed specifications, fictional cases, synthetic benchmarks, tests, procedural simulations and non-confidential research documentation.

The public repository is not a court, arbitral institution, payment service, production dispute platform or source of binding legal determinations.

## Material that may remain public

- generic contract and evidence schemas;
- fictional disputes, synthetic evidence and public benchmarks;
- deterministic checking code and procedural simulations;
- research documentation, public interfaces and reproducible tests;
- aggregate findings cleared for publication.

## Material that must remain private

- real disputes, parties, contracts, communications, evidence and settlement positions;
- client identities, legal advice, privileged or confidential material;
- production policies, proprietary scoring or risk modules and customer-specific rules;
- identity, fraud, sanctions, payment or enforcement records;
- credentials, private keys, tokens, production databases and deployment configuration;
- incident records, unpublished partner integrations and restricted third-party data.

## Operational split trigger

Create a private operational repository or workspace when the first real dispute, customer policy, production identity flow, confidential evidence package or proprietary commercial module exists. The public protocol and fictional reference implementation may remain here while real cases, adapters, credentials and commercial decision rules stay private.

Public issues should contain only non-confidential proposals or synthetic reproductions. No submission through an issue creates jurisdiction, authority, payment entitlement or a duty to decide.

## Release check

Before publication, establish publication rights, inspect source and generated artifacts for secrets and personal data, confirm that every case is fictional or cleared, preserve unresolved findings, and avoid describing software output as a legal judgment. Removing a file from the current branch does not by itself remove it from Git history.

`RIGHTS.md` governs reuse of this repository. Public visibility grants no licence beyond those terms and no permission to use Piepowder for a real dispute or commercial execution.
