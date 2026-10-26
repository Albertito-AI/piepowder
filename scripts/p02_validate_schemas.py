"""Optional development-only JSON Schema Draft 2020-12 meta-validation."""
from __future__ import annotations

import json
from pathlib import Path
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit("Install the optional developer validator: python -m pip install jsonschema==4.26.0")

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec"
FILES = ("case", "contract", "mandates", "policy", "evidence", "geocode-sample")


def main() -> int:
    for label in FILES:
        document = json.loads((SPEC / (label + ".schema.json")).read_text(encoding="utf-8"))
        if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError("Unexpected schema dialect: " + label)
        Draft202012Validator.check_schema(document)
        example = (ROOT / "examples/geocode-explicit-pass" /
                   ("evidence/sample.json" if label == "geocode-sample" else label + ".json"))
        value = json.loads(example.read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(document, format_checker=FormatChecker()).iter_errors(value),
                        key=lambda e: str(e.path))
        if errors:
            raise ValueError("Example failed " + label + " schema: " + errors[0].message)
        print(label + ": meta-schema valid; one fictional authoring example valid")
    print("6 of 6 Draft 2020-12 schemas and example instances validated; runtime checks remain separate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
