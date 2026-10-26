# Authoring schemas

These standalone JSON Schema 2020-12 documents describe the supported v0.1 input shapes. They are authoring aids for the offline sandbox, not contracts, authority credentials or legal validation. They use internal references only; an offline validator does not need to fetch another Piepowder schema. Their `urn:piepowder:` identifiers identify documents and are not service endpoints.

| Fixed artifact or evidence type | Authoring schema |
| --- | --- |
| `case.json` | `case.schema.json` |
| `contract.json` | `contract.schema.json` |
| `mandates.json` | `mandates.schema.json` |
| `policy.json` | `policy.schema.json` |
| `evidence.json` | `evidence.schema.json` |
| A `geocode_sample` evidence file | `geocode-sample.schema.json` |

All five fixed artifacts are required by `analyse_case`. The contract schema deliberately allows omitted or null acceptance tests, assessors, triggers, deadlines and mandate references. It also allows an explicitly unspecified denominator. These represent incomplete drafting that the compiler must report, rather than silently supply. An empty mandate list or evidence list is representable and cannot make the associated missing authority or acceptance condition pass. Unsupported acceptance and assessor kinds fall outside the authoring schema; the runtime can still identify such inputs as unsupported and route them for review.

Original alpha baseline, 25 October 2026: all six schema documents were parsed as JSON and their field names and required/optional boundaries were reviewed against the runtime and the six committed fictional cases. Formal validation against the JSON Schema 2020-12 meta-schema was **not run at that stage** because no JSON Schema validator was installed in the checked Python environment. No validator was installed for that original task. The field consistency review is not a substitute for meta-schema validation.

Subsequent P02 evidence, 26 October 2026: the optional development-only
`jsonschema==4.26.0` job checked all six Draft 2020-12 schema documents and one
fictional instance per schema. The [post-merge schema run](https://github.com/Albertito-AI/piepowder/actions/runs/40249690726)
passed for main `1ebdaf1b27c1ee7f3394bc4f973b5cba62437dc9`.
See the [validation record](../docs/validation.md) for the retained first-run
fixture failures and corrected engineering result. This updates the historical
schema-check status; it is not independent human use or external data validation.

## The runtime remains authoritative for supported checks

A schema-valid shape does not establish any of the following. The runtime separately checks them where supported:

- Distinct party and agent identifiers within a record, one buyer and one seller, and unique identifiers within each of the duty, mandate and evidence collections.
- Agreement references, exact supplied policy versions, case and duty links, named submitters and contested-record references.
- Ordered UTC timestamps, nonempty mandate validity intervals, recorded revocation, formation-time scope, deadline order and recorded submission windows.
- Count totals, the agreed sample size, exact integer threshold comparisons, zero denominators, ambiguous rules and conflicting submissions.
- Duplicate or case-folded paths, reserved filenames, filesystem links and reparse points, opened file identity, containment, read errors and changed bytes.
- Input byte, depth, string, object-count, integer-range and aggregate evidence budgets.

Some relations cannot be expressed by these schemas without application logic. In particular, `uniqueItems` does not enforce uniqueness of just one identifier inside otherwise different objects; a date-time format declaration does not compare two dates; a path string cannot establish safe filesystem access; and a digest-shaped string does not verify the file's bytes. A validator may also treat `format` as annotation unless format assertion is enabled. Runtime checks do not depend on schema-validator settings.

## The JSON number profile is stricter at runtime

JSON Schema's `integer` describes a mathematical value. A validator may accept JSON numbers such as `1.0` or `1e0` as integers. Piepowder's bounded JSON parser rejects every fractional or exponent-form numeric token, even if its value would be mathematically integral. Supply lexical integer tokens such as `1`. The parser also rejects duplicate object keys, non-finite values, invalid UTF-8, non-scalar Unicode values and integers outside its supported exact range. Domain integer fields reject booleans.

The runtime accepts only whole-second UTC timestamps in `YYYY-MM-DDTHH:MM:SSZ` form. Offset timestamps, local times, fractional seconds and invalid calendar dates are unsupported. Amounts are integer currency minor units; acceptance percentages are integer basis points. These are declared units, not independently verified currency or conversion information.

## Assurance and effects

Mandates are recorded claims. The implemented scope check concerns `form_contract` at the contract's `formed_at` only. It does not verify principal identity, signatures, actual authority, later event delegation or legal formation. An evidence timestamp is a recorded assertion. Sample counts are recorded assertions whose real-world truth, selection method and reference-service accuracy remain unverified.

Every analysis output retains `work_allowed: false` and `payment_authorised: false`. `CHECKS_COMPLETE` describes supported record checks; it neither issues a ruling nor certifies the meaning of prose. Missing or disputed evidence and unresolved interpretations require review. Quoted text remains inert and requires human review. No model panel, public registry, external timestamp, live network check or payment adapter is provided.

No JSON Schema validator is a runtime dependency. The package's strict standard-library parser and checks remain the implementation used by the CLI. The six fictional fixtures and independently specified test outcomes demonstrate the supported subset; they do not measure real-world arbitration accuracy.
