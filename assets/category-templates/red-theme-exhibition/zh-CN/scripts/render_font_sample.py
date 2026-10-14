from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys
root=Path(__file__).resolve().parents[1]
fonts=json.loads((root/'references/font-manifest.json').read_text('utf-8'))['fonts']
fonts=[v for v in fonts if v.get('status')!='unavailable']
def font_path(family,weight):
 return root/next(v['file'] for v in fonts if v['family']==family and v['weight']==weight)
canvas=Image.new('RGB',(1500,130+len(fonts)*155),'#F8F5F0'); d=ImageDraw.Draw(canvas)
d.text((60,35),'RED THEME FONT SAMPLE | REAL FONT FILES',font=ImageFont.truetype(str(font_path('nunito','bold')),42),fill='#4b2524')
for i,v in enumerate(fonts):
 y=130+i*155
 font=ImageFont.truetype(str(root/v['file']),48)
 label=f"{v['family']} — {v['weight']}"
 d.text((60,y),label,font=ImageFont.truetype(str(font_path('nunito','regular')),23),fill='#555555')
 phrase='百年征程 初心如磐' if v['covers_cjk'] else 'THE FANTASTIC FOREST'
 d.text((60,y+32),phrase,font=font,fill='#6D2525')
out=Path(sys.argv[1]) if len(sys.argv)>1 else root/'font-render-sample.png'
out.parent.mkdir(parents=True,exist_ok=True);canvas.save(out)
print('Rendered',out)
