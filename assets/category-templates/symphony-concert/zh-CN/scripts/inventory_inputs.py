#!/usr/bin/env python3
"""Inventory a poster project's input package without modifying source files."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


TYPE_MAP = {
    ".pdf": "document_pdf",
    ".docx": "document_word",
    ".doc": "document_word_legacy",
    ".txt": "text",
    ".md": "text_markdown",
    ".csv": "table_csv",
    ".json": "structured_json",
    ".yaml": "structured_yaml",
    ".yml": "structured_yaml",
    ".png": "image_raster",
    ".jpg": "image_raster",
    ".jpeg": "image_raster",
    ".webp": "image_raster",
    ".tif": "image_raster",
    ".tiff": "image_raster",
    ".svg": "image_vector",
    ".zip": "archive",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path, include_hidden: bool, with_hash: bool) -> dict:
    files = []
    counts: Counter[str] = Counter()
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if not include_hidden and any(part.startswith(".") for part in relative.parts):
            continue
        extension = path.suffix.lower()
        kind = TYPE_MAP.get(extension, "unknown")
        counts[kind] += 1
        item = {
            "path": relative.as_posix(),
            "extension": extension or None,
            "size_bytes": path.stat().st_size,
            "kind": kind,
            "role": "unknown",
            "read_status": "unreviewed",
            "notes": "",
        }
        if with_hash:
            item["sha256"] = sha256(path)
        files.append(item)
    return {
        "schema_version": "1.0",
        "input_root": str(root.resolve()),
        "file_count": len(files),
        "kind_counts": dict(sorted(counts.items())),
        "unknown_count": counts.get("unknown", 0),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory to inventory recursively")
    parser.add_argument("--output", "-o", type=Path, help="Write JSON manifest to this path")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden paths")
    parser.add_argument("--hash", action="store_true", help="Calculate SHA-256 for every file")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        parser.error(f"input_dir is not a directory: {args.input_dir}")

    manifest = build_manifest(args.input_dir, args.include_hidden, args.hash)
    payload = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)

    if manifest["unknown_count"]:
        print(f"warning: {manifest['unknown_count']} unknown file type(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

