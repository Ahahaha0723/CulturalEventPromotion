from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys
def render(package):
 p=Path(package);en=json.loads((p/'content.json').read_text(encoding='utf-8'))['language']=='en'
 im=Image.open(p/'background.png').convert('RGB').resize((2400,3200),Image.Resampling.LANCZOS);d=ImageDraw.Draw(im)
 cream='#F1E5C9';gold='#D4AA64';bounds=[]
 def ft(size,kind):
  f=ImageFont.truetype(str(p/'fonts'/{'zh':'NotoSerifSC.ttf','title':'MaShanZheng-Regular.ttf','en':'BodoniModa.ttf','sans':'Inter.ttf'}[kind]),size)
  if kind=='zh':f.set_variation_by_axes([500])
  if kind=='en':f.set_variation_by_axes([400,36])
  if kind=='sans':f.set_variation_by_axes([32,400])
  return f
 def t(s,x,y,size,kind='zh',color=cream):
  f=ft(size,kind);d.text((x,y),s,font=f,fill=color,anchor='lt');bounds.append((s,d.textbbox((x,y),s,font=f,anchor='lt')))
 if en:
  t('DUNHUANG',150,180,113,'en',gold);t('ON THE',170,365,132,'en',gold);t('WALL',155,545,221,'en',gold)
  d.line((170,850,920,850),fill=gold,width=2)
  t('TRACE THE PAINTED WALLS.',170,930,30,'sans',gold)
  t('HEAR THE ECHO OF CENTURIES.',170,990,29,'sans',gold)
 else:
  for ch,y in zip('壁上敦煌',[120,475,830,1185]):t(ch,160,y,310,'title',gold)
  t('Dunhuang',655,560,48,'en');t('on the Wall',655,625,43,'en')
  t('循壁上丹青，见千年回响',140,1795,43,'zh',gold)
 x=1450
 if en:
  t('DUNHUANG CAVE MURALS',x,1710,42,'en')
  t('ART & CONSERVATION',x,1775,48,'en')
  t('THEMATIC EXHIBITION',x,1840,44,'en')
  t('Images & reproductions',x,1930,28,'sans',gold)
  t('No original murals on display',x,1980,27,'sans',gold)
 else:
  t('敦煌石窟壁画',x,1740,81);t('艺术与保护主题展',x,1855,73)
  t('图像与复制展示 · 非原作展',x,1990,31,'zh',gold)
 d.line((x,2090,2220,2090),fill=gold,width=1)
 t('EXHIBITION DATES' if en else '展览时间  Dates',x,2150,28,'sans' if en else 'zh',gold)
 t('05 DEC 2026' if en else '2026.12.05',x,2220,69 if en else 86,'en')
 t('— 10 JAN 2027' if en else '— 2027.01.10',x,2320,65 if en else 76,'en')
 t('Daily 10:00–18:00' if en else '每日10:00—18:00',x,2440,31 if en else 35,'sans' if en else 'zh')
 t('Last entry 17:30' if en else '17:30停止入场',x,2495,31 if en else 35,'sans' if en else 'zh')
 t('EXHIBITION VENUE' if en else '展览地点  Venue',x,2610,28,'sans' if en else 'zh',gold)
 if en:
  t('Silk Road Art',x,2670,49,'en');t('Exhibition Hall',x,2730,49,'en')
  t('Jing’an District, Shanghai',x,2805,29,'sans')
  t('Fictional venue · Free admission',x,2860,27,'sans',gold)
  t('Guided tours: see on-site schedule',x,2915,26,'sans')
 else:
  t('上海市静安区',x,2670,55);t('丝路艺术专题展厅',x,2750,55)
  t('虚构场地 · 免费入场',x,2840,32,'zh',gold);t('导览按现场公布的场次参加',x,2895,30)
 d.line((170,3040,2220,3040),fill=gold,width=1)
 t('Host: City Silk Road Art Exhibition Centre (fictional)' if en else '主办方：城市丝路艺术展览中心（虚构机构）',170,3090,24 if en else 28,'sans' if en else 'zh')
 t('Simulated event · Concept design' if en else '模拟活动 · 概念设计',1740 if en else 1870,3145 if en else 3090,24 if en else 27,'sans' if en else 'zh',gold)
 for s,b in bounds:assert b[2]<2340 and b[3]<3190,(s,b)
 im.save(p/f'poster-{"en" if en else "zh"}.png')
 (p/'qa.json').write_text(json.dumps({'canvas':[2400,3200],'text_bounds':'pass','fictional_notices':'retained','source_fonts':'unidentified; open-source substitutes used','status':'concept, not a real exhibition announcement'},indent=2),encoding='utf-8')
if __name__=='__main__':render(sys.argv[1])
