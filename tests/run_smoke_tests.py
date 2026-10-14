#!/usr/bin/env python3
"""Run dependency-light smoke tests for the skill's deterministic scripts."""

from __future__ import annotations

import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*arguments: str, expected: int = 0) -> None:
    result = subprocess.run([PYTHON, *arguments], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != expected:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expected}: {' '.join(arguments)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def write_png_header(path: Path, width: int, height: int) -> None:
    """Write the PNG signature and IHDR fields needed by the header validator."""
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR" + struct.pack(">II", width, height))


def main() -> int:
    validate_brief = str(ROOT / "scripts" / "validate_brief.py")
    fixtures = ROOT / "tests" / "fixtures"
    run(validate_brief, str(fixtures / "valid-bilingual-lecture.json"))
    run(validate_brief, str(fixtures / "valid-mixed-event.json"))
    run(validate_brief, str(fixtures / "invalid-missing-critical-fields.json"), expected=1)

    with tempfile.TemporaryDirectory() as temp_dir:
        output_root = Path(temp_dir)
        sports_brief = json.loads((fixtures / "valid-bilingual-lecture.json").read_text())
        sports_brief["classification"]["primary_type"] = "sports"
        sports_path = output_root / "sports-brief.json"
        sports_path.write_text(json.dumps(sports_brief), encoding="utf-8")
        run(validate_brief, str(sports_path))
        sports_brief["classification"]["primary_type"] = "unsupported-test-type"
        sports_path.write_text(json.dumps(sports_brief), encoding="utf-8")
        run(validate_brief, str(sports_path), expected=1)
        for language in ("zh-CN", "en"):
            write_png_header(output_root / f"lecture-test_{language}_4x5_final_v01.png", 2400, 3000)
        manifest = {
            "schema_version": "1.0",
            "project_id": "lecture-test",
            "files": [
                {"path": "lecture-test_zh-CN_4x5_final_v01.png", "language": "zh-CN", "format": "png", "width_px": 2400, "height_px": 3000, "status": "final"},
                {"path": "lecture-test_en_4x5_final_v01.png", "language": "en", "format": "png", "width_px": 2400, "height_px": 3000, "status": "final"},
            ],
        }
        manifest_path = output_root / "delivery.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        run(
            str(ROOT / "scripts" / "validate_delivery.py"),
            str(fixtures / "valid-bilingual-lecture.json"),
            str(manifest_path),
            "--output-root",
            str(output_root),
        )
        manifest["files"] = manifest["files"][:1]
        invalid_manifest_path = output_root / "delivery-invalid.json"
        invalid_manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        run(
            str(ROOT / "scripts" / "validate_delivery.py"),
            str(fixtures / "valid-bilingual-lecture.json"),
            str(invalid_manifest_path),
            "--output-root",
            str(output_root),
            expected=1,
        )

        # A 2:3 export must be rejected against the requested 4:5 canvas,
        # even when filename and manifest dimensions agree with that wrong export.
        wrong_canvas_files = []
        for language in ("zh-CN", "en"):
            name = f"academic-forum_{language}_2x3_review.png"
            write_png_header(output_root / name, 2400, 3600)
            wrong_canvas_files.append({"path": name, "language": language,
                                       "format": "png", "width_px": 2400,
                                       "height_px": 3600, "status": "review"})
        wrong_canvas_manifest = output_root / "delivery-wrong-canvas.json"
        wrong_canvas_manifest.write_text(json.dumps({"files": wrong_canvas_files}), encoding="utf-8")
        run(str(ROOT / "scripts" / "validate_delivery.py"),
            str(fixtures / "valid-bilingual-lecture.json"),
            str(wrong_canvas_manifest), "--output-root", str(output_root), expected=1)

    # Missing English must fail even when a caller supplies a stale Chinese-only brief.
    import importlib.util
    module_spec = importlib.util.spec_from_file_location("delivery", ROOT / "scripts" / "validate_delivery.py")
    delivery = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(delivery)
    # Fixed academic template: humanities win over digital methods, uncertainty
    # defaults to calligraphy, while computing-only subjects use bitmap titles.
    academic_spec = importlib.util.spec_from_file_location(
        "academic_assets", ROOT / "assets/category-templates/academic-forum/scripts/check_assets.py")
    academic = importlib.util.module_from_spec(academic_spec)
    academic_spec.loader.exec_module(academic)
    assert academic.choose_title("数字人文与文化遗产保护")['font_key'] == 'humanities'
    assert academic.choose_title("计算机系统与数字算法")['font_key'] == 'digital'
    assert academic.choose_title("跨领域学术交流")['font_key'] == 'humanities'
    assert academic.check("文化遗产与数字技术")['valid']
    assert academic.SPEC['canvas']['width'] * 5 == academic.SPEC['canvas']['height'] * 4
    background_spec = importlib.util.spec_from_file_location(
        "academic_background", ROOT / "assets/category-templates/academic-forum/scripts/background.py")
    background = importlib.util.module_from_spec(background_spec)
    background_spec.loader.exec_module(background)
    palette = academic.SPEC['default_palette']
    assert background.contrast(background.rgb(palette['ink']), background.rgb(palette['background_top'])) >= 4.5
    assert background.contrast(background.rgb(palette['ink']), background.rgb(palette['background_bottom'])) >= 4.5
    assert academic.SPEC['background_policy']['reference_locks'] == 'typography_only'
    title_spec = importlib.util.spec_from_file_location(
        "academic_title", ROOT / "assets/category-templates/academic-forum/scripts/title.py")
    title = importlib.util.module_from_spec(title_spec)
    title_spec.loader.exec_module(title)
    assert title.display_title({'title_lines':['2026年全球论坛'],'dates':'2026.11.06'})[0] == ['全球论坛']
    assert title.display_title({'title_lines':['2026 Global Forum'],'year_label':'FORUM 2026'})[0] == ['Global Forum']
    assert title.display_title({'title_lines':['2026论坛'],'dates':'11月6日'})[0] == ['2026论坛']
    assert title.display_title({'title_lines':['第五届论坛','12位嘉宾'],'dates':'2026.11.06'})[0] == ['第五届论坛','12位嘉宾']
    assert title.display_title({'title_lines':['第2026届论坛'],'year_label':'2026'})[0] == ['第2026届论坛']
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        write_png_header(temp / "zh.png", 2400, 3000)
        (temp / "en.svg").write_text("<svg/>")
        brief = json.loads((fixtures / "valid-bilingual-lecture.json").read_text())
        brief["languages"]["required"] = ["zh-CN"]
        brief["deliverables"]["formats"] = ["png", "svg"]
        files = [{"path": "zh.png", "language": "zh-CN", "width_px": 2400, "height_px": 3000, "status": "final"}]
        errors, _ = delivery.validate(brief, {"files": files}, temp)
        assert any("language 'en'" in error for error in errors)
        files.append({"path": "en.svg", "language": "en", "width_px": 2400, "height_px": 3000, "status": "final"})
        errors, _ = delivery.validate(brief, {"files": files}, temp)
        assert any("language 'en'" in error for error in errors), "English SVG cannot replace the English poster"

    run(str(ROOT / "scripts" / "check_internal_links.py"), str(ROOT))
    print("PASS: all smoke tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
