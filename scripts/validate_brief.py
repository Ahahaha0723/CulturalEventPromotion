#!/usr/bin/env python3
"""Validate a cultural-event poster content master in YAML or JSON format."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"confirmed", "pending", "missing", "conflict"}
ALLOWED_CONFIDENCE = {"high", "medium", "low", "unknown"}
ALLOWED_TYPES = {
    "exhibition", "performance", "festival", "lecture", "workshop",
    "reading", "screening", "hybrid", "sports", "other",
}
REQUIRED_FACTS = (
    "event.name",
    "event.organizer",
    "schedule.date",
    "venue.name",
    "audience.target",
)


def load_data(path: Path) -> Any:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError as error:
        raise RuntimeError("YAML input requires PyYAML. Install it or provide JSON.") from error
    return yaml.safe_load(text)


def get_path(data: dict, dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def check_fact(path: str, fact: Any, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(fact, dict):
        errors.append(f"{path}: expected a fact object")
        return
    status = fact.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{path}.status: expected one of {sorted(ALLOWED_STATUSES)}")
    if fact.get("confidence") not in ALLOWED_CONFIDENCE:
        errors.append(f"{path}.confidence: expected one of {sorted(ALLOWED_CONFIDENCE)}")
    if status == "confirmed" and not fact.get("value"):
        errors.append(f"{path}: confirmed fact has no value")
    if status in {"confirmed", "pending", "conflict"} and not fact.get("source"):
        warnings.append(f"{path}: value/status has no source")
    if status in {"missing", "conflict"}:
        warnings.append(f"{path}: status is {status}")


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["root: expected an object"], warnings

    for key in ("schema_version", "project", "event", "schedule", "venue", "audience", "languages", "deliverables", "classification"):
        if key not in data:
            errors.append(f"root: missing key '{key}'")

    for path in REQUIRED_FACTS:
        fact = get_path(data, path)
        if fact is None:
            errors.append(f"{path}: missing required fact")
        else:
            check_fact(path, fact, errors, warnings)

    primary_type = get_path(data, "classification.primary_type")
    if primary_type not in ALLOWED_TYPES:
        errors.append(f"classification.primary_type: expected one of {sorted(ALLOWED_TYPES)}")
    confidence = get_path(data, "classification.confidence")
    if confidence not in ALLOWED_CONFIDENCE - {"unknown"}:
        errors.append("classification.confidence: expected high, medium, or low")
    if confidence == "low":
        warnings.append("classification.confidence: human confirmation required")

    required_languages = get_path(data, "languages.required")
    if not isinstance(required_languages, list) or not required_languages:
        errors.append("languages.required: expected a non-empty list")

    override = get_path(data, "languages.explicit_single_language_override") is True
    if override and not get_path(data, "languages.override_reason"):
        errors.append("languages.override_reason: explicit single-language override requires the user's instruction")
    if not override and (not isinstance(required_languages, list) or not {"zh-CN", "en"}.issubset(required_languages)):
        errors.append("languages.required: every category requires both zh-CN and en posters")

    ratio = get_path(data, "deliverables.canvas.ratio")
    if not isinstance(ratio, str) or ":" not in ratio:
        errors.append("deliverables.canvas.ratio: expected a ratio such as '4:5'")
    formats = get_path(data, "deliverables.formats")
    if not isinstance(formats, list) or not formats:
        errors.append("deliverables.formats: expected a non-empty list")
    quantity = get_path(data, "deliverables.quantity_per_language")
    if not isinstance(quantity, int) or quantity < 1:
        errors.append("deliverables.quantity_per_language: expected an integer >= 1")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="YAML or JSON content master")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    args = parser.parse_args()

    try:
        data = load_data(args.brief)
        errors, warnings = validate(data)
    except (OSError, ValueError, RuntimeError) as error:
        errors, warnings = [str(error)], []

    result = {"valid": not errors, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if result["valid"] else "FAIL")
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARNING: {message}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
