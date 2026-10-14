"""Check packaged font bytes, relative references and production resources."""
from pathlib import Path
import hashlib
import json
import re


def main():
    root = Path(__file__).resolve().parents[1]
    spec = json.loads((root / 'references/layout-spec.json').read_text(encoding='utf-8'))
    manifest = json.loads((root / 'references/font-assets.json').read_text(encoding='utf-8'))
    directory = root / spec['fontDirectory']
    assert spec['fontDirectory'] == manifest['fontDirectory'], 'Font directory mismatch'
    for item in manifest['fonts']:
        data = (directory / item['file']).read_bytes()
        assert len(data) == item['bytes'], 'Font size mismatch: ' + item['file']
        assert data[:4] in (b'\x00\x01\x00\x00', b'OTTO'), 'Invalid font: ' + item['file']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], 'Font checksum mismatch: ' + item['file']
    expected = {item['file'] for item in manifest['fonts']}
    assert expected == {value[0] for value in spec['fonts'].values()}, 'Font registry differs from manifest'
    for md in [root / 'SKILL.md', *root.glob('references/*.md')]:
        for target in re.findall(r'\]\(([^)]+)\)', md.read_text(encoding='utf-8')):
            if not target.startswith(('http:', 'https:', '#')):
                assert (md.parent / target).exists(), f'Missing resource: {md.name} -> {target}'
    for name in ['render_typography.cjs', 'build_overlap_mask.cjs', 'compose_poster.py']:
        assert (root / 'scripts' / name).is_file(), 'Missing production script: ' + name
    for file in root.glob('references/*.json'):
        json.loads(file.read_text(encoding='utf-8'))
    print('PASS: six real Harmony fonts, matching registry, checksums, references and production scripts')


if __name__ == '__main__':
    main()
