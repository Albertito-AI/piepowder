# Validation record

Prepared 25 October 2026 for version 0.1.0a1. This is an internal engineering
baseline, not independent validation, legal approval or evidence of demand.

## Observed local result

The complete suite ran on Linux with CPython 3.12.14:

```text
PYTHONPATH=src python -m unittest discover -s tests -v
Ran 53 tests in 0.219s
OK
```

All 53 tests passed, with no skipped tests: 34 core, 14 procedural, two report
safety and three CLI integration tests. The recorded duration is one observed
run, not a performance benchmark. The private project archive retains its output.

Coverage addresses restricted JSON input; exact contract, mandate and policy
byte commitments; absent criteria; declared mandate scope and revocation;
path traversal, symlink and hard-link aliases; inconsistent or unavailable
evidence; contested assertions; inert quoted instructions; exact threshold
comparison; replay and retained-checkpoint comparison; late answers; evidence
closure and reopening; safe report embedding; and preservation of existing
output files. The expected fixture outcomes were specified separately from
the generated observation records.

## Demonstration observed

| Fictional case | Numerical quality check | Overall result |
| --- | --- | --- |
| Unspecified denominator | UNKNOWN | HUMAN_REVIEW |
| Explicit exclusion of flagged records | SATISFIED | CHECKS_COMPLETE |
| Explicit inclusion of flagged records | NOT_SATISFIED | HUMAN_REVIEW |
| Contested evidence | UNKNOWN | HUMAN_REVIEW |
| Conflicting evidence | UNKNOWN | HUMAN_REVIEW |
| Missing evidence | UNKNOWN | HUMAN_REVIEW |

The sample produces 97.200000% when all 1,000 records count, and 98.880977%
when the 17 flagged records are excluded. The displayed percentage is rounded;
acceptance uses exact integer comparisons. No ground-truth geocoding was performed.

The demonstration creates real JSON and Markdown analysis, a self-contained HTML
viewer and a synthetic docket. Docket replay ends at `HUMAN_REVIEW_PENDING`;
all analysis and projection records retain false work/payment authorisations.

## Hosted verification

The workflow in `.github/workflows/ci.yml` runs the suite, six-case demonstration
and docket replay on Python 3.10, 3.12 and 3.14. Its action revisions are pinned.
This file records the preparation baseline before the first hosted run; the
GitHub pull-request checks and dated project receipt are the authoritative
records of the actual hosted result and commit. A configured workflow is not
itself evidence that a hosted run passed.

## Limits retained

- The six JSON Schema authoring documents parse as JSON. Formal Draft 2020-12
  meta-schema validation was not run because no validator was installed.
- HTML report escaping and structure are covered by tests. Interactive browser
  inspection of the generated local file was blocked by the cloud browser's
  URL policy, which permits HTTP(S) only. No alternate route was used to bypass
  that restriction. Visual and interaction review remains unverified here.
- No Windows execution, hostile multi-user server test, external security audit,
  performance benchmark or formal state-machine verification was performed.
- Tests exercise locally supplied identity, authority, timestamps and notice
  assertions. They do not authenticate those assertions or establish sample truth.
- The docket records an assessment reference; it does not independently load
  and authenticate the assessment body against the current agreement/dossier.
- There is no empirical model-panel evaluation, independent reviewer study,
  customer-specific pilot, customer payment or live dispute outcome.

Run the narrow checks relevant to each subsequent change and retain failures.
Use the current engineering state and observed results rather than extrapolating
production readiness from this initial suite.
