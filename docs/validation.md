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

## P02 prelabelled internal benchmark increment, 26 October 2026

An additional `benchmarks/p02-labels.json` declares 27 distinct fictional variants **before** the benchmark runner evaluates them. They are materialised into separate temporary directories using the existing fictional example files. Categories: six favourable, six adverse, nine unknown and six adversarial. The declared labels contain the expected overall and quality state and selected reason codes. The test does not generate labels from its observations, and retains every failure.

Run the standard-library benchmark using `PYTHONPATH=src python -m benchmarks.p02_benchmark` and the added tests using the existing suite command. The benchmark is explicitly internal. It does not authenticate source counts, sample-selection methods, participants, buyer acceptance or the general usefulness of this product.

The distinct development-only `scripts/p02_validate_schemas.py` checks all six authoring documents against the Draft 2020-12 meta-schema and one known fictional instance per schema using `jsonschema==4.26.0`. A dedicated CI job installs that optional validator; the product runtime and ordinary tests retain no third-party dependency. Formal schema validation is distinct from the runtime's linked-record checks, lexically strict integers and safe filesystem handling.

**Execution evidence:** inspect the actual associated pull-request workflow runs. This entry documents the scope of the increment and does not presume a passed job before its result is observed. The independent human reconstruction protocol is prepared in `benchmarks/p02-human-review.md`; its execution and user-effort outcomes are **NOT_PERFORMED/UNKNOWN**. Minimum P03 operator/input controls and any customer release remain separate open gates.

### P02 observed hosted correction and reproducibility, 26 October 2026

The first hosted run at [40249375608](https://github.com/Albertito-AI/piepowder/actions/runs/40249375608) **failed** two of the 27 declared cases: A01 and U04 had sample-count fields inconsistent with their input mutations, returning `SAMPLE_TOTAL_MISMATCH`. The benchmark retained both failures rather than adjusting the expected output to the engine. Corrected the **input fixture** counts (A01 sample size 10,000; U04 sample size 999), leaving their independently declared expected quality outcomes unchanged.

The follow-up [suite run 40249466456](https://github.com/Albertito-AI/piepowder/actions/runs/40249466456) passed 56 tests on each of Python 3.10, 3.12 and 3.14, with 27/27 labelled cases passing. The [separate schema job 40249466481](https://github.com/Albertito-AI/piepowder/actions/runs/40249466481) passed the six authoring meta-schema checks and one example per schema using `jsonschema==4.26.0`. These statements are tied to the tested branch head; subsequent edits require fresh CI. No independent human first-use measurement, empirical effectiveness or live product release resulted.
