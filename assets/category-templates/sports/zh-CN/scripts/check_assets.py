from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]
spec = json.loads((root / 'references/layout-spec.json').read_text(encoding='utf-8'))
manifest = json.loads((root / 'references/font-assets.json').read_text(encoding='utf-8'))
for item in manifest['fonts']:
    data = (root / spec['fontDirectory'] / item['file']).read_bytes()
    assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'], item['file']
assert {v[0] for v in spec['fonts'].values()} == {v['file'] for v in manifest['fonts']}
for md in [root / 'SKILL.md', *root.glob('references/*.md')]:
    for link in re.findall(r'\]\(([^)]+)\)', md.read_text(encoding='utf-8')):
        if not link.startswith(('https:', 'http:', '#')):
            assert (md.parent / link).exists(), link
for file in root.glob('references/*.json'):
    json.loads(file.read_text(encoding='utf-8'))
assert (root / 'scripts/render_layout.cjs').is_file()
print('PASS: fonts, reference images, linked resources, layout examples and renderer')
