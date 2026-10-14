"""Verify an explicitly selected reference font; never silently substitute another."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from font_engine import Font
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    p.add_argument('--font-id',required=True)
    t=p.add_mutually_exclusive_group(required=True);t.add_argument('--text');t.add_argument('--text-file',type=Path)
    a=p.parse_args()
    try:
        root=a.root.resolve();catalog=json.loads((root/'assets/fonts/catalog.json').read_text(encoding='utf-8'))
        records=[r for r in catalog['fonts'] if r['id']==a.font_id]
        if len(records)!=1:raise ValueError('Unknown or duplicate font ID')
        rec=records[0];file=(root/rec['file']).resolve();license=(root/rec['license_file']).resolve()
        allowed_root = root.parents[3] if root.parents[1].name == 'category-templates' and root.parents[2].name == 'assets' and root.parents[3].name == 'cultural-event-poster' else root
        if not file.is_relative_to(allowed_root) or not license.is_relative_to(allowed_root):raise ValueError('Font/license escapes skill package')
        if hashlib.sha256(file.read_bytes()).hexdigest()!=rec['sha256']:raise ValueError('Font checksum mismatch')
        if hashlib.sha256(license.read_bytes()).hexdigest()!=rec['license_sha256']:raise ValueError('License checksum mismatch')
        text=a.text if a.text is not None else a.text_file.read_text(encoding='utf-8-sig')
        font=Font(file);missing=font.missing(text)
        if missing:raise ValueError('Chosen font lacks glyphs: '+''.join(missing)+'; no fallback performed')
        print(json.dumps({'font_id':a.font_id,'file':str(file),'sha256':rec['sha256'],'internal_font':font.info()['names'],'all_glyphs_present':True,'fallback_used':False,'aesthetic_match':'requires source/candidate comparison; not proved by glyph coverage','source_font_identity':'not asserted'},ensure_ascii=False,indent=2));return 0
    except (OSError,ValueError,KeyError) as e:
        print(json.dumps({'error':str(e),'fallback_performed':False},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
