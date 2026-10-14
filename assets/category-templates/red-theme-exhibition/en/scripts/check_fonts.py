from pathlib import Path
import json, hashlib, sys
try:
 from fontTools.ttLib import TTFont
except ImportError:
 print('请先运行 pip install fonttools'); sys.exit(2)
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'references/font-manifest.json').read_text('utf-8'))
failed=0
for entry in manifest['fonts']:
 if entry.get('status')=='unavailable':
  print('UNAVAILABLE (not eligible for layout)',entry['family'],entry.get('reason',''));continue
 path=root/entry['file']
 if not path.is_file():print('MISSING',path);failed+=1;continue
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 try:
  f=TTFont(path,lazy=True)
  cp=set()
  for t in f['cmap'].tables:
   if t.isUnicode(): cp.update(t.cmap.keys())
  f.close()
  test='百年征程初心如磐历史人物档案展览2026' if entry['covers_cjk'] else 'THE FANTASTIC FOREST ADVENTURE 2026'
  missing=''.join(sorted({c for c in test if not c.isspace() and ord(c) not in cp}))
  ok=(digest==entry['sha256'] and not missing)
  print('OK' if ok else 'FAIL',entry['family'],path.name,'hash',digest==entry['sha256'],'missing',missing or 'none')
  if not ok:failed+=1
 except Exception as e: print('INVALID FONT',path,e);failed+=1
print('AVAILABLE FONT CHECK', 'PASS' if not failed else f'FAIL {failed}')
sys.exit(1 if failed else 0)
