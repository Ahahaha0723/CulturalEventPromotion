"""Resolve a red-theme manifest font to a checked absolute path for prompt/layout plans."""
import argparse
import hashlib
import json
from pathlib import Path


def resolve(root, family, weight, text):
    from fontTools.ttLib import TTFont
    root = Path(root).resolve()
    manifest_path = root / 'references/font-manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    matches = [r for r in manifest['fonts'] if r['family'] == family and r['weight'] == weight]
    if len(matches) != 1:
        raise ValueError('Select one manifest family/weight; no implicit replacement.')
    row = matches[0]
    if row.get('status') != 'bundled':
        raise ValueError('Font is not available: ' + family)
    skill_root = root.parents[3]  # assets/category-templates/<category>/<language>
    font_path = (root / row['file']).resolve()
    license_path = (root / row['license_file']).resolve()
    for path in [font_path, license_path]:
        if not path.is_relative_to(skill_root) or not path.is_file():
            raise ValueError('Missing or out-of-skill resource: ' + str(path))
    sha = hashlib.sha256(font_path.read_bytes()).hexdigest()
    if sha != row['sha256']:
        raise ValueError('Font SHA256 mismatch: ' + str(font_path))
    license_sha = hashlib.sha256(license_path.read_bytes()).hexdigest()
    if row.get('license_sha256') and license_sha != row['license_sha256']:
        raise ValueError('License SHA256 mismatch: ' + str(license_path))
    with TTFont(font_path) as font:
        cmap = font.getBestCmap() or {}
        missing = sorted({c for c in text if not c.isspace() and not cmap.get(ord(c))})
        if missing:
            raise ValueError('Missing glyphs; no silent fallback: ' + json.dumps(missing, ensure_ascii=False))
        names = {str(i): sorted({r.toUnicode() for r in font['name'].names if r.nameID == i})
                 for i in [1, 2, 4, 5, 6]}
        actual_weight = font['OS/2'].usWeightClass
    return {'family': family, 'weight': weight, 'font_file': str(font_path),
            'license_file': str(license_path), 'sha256': sha, 'license_sha256': license_sha,
            'manifest_file': str(manifest_path), 'internal_names': names,
            'actual_weight': actual_weight, 'text': text, 'all_glyphs_present': True,
            'scope': 'Path/hash/glyph binding; render and review typography separately.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--family', required=True)
    parser.add_argument('--weight', required=True)
    parser.add_argument('--output', type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text')
    group.add_argument('--text-file', type=Path)
    args = parser.parse_args()
    try:
        text = args.text if args.text is not None else args.text_file.read_text(encoding='utf-8-sig')
        result = resolve(args.root, args.family, args.weight, text)
        encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            output = args.output.resolve()
            module_root = args.root.resolve()
            skill_root = module_root.parents[3]
            if output.is_relative_to(skill_root):
                raise ValueError('Write project bindings outside the skill resource directory.')
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(encoded, encoding='utf-8')
        print(encoded, end='')
    except (OSError, ValueError, KeyError, ImportError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
