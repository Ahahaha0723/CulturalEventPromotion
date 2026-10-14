"""Compose an upstream-approved type layer with a gradient/abstract scene SVG.
python compose_scene.py typography.svg scene.svg output.svg
"""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 4:
    raise SystemExit(__doc__)
type_path, scene_path, output = map(Path, sys.argv[1:])
ns = 'http://www.w3.org/2000/svg'
tag = lambda name: '{' + ns + '}' + name
ET.register_namespace('', ns)
scene, typography = ET.parse(scene_path).getroot(), ET.parse(type_path).getroot()
for dimension in ['width', 'height']:
    if float(scene.get(dimension)) != float(typography.get(dimension)):
        raise ValueError('Scene and typography canvas dimensions must match')
for source in [scene, typography]:
    for element in source.iter():
        href = element.get('href') or element.get('{http://www.w3.org/1999/xlink}href')
        if href and not href.startswith(('data:', '#')):
            raise ValueError('Embed external resources before composition')
root = ET.Element(tag('svg'), dict(scene.attrib))
for child in scene:
    root.append(child)
layer = ET.SubElement(root, tag('g'), {'id': 'upstream-approved-typography'})
for child in typography:
    layer.append(child)
output.parent.mkdir(parents=True, exist_ok=True)
ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
print('Composed gradient, abstract hero and actual typography:', output)
