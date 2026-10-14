from pathlib import Path
import hashlib,json,re,struct
root=Path(__file__).resolve().parents[1]
def glyph_lookup(data):
    tables={}
    for i in range(struct.unpack_from('>H',data,4)[0]):
        tag,_,offset,length=struct.unpack_from('>4sIII',data,12+i*16);tables[tag]=offset
    base=tables[b'cmap'];subs=[]
    for i in range(struct.unpack_from('>H',data,base+2)[0]):
        platform,encoding,off=struct.unpack_from('>HHI',data,base+4+i*8)
        if platform in (0,3):subs.append(base+off)
    def glyph(cp):
        for s in subs:
            fmt=struct.unpack_from('>H',data,s)[0]
            if fmt==12:
                for k in range(struct.unpack_from('>I',data,s+12)[0]):
                    lo,hi,g=struct.unpack_from('>III',data,s+16+k*12)
                    if lo<=cp<=hi:return g+cp-lo
            if fmt==4 and cp<=65535:
                seg=struct.unpack_from('>H',data,s+6)[0]//2
                ep=s+14;sp=ep+2*seg+2;dp=sp+2*seg;rp=dp+2*seg
                for k in range(seg):
                    end=struct.unpack_from('>H',data,ep+2*k)[0];start=struct.unpack_from('>H',data,sp+2*k)[0]
                    if start<=cp<=end:
                        delta=struct.unpack_from('>h',data,dp+2*k)[0];ro=struct.unpack_from('>H',data,rp+2*k)[0]
                        if not ro:return (cp+delta)&65535
                        g=struct.unpack_from('>H',data,rp+2*k+ro+2*(cp-start))[0]
                        return (g+delta)&65535 if g else 0
        return 0
    return glyph
manifest=json.loads((root/'references/font-assets.json').read_text(encoding='utf-8'))
example=json.loads((root/'references/layout-input.example.json').read_text(encoding='utf-8'))
assert len(manifest['fonts'])==8
for f in manifest['fonts']:
    data=(root/'fonts'/f['file']).read_bytes()
    assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],f['file']
    get=glyph_lookup(data)
    chars=set('校庆周年0123456789')
    for block in example['blocks']:
        if block['font']==f['style']:chars.update(''.join(block['lines']))
    assert all(get(ord(c)) for c in chars),f['file']+' missing sample glyphs'
for file in root.glob('references/*.json'):json.loads(file.read_text(encoding='utf-8'))
for file in [root/'SKILL.md',*root.glob('references/*.md')]:
    for link in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
        if not link.startswith(('http:','https:','#')):assert (file.parent/link).exists(),link
skill=(root/'SKILL.md').read_text(encoding='utf-8')
assert skill.startswith('---\nname: university-anniversary-editorial-en\n')
assert '\ndescription: ' in skill.split('---',2)[1]
print('PASS: eight font binaries and glyph coverage, JSON, links and frontmatter')
