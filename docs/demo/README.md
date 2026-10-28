# Recorded denominator and evidence review

Executed on 28 October 2026 from
[`d3fcef95f53c82b4e170a914f21e45f4a2c52263`](https://github.com/Albertito-AI/piepowder/tree/d3fcef95f53c82b4e170a914f21e45f4a2c52263), using
CPython 3.12.14 on Linux x86_64. All six shipped cases are fictional.
The README image illustrates observed data; it is not a browser screenshot.
The repository's [reserved rights](../../RIGHTS.md) remain unchanged.

## Input and reproduction

The sample records 972 correct, 11 incorrect and 17 flagged results. Its contract
requires 98% accuracy and allows at most 2% flagged records. The [shipped case guide](../../examples/README.md)
links the contracts, evidence and different denominator choices.

From an authorised repository checkout, using a new output directory:

```sh
PYTHONPATH=src python -m piepowder demo --output artifacts/readme-demo
```

The recorded command used a temporary output directory and exited with status 0.
These are the observed quality and overall fields for all six cases:

| Case | Quality result | Overall result |
| --- | --- | --- |
| `geocode-ambiguous` | `UNKNOWN` | `HUMAN_REVIEW` |
| `geocode-explicit-pass` | `SATISFIED` | `CHECKS_COMPLETE` |
| `geocode-explicit-fail` | `NOT_SATISFIED` | `HUMAN_REVIEW` |
| `geocode-contested` | `UNKNOWN` | `HUMAN_REVIEW` |
| `geocode-conflicting` | `UNKNOWN` | `HUMAN_REVIEW` |
| `geocode-missing-evidence` | `UNKNOWN` | `HUMAN_REVIEW` |

The engine displays `97.200000%` for 972/1000 and `98.880977%` for 972/983.
Displayed percentages are rounded; acceptance comparisons use integers.
An unspecified denominator retains both readings and `AMBIGUOUS_DENOMINATOR`.
No real geocoding or authentication of the supplied counts occurs.

## Inspect the actual viewer and record

Open [index.html](index.html) from an authorised checkout, or download that one file
and open it locally. It is the unmodified generated six-case report, with its data
embedded and no network calls. GitHub displays HTML source instead of running it.
Its SHA-256 and the [complete stdout and docket replay result](recorded-run.json)
are retained with the exact source commit. Browser interaction is not claimed as
newly tested in this documentation change.

Replaying the generated docket with `python -m piepowder verify-docket` ended at
`HUMAN_REVIEW_PENDING`, with six events and `integrity: internally_consistent`.
The replay did not compare an independent checkpoint. `work_allowed` and
`payment_authorised` remained false; `legal_effect` remained `none`.

The 57 existing tests passed in the same environment. This records internal
engineering behaviour, not independent human first use, authenticated evidence,
legal correctness, an enforceable decision, or a customer-readiness milestone.
