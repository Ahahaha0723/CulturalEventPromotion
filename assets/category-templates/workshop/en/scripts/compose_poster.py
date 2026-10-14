"""Compose vector art and real glyphs with partial white text at dark intersections.

python compose_poster.py typography-outlined.svg text-clearance-mask.svg artwork.svg output.svg [node-executable] [sharp-module-path]
The clearance argument is retained for old callers; whole-text clearance is disabled.
"""
from pathlib import Path
import base64
import copy
import json
import subprocess
import sys
import xml.etree.ElementTree as ET


def main():
    if not 5 <= len(sys.argv) <= 7:
        raise SystemExit(__doc__)
    type_path, mask_path, art_path, output_path = map(Path, sys.argv[1:5])
    spec = json.loads((Path(__file__).resolve().parents[1] / "references/layout-spec.json").read_text(encoding="utf-8"))
    width, height = spec["canvas"]["width"], spec["canvas"]["height"]
    ns = "http://www.w3.org/2000/svg"
    tag = lambda name: "{" + ns + "}" + name
    ET.register_namespace("", ns)
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    root = ET.Element(tag("svg"), {"width": str(width), "height": str(height), "viewBox": f"0 0 {width} {height}"})
    ET.SubElement(root, tag("rect"), {"width": str(width), "height": str(height), "fill": spec["canvas"]["background"]})
    definitions = ET.SubElement(root, tag("defs"))
    art = ET.parse(art_path).getroot()
    viewbox = art.get("viewBox", "").replace(",", " ").split()
    if len(viewbox) != 4 or list(map(float, viewbox)) != [0, 0, width, height]:
        raise ValueError("Artwork must use the matching canvas/viewBox; do not stretch an unrelated image.")
    for element in art.iter():
        if element.tag.endswith("text"):
            raise ValueError("Abstract artwork must not contain generated formal lettering.")
        href = element.get("href") or element.get("{http://www.w3.org/1999/xlink}href")
        if href and not href.startswith(("data:", "#")):
            raise ValueError("Embed external image resources before composition.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    coverage_path = output_path.with_suffix(".overlap-mask.png")
    report_path = output_path.with_suffix(".overlap-report.json")
    node = sys.argv[5] if len(sys.argv) > 5 else "node"
    command = [node, str(Path(__file__).with_name("build_overlap_mask.cjs")),
               str(art_path), str(type_path), str(coverage_path), str(report_path)]
    if len(sys.argv) > 6:
        command.append(sys.argv[6])
    subprocess.run(command, check=True)
    mask = ET.SubElement(definitions, tag("mask"), {"id":"dark-art-intersection",
        "maskUnits":"userSpaceOnUse", "x":"0", "y":"0", "width":str(width),
        "height":str(height), "style":"mask-type:alpha"})
    ET.SubElement(mask, tag("image"), {"width":str(width), "height":str(height),
        "href":"data:image/png;base64," + base64.b64encode(coverage_path.read_bytes()).decode("ascii")})
    graphic = ET.SubElement(root, tag("g"), {"id": "mother-text-abstract"})
    for child in art:
        if child.tag == tag("defs"):
            for definition in child:
                definitions.append(definition)
        else:
            graphic.append(child)
    typography = ET.SubElement(root, tag("g"), {"id": "harmony-chinese-typography"})
    white_type = ET.SubElement(root, tag("g"), {"id":"overlapping-glyph-portions-white", "mask":"url(#dark-art-intersection)"})
    for child in ET.parse(type_path).getroot():
        typography.append(copy.deepcopy(child))
        overlay = copy.deepcopy(child)
        for element in overlay.iter():
            if "fill" in element.attrib and element.get("fill") != "none":
                element.set("fill", "#FFFFFF")
            if "id" in element.attrib:
                element.set("id", "white-" + element.get("id"))
        white_type.append(overlay)
    ET.ElementTree(root).write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Composed poster SVG: {output_path}")


if __name__ == "__main__":
    main()
