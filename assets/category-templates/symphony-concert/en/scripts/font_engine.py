"""Inspect SFNT fonts and choose only candidates covering the complete supplied text.
Uses Python's standard library; does not install fonts or contact the network.
"""
import argparse, hashlib, json, struct
from pathlib import Path

def u16(b,o):return struct.unpack_from('>H',b,o)[0]
def s16(b,o):return struct.unpack_from('>h',b,o)[0]
def u32(b,o):return struct.unpack_from('>I',b,o)[0]

class Font:
    def __init__(self,path):
        self.path=Path(path);self.b=self.path.read_bytes()
        if self.b[:4] not in (b'OTTO',b'\x00\x01\x00\x00'):raise ValueError('Unsupported SFNT: '+str(path))
        self.tables={}
        for i in range(u16(self.b,4)):
            p=12+i*16;tag=self.b[p:p+4].decode('ascii');offset,length=u32(self.b,p+8),u32(self.b,p+12)
            if offset+length>len(self.b):raise ValueError('Truncated table: '+tag)
            self.tables[tag]=self.b[offset:offset+length]
        if not {'name','cmap','head','maxp'}.issubset(self.tables):raise ValueError('Missing font tables')
        self.cmaps=[];b=self.tables['cmap']
        for i in range(u16(b,2)):
            p=4+i*8;platform,encoding,offset=u16(b,p),u16(b,p+2),u32(b,p+4)
            if platform==0 or (platform==3 and encoding in (1,10)):
                fmt=u16(b,offset)
                if fmt in (4,12):self.cmaps.append((fmt,b[offset:]))
        if not self.cmaps:raise ValueError('No supported Unicode cmap')
    def glyph(self,cp):
        for fmt,b in self.cmaps:
            if fmt==12:
                lo,hi=0,u32(b,12)-1
                while lo<=hi:
                    mid=(lo+hi)//2;p=16+mid*12;start,end,gid=u32(b,p),u32(b,p+4),u32(b,p+8)
                    if cp<start:hi=mid-1
                    elif cp>end:lo=mid+1
                    else:return gid+cp-start
            elif cp<=0xffff:
                n=u16(b,6)//2;ends=14;starts=16+2*n;deltas=16+4*n;ranges=16+6*n
                for i in range(n):
                    if cp>u16(b,ends+2*i):continue
                    if cp<u16(b,starts+2*i):break
                    delta=s16(b,deltas+2*i);ro=u16(b,ranges+2*i)
                    if not ro:return (cp+delta)&0xffff
                    at=ranges+2*i+ro+2*(cp-u16(b,starts+2*i))
                    gid=u16(b,at) if at+2<=len(b) else 0
                    return (gid+delta)&0xffff if gid else 0
        return 0
    def missing(self,text):return sorted({c for c in text if not c.isspace() and not self.glyph(ord(c))})
    def info(self):
        b=self.tables['name'];count,strings=u16(b,2),u16(b,4);names={}
        for i in range(count):
            p=6+i*12;platform,encoding,lang,nid,length,offset=struct.unpack_from('>6H',b,p)
            if nid not in (1,2,4,6):continue
            raw=b[strings+offset:strings+offset+length]
            try:value=raw.decode('utf-16-be' if platform in (0,3) else 'mac_roman')
            except UnicodeError:continue
            if str(nid) not in names or lang==0x409:names[str(nid)]=value
        weight=u16(self.tables['OS/2'],4) if 'OS/2' in self.tables else None
        axes=[]
        if 'fvar' in self.tables:
            b=self.tables['fvar'];start,count,size=u16(b,4),u16(b,8),u16(b,10)
            for i in range(count):
                p=start+i*size;tag=b[p:p+4].decode('ascii')
                axes.append({'tag':tag,'min':struct.unpack_from('>i',b,p+4)[0]/65536,'default':struct.unpack_from('>i',b,p+8)[0]/65536,'max':struct.unpack_from('>i',b,p+12)[0]/65536})
        return {'names':names,'weight':weight,'axes':axes,'glyph_count':u16(self.tables['maxp'],4),'sha256':hashlib.sha256(self.b).hexdigest()}

def select(root,profile,language,role,text):
    root=Path(root);catalog=json.loads((root/'assets/fonts/catalog.json').read_text(encoding='utf-8'))
    profiles=json.loads((root/'assets/fonts/role-profiles.json').read_text(encoding='utf-8'))
    if profile not in profiles['profiles']:raise ValueError('Unknown profile: '+profile)
    candidates=profiles['profiles'][profile]['languages'][language][role]
    failed=[]
    for fontid in candidates:
        rec=next(x for x in catalog['fonts'] if x['id']==fontid)
        f=Font(root/rec['file']);actual=f.info()['sha256']
        if actual!=rec['sha256']:raise ValueError('Font checksum mismatch: '+rec['file'])
        missing=f.missing(text)
        if missing:failed.append({'font_id':fontid,'missing':missing});continue
        return {'selected':fontid,'file':str((root/rec['file']).resolve()),'family':rec['family'],'internal_font':f.info()['names'],'weight':f.info()['weight'],'axes':f.info()['axes'],'profile':profile,'language':language,'role':role,'fallback_used':bool(failed),'rejected_candidates':failed,'all_glyphs_present':True,'scope':'coverage-compatible candidate; aesthetic fit requires rendered review'}
    raise ValueError('No bundled candidate covers this text: '+json.dumps(failed,ensure_ascii=False))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    p.add_argument('--profile',required=True);p.add_argument('--language',choices=['zh-CN','en'],required=True)
    p.add_argument('--role',choices=['title','subtitle','body','numeric'],required=True)
    t=p.add_mutually_exclusive_group(required=True);t.add_argument('--text');t.add_argument('--text-file',type=Path)
    a=p.parse_args();text=a.text if a.text is not None else a.text_file.read_text(encoding='utf-8-sig')
    try:print(json.dumps(select(a.root,a.profile,a.language,a.role,text),ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,StopIteration) as e:print(json.dumps({'error':str(e)},ensure_ascii=False));return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
