# Integration with the existing projects

Piepowder has a separate repository so that a marketplace cannot silently change
the evidence-review rules while a transaction is in progress. This separation
supports a future neutral service; it does not itself establish institutional independence.

## Existing capabilities and the proposed boundary

| Project | Current role | Proposed relationship |
| --- | --- | --- |
| Symbolon | Private machine-work sandbox with typed work orders, TEST-unit accounting, exact-reference acceptance and challenge/settlement records | Export an expressly versioned case for independent review |
| Piepowder | Offline acceptance clarity, bounded checks and review dossier | Read a permitted export and return findings plus exact source references |
| RegNav | Explicitly mapped local source-change and evidence-handover signals | Signal that a dossier's source dependencies may need reconsideration |

The current Symbolon README was inspected on 25 October 2026. Its existing
`exact-json-v1` and invoice checks are retained as Symbolon capabilities. Its
ledger and settlement simulation are not reproduced in Piepowder. Neither
project currently authenticates a real customer or moves real money.

## First adapter specification

A future read-only Symbolon adapter must pin the supported source-export
version and expected digest, preserve contract/criterion/evidence identifiers,
and report unsupported fields. Required mapping: source repository and revision,
contract ID and bytes, party labels and declared mandates, criterion definitions,
observed delivery/evidence digests, check results and relevant event references.
It must disclose absent authentication and translate TEST units without ever
presenting them as bank money or customer income.

Import must create a new review dossier and leave the source database/export
unchanged. There must be no callback that accepts work, resolves a dispute,
settles a ledger or authorises payment. Round-trip identity checks, unexpected
versions, missing evidence, disputed assertions and partial exports are the
acceptance tests for this adapter.

The adapter is not implemented in 0.1.0a1. A2A, MCP, ERC-8183, ADP and ADRP are
also design targets rather than implemented or certified integrations. Their
current specifications and legal effects must be reviewed before implementing
one justified interface. An MCP tool cannot supply legal authority merely by
returning a successful check.

## A source-change event

If RegNav reports that a mapped local file changed or is missing, Piepowder
should retain the old dossier and open a new review question against the new
version. A source-change event cannot decide substantive falsity, breach,
liability, damages or which party should receive funds.
