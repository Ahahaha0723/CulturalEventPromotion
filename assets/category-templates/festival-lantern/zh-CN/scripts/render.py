from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,sys
def render(package):
 p=Path(package);c=json.loads((p/'content.json').read_text(encoding='utf-8'));en=c['language']=='en'
 im=Image.open(p/'background.png').convert('RGB').resize((2400,3200),Image.Resampling.LANCZOS);d=ImageDraw.Draw(im)
 cream='#F4EAD3';red='#98251E'
 def f(size,style='serif'):
  ft=ImageFont.truetype(str(p/'fonts'/{'serif':'BodoniModa.ttf','sans':'Inter.ttf','zh':'NotoSerifSC.ttf'}[style]),size)
  ft.set_variation_by_axes([400,80] if style=='serif' else ([32,400] if style=='sans' else [400]))
  return ft
 bounds=[]
 def text(s,x,y,size,style='serif',color=cream,anchor='lt'):
  ft=f(size,style);d.text((x,y),s,font=ft,fill=color,anchor=anchor);bounds.append((s,d.textbbox((x,y),s,font=ft,anchor=anchor)))
 def track(s,x,y,size,gap,style='sans',color=cream):
  ft=f(size,style)
  for ch in s:
   d.text((x,y),ch,font=ft,fill=color,anchor='lt');x+=d.textlength(ch,font=ft)+gap
 text('2027',1200,155,90,color=red,anchor='mt')
 text('DINGWEI · YEAR OF THE GOAT' if en else '丁 未 羊 年',1200,282,24 if en else 28,'sans' if en else 'zh',red,'mt')
 track('SPRING FESTIVAL',970,1758,25,5)
 text('YEAR',965,1840,155);text('OF THE',976,2012,66);text('GOAT',953,2110,242)
 if en:
  track('GRACE IN STILLNESS',980,2438,28,4)
  track('A YEAR OF HARMONY',983,2512,23,3)
 else:
  track('温润成祥',980,2425,47,18,'zh');track('GRACE IN STILLNESS',983,2512,24,4)
 d.line((260,2790,2020,2790),fill=cream,width=1)
 track('HAPPY CHINESE',260,2860,33,4);track('NEW YEAR',260,2926,33,4)
 if en:
  track('PEACE FOR THE NEW YEAR',1350,2860,25,2)
  text('May warmth and quiet strength fill the year.',1350,2930,25,'sans')
 else:
  track('新春安宁 · 万象和合',1350,2860,29,5,'zh');text('愿新岁温暖，亦有从容的力量。',1350,2930,28,'zh')
 track('CHINESE NEW YEAR  /  2027',260,3070,21,3)
 text('SPRING FESTIVAL' if en else '羊 年 · 春 节',2020,3066,24 if en else 28,'sans' if en else 'zh',anchor='rt')
 for s,b in bounds:assert b[0]>=0 and b[2]<2310 and b[3]<3170,(s,b)
 im.save(p/('poster-en.png' if en else 'poster-zh.png'))
 (p/'qa.json').write_text(json.dumps({'size':[2400,3200],'text_bounds':'pass','fonts':['Bodoni Moda','Inter','Noto Serif SC'],'status':'digital art concept; no event or brand invented'},indent=2),encoding='utf-8')
if __name__=='__main__':render(sys.argv[1])
