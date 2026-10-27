"""Validate JSON design data without making any network calls."""
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from codegen.schema import DesignDefinition


def load_and_validate(path: str | Path) -> DesignDefinition:
    """Read JSON from disk and return a validated design definition."""
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})") from exc
    except OSError as exc:
        raise ValueError(f"Cannot read input file: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Top-level JSON value must be an object")

    try:
        return DesignDefinition.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m codegen.validator <design.json>", file=sys.stderr)
        return 2
    try:
        design = load_and_validate(sys.argv[1])
    except ValueError as exc:
        print(f"VALIDATION FAILED\n{exc}", file=sys.stderr)
        return 1

    print(f"VALIDATION PASSED: {design.class_name} ({len(design.fields)} fields)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
