from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,sys
def render(package):
    p=Path(package);cfg=json.loads((p/'content.json').read_text(encoding='utf-8'));en=cfg['language']=='en'
    im=Image.open(p/'background.png').convert('RGB').resize((1536,2048),Image.Resampling.LANCZOS)
    d=ImageDraw.Draw(im);black='#101610';green='#A5FF63';white='#FAFCF7'
    def f(size,bold=False,zh=False):
        ft=ImageFont.truetype(str(p/'fonts'/('NotoSansSC.ttf' if zh else 'Inter.ttf')),size)
        ft.set_variation_by_axes([900 if bold else 400] if zh else [32,750 if bold else 400])
        return ft
    bounds=[]
    def t(s,x,y,size,bold=False,zh=False):
        ft=f(size,bold,zh);d.text((x,y),s,font=ft,fill=black,anchor='lt')
        b=d.textbbox((x,y),s,font=ft,anchor='lt');bounds.append((s,b))
    def box(x,y,w,h,color=white):d.rectangle((x,y,x+w,y+h),fill=color)
    def dash(x1,y1,x2,y2):
        import math
        length=math.hypot(x2-x1,y2-y1)
        for step in range(0,int(length),19):
            a=step/length;b=min(step+9,length)/length
            d.line((x1+(x2-x1)*a,y1+(y2-y1)*a,x1+(x2-x1)*b,y1+(y2-y1)*b),fill='#69716B',width=1)
    box(96,83,42,15,green);t('UNSEEN REALMS',160,77,31,True)
    box(1060,64,378,49);t('GENERATIVE ART',1073,80,26)
    t('AND PERCEPTION',1090,137,24)
    if en:
        t('UNSEEN',88,251,170,True);t('REALMS',327,491,174,True)
        box(105,768,715,110);t('GENERATIVE ART &',120,785,34,True);t('PERCEPTION EXPERIMENTS',120,832,34,True)
    else:
        t('未见',87,235,245,True,True);t('之境',395,493,245,True,True)
        box(105,768,705,77);t('生成艺术与感知实验展',120,789,44,True,True)
    d.ellipse((833,782,1107,1056),outline=green,width=17)
    d.line((825,1050,1125,785),fill=green,width=23)
    box(91,892,18,18,black);dash(100,918,100,1368);box(91,1368,18,18,black)
    dash(100,1040,565,1040);box(140,1060,316,45);t('DATA → LANDSCAPE',152,1072,27)
    box(365,1262,853,67)
    t('See new possibilities in change.' if en else '在变化之中，看见另一种可能',383,1281,35 if en else 39,False,not en)
    box(368,1341,176,8,green)
    dash(100,1492,1440,1492);box(1430,1483,23,23,black)
    t('2026',102,1528,38,True)
    t('21 NOV — 20 DEC' if en else '11.21 — 12.20',100,1610,76 if en else 83,True)
    box(1178,1578,263,64,green);t('FREE ENTRY' if en else '免费入场',1195,1596,30 if en else 36,True,not en)
    box(100,1690,1050 if en else 870,57)
    t('Daily 10:00–21:00 / Last entry 20:30' if en else '每日10:00—21:00 / 20:30停止入场',112,1706,31,False,not en)
    t('BOUNDARY DIGITAL ART SPACE' if en else '上海市徐汇区 · 边界数字艺术空间',110,1794,36 if en else 37,True,not en)
    if en:
        t('Xuhui District, Shanghai',110,1851,28)
        t('Fictional venue / Queue on site for interactive areas',110,1900,24)
    else:t('虚构场地 / 互动区域现场排队',110,1857,29,False,True)
    d.line((100,1940,1440,1940),fill='#7B827B',width=1)
    t('Host: Boundary Digital Art Lab (fictional)' if en else '主办方：边界数字艺术研究室（虚构机构）',110,1964,23,False,not en)
    t('Generative imagery / Dynamic projections / Audience participation' if en else '生成影像 / 动态投影 / 观众参与',110,2012,18 if en else 23,False,not en)
    t('Simulated event · Concept design' if en else '模拟活动 · 概念设计',1110 if en else 1190,2012,18 if en else 23,False,not en)
    for s,b in bounds:assert b[2]<1500 and b[3]<2048,(s,b)
    im.save(p/('poster-en.png' if en else 'poster-zh.png'))
    (p/'qa.json').write_text(json.dumps({'size':im.size,'text_bounds':'pass','fictional_notices':'retained','fonts':['Inter','Noto Sans SC'],'font_origin':'open-source substitutes; original font unidentified'},indent=2),encoding='utf-8')
if __name__=='__main__':render(sys.argv[1])
