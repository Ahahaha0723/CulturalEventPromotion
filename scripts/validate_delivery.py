#!/usr/bin/env python3
"""Validate poster output files against a brief and delivery manifest."""

from __future__ import annotations

import argparse
import json
import math
import struct
from collections import Counter
from pathlib import Path
from typing import Any


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


def parse_ratio(value: str) -> float:
    left, right = value.split(":", 1)
    return float(left) / float(right)


def read_image_info(path: Path) -> tuple[str, int, int] | None:
    """Read PNG/JPEG format and dimensions from the file header."""
    with path.open("rb") as handle:
        header = handle.read(24)
        if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
            width, height = struct.unpack(">II", header[16:24])
            return "png", width, height
        if header[:2] != b"\xff\xd8":
            return None
        handle.seek(2)
        while True:
            byte = handle.read(1)
            if not byte:
                return None
            if byte != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9"}:
                continue
            length_raw = handle.read(2)
            if len(length_raw) != 2:
                return None
            length = struct.unpack(">H", length_raw)[0]
            if marker and marker[0] in range(0xC0, 0xC4):
                data = handle.read(5)
                if len(data) != 5:
                    return None
                height, width = struct.unpack(">HH", data[1:5])
                return "jpg", width, height
            handle.seek(max(length - 2, 0), 1)


def validate(brief: dict, manifest: dict, output_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    files = manifest.get("files")
    if not isinstance(files, list):
        return ["manifest.files: expected a list"], warnings

    languages = list(get_path(brief, "languages.required") or [])
    override = get_path(brief, "languages.explicit_single_language_override") is True
    if override and not get_path(brief, "languages.override_reason"):
        errors.append("languages.override_reason: missing explicit user instruction")
    if not override:
        languages = list(dict.fromkeys([*languages, "zh-CN", "en"]))
    allowed_formats = {str(item).lower().lstrip(".") for item in (get_path(brief, "deliverables.formats") or [])}
    required_count = get_path(brief, "deliverables.quantity_per_language") or 1
    ratio_text = get_path(brief, "deliverables.canvas.ratio")
    expected_width = get_path(brief, "deliverables.canvas.width_px")
    expected_height = get_path(brief, "deliverables.canvas.height_px")
    try:
        expected_ratio = parse_ratio(ratio_text)
    except (AttributeError, TypeError, ValueError, ZeroDivisionError):
        errors.append("brief deliverable ratio is invalid")
        expected_ratio = None

    counts: Counter[str] = Counter()
    seen_paths: set[str] = set()
    for index, item in enumerate(files):
        label = f"files[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: expected an object")
            continue
        relative = item.get("path")
        language = item.get("language")
        if not isinstance(relative, str) or not relative:
            errors.append(f"{label}.path: missing")
            continue
        if relative in seen_paths:
            errors.append(f"{label}.path: duplicate '{relative}'")
        seen_paths.add(relative)
        target = (output_root / relative).resolve()
        try:
            target.relative_to(output_root.resolve())
        except ValueError:
            errors.append(f"{label}.path: escapes output root")
            continue
        if not target.is_file():
            errors.append(f"{label}.path: file not found '{relative}'")
        extension = target.suffix.lower().lstrip(".")
        if extension not in allowed_formats:
            errors.append(f"{label}.path: format '{extension}' not allowed")
        declared_format = str(item.get("format", extension)).lower().lstrip(".")
        if declared_format != extension:
            errors.append(f"{label}.format: '{declared_format}' does not match file extension '{extension}'")
        if language not in languages:
            errors.append(f"{label}.language: unexpected '{language}'")
        else:
            if target.is_file() and extension in {"png", "jpg", "jpeg"}:
                counts[language] += 1
        width, height = item.get("width_px"), item.get("height_px")
        if target.is_file() and extension in {"png", "jpg", "jpeg"}:
            image_info = read_image_info(target)
            if image_info is None:
                errors.append(f"{label}: cannot read {extension.upper()} image header")
            else:
                actual_format, actual_width, actual_height = image_info
                normalized_extension = "jpg" if extension == "jpeg" else extension
                if actual_format != normalized_extension:
                    errors.append(f"{label}: file signature is {actual_format}, extension is {extension}")
                if (width, height) != (actual_width, actual_height):
                    errors.append(
                        f"{label}: manifest dimensions {width}x{height} do not match file {actual_width}x{actual_height}"
                    )
                width, height = actual_width, actual_height
        if isinstance(expected_width, int) and isinstance(expected_height, int):
            if (width, height) != (expected_width, expected_height):
                errors.append(f"{label}: expected {expected_width}x{expected_height}, found {width}x{height}")
        if expected_ratio is not None:
            if not isinstance(width, int) or not isinstance(height, int) or height <= 0:
                warnings.append(f"{label}: missing usable width_px/height_px")
            elif not math.isclose(width / height, expected_ratio, rel_tol=0.01, abs_tol=0.01):
                errors.append(f"{label}: pixel ratio {width}:{height} does not match {ratio_text}")
        if item.get("status") != "final":
            warnings.append(f"{label}: status is not final")

    for language in languages:
        if counts[language] < required_count:
            errors.append(f"language '{language}': expected at least {required_count} complete PNG/JPEG poster(s), found {counts[language]}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="Validated content master")
    parser.add_argument("manifest", type=Path, help="Delivery manifest YAML or JSON")
    parser.add_argument("--output-root", type=Path, help="Base directory for manifest paths")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    args = parser.parse_args()

    try:
        brief = load_data(args.brief)
        manifest = load_data(args.manifest)
        root = args.output_root or args.manifest.parent
        errors, warnings = validate(brief, manifest, root)
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

