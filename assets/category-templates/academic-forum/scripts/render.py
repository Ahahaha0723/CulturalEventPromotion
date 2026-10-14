"""Real-font renderer for the NEW left-headline / lower-right date reference."""
from pathlib import Path
import argparse,json,re
from datetime import date
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfbase.ttfonts import TTFont
from check_assets import check,SPEC
from background import build,rgb,region_contrast
from title import display_title,packed_line

def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

class Poster:
    def __init__(self,lang,assets,brief):
        self.lang=lang;self.brief=brief;self.paths=dict(assets['fonts']);self.paths['title']=assets['decision']['font_path']
        self.im,self.palette,self.bg_record=build(brief.get('visual',{}),SPEC)
        self.background=self.im.copy();self.d=ImageDraw.Draw(self.im);self.ink=self.palette['ink']
        self.fonts={};self.maps={};self.elements=[];self.errors=[]
    def font(self,key,size):
        if (key,size) not in self.fonts:self.fonts[key,size]=ImageFont.truetype(self.paths[key],size)
        return self.fonts[key,size]
    def width(self,text,key,size):
        f=self.font(key,size);b=self.d.textbbox((0,0),text,font=f,anchor='lt')
        return max(self.d.textlength(text,font=f),b[2]-min(0,b[0]))
    def record(self,text,role,zone,key,size,box):
        if key not in self.maps:self.maps[key]=TTFont(key,self.paths[key]).face.charToGlyph
        missing=sorted(set(c for c in text if ord(c) not in self.maps[key]))
        if missing:self.errors.append(f'{role}: missing {missing}')
        x,y,w,h=SPEC[zone]
        if box[0]<x-1 or box[1]<y-1 or box[2]>x+w+1 or box[3]>y+h+1:self.errors.append(f'{role}: outside {zone}: {text}')
        self.elements.append({'text':text,'role':role,'zone':zone,'font':self.paths[key],'size':size,
                             'family':'title' if key=='title' else 'HarmonyOS Sans SC','bbox':list(box)})
    def text(self,text,x,y,key,size,role,zone):
        b=self.d.textbbox((x,y),text,font=self.font(key,size),anchor='lt')
        self.d.text((x,y),text,font=self.font(key,size),fill=self.ink,anchor='lt');self.record(text,role,zone,key,size,b)
    def wrap(self,text,key,size,width):
        zh=bool(re.search(r'[\u3400-\u9fff]',text));units=list(text) if zh else text.split()
        lines=[];line=''
        for unit in units:
            candidate=line+unit if zh else (line+' '+unit).strip()
            if line and self.width(candidate,key,size)>width:lines.append(line);line=unit
            else:line=candidate
        if line:lines.append(line)
        return lines
    def group(self,lines,zone,key,role,maximum,minimum=25):
        x,y,w,h=SPEC[zone]
        for size in range(maximum,minimum-1,-1):
            leading=round(size*1.22)
            if all(self.width(t,key,size)<=w for t in lines) and (len(lines)-1)*leading+size<=h:break
        else:raise ValueError(f'{role} cannot fit')
        for i,line in enumerate(lines):self.text(line,x,y+i*leading,key,size,role,zone)
    def headline(self,copy):
        lines,record=display_title({'title_lines':copy['headline_lines'],'dates':copy['year']})
        x,y,w,h=SPEC['title_box']
        for size in range(450,89,-1):
            measurements=[packed_line(self.font('title',size),line,0.5) for line in lines]
            leading=max(size*SPEC['title_policy']['line_advance_em'],max(b[3]-b[1] for _,b,_ in measurements)+size*0.08)
            if all(b[2]-b[0]<=w for _,b,_ in measurements) and max(i*leading+b[3]-b[1] for i,(_,b,_) in enumerate(measurements))<=h:break
        else:raise ValueError('H1 does not fit')
        heights=[b[3]-b[1] for _,b,_ in measurements]
        original_gaps=[leading-height for height in heights[:-1]]
        reduced_gaps=[gap*SPEC['title_policy']['interline_gap_factor'] for gap in original_gaps]
        tops=[0.0]
        for height,gap in zip(heights,reduced_gaps):tops.append(tops[-1]+height+gap)
        for i,(line,(positions,b,gaps)) in enumerate(zip(lines,measurements)):
            baseline=y+tops[i]-b[1];origin=x-b[0]
            for char,offset in positions:self.d.text((origin+offset,baseline),char,font=self.font('title',size),fill=self.ink,anchor='ls')
            self.record(line,'H1','title_box','title',size,[x,y+tops[i],x+b[2]-b[0],y+tops[i]+b[3]-b[1]])
        record.update({'size':size,'reference_line_advance_px':leading,'line_top_offsets_px':tops,'original_interline_gaps_px':original_gaps,'interline_gaps_px':reduced_gaps,'interline_gap_factor':SPEC['title_policy']['interline_gap_factor'],'new_reference':True,'positive_gap_factor':0.5})
        self.title_record=record
    def information(self,groups):
        x,y,w,h=SPEC['information_box']
        for size in range(46,27,-1):
            label_size=round(size*0.92);leading=round(size*1.34);gap=round(size*0.48)
            rows=[];cursor=0
            for item in groups:
                rows.append((item['label'],cursor,'body_bold',label_size,'H4-label'));cursor+=leading
                for paragraph in item['lines']:
                    for line in self.wrap(paragraph,'body_regular',size,w):
                        rows.append((line,cursor,'body_regular',size,'H4-body'));cursor+=leading
                cursor+=gap
            if cursor-gap<=h:break
        else:raise ValueError('Lower-left information does not fit')
        for text,dy,key,s,role in rows:self.text(text,x,y+dy,key,s,role,'information_box')
    def date_node(self,iso,zone):
        value=date.fromisoformat(iso);x,y,w,h=SPEC[zone]
        self.text(str(value.month),x,y,'body_regular',142,'H3-month',zone)
        self.d.line((x+70,y+210,x+235,y+35),fill=self.palette['line'],width=3)
        self.text(f'{value.day:02d}',x+230,y+94,'body_regular',155,'H3-day',zone)
        weekday=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][value.weekday()]
        self.text(weekday,x+450,y+175,'body_regular',50,'H3-weekday',zone)
    def draw(self,copy):
        self.headline(copy)
        names,_=display_title({'title_lines':copy['forum_lines'],'dates':copy['year']})
        self.group(names,'forum_name_box','body_bold','H2-forum-name',102,45)
        self.group(copy['auxiliary_lines'],'auxiliary_box','body_regular','H3-auxiliary',46,25)
        self.information(copy['groups'])
        self.group(copy['location_lines'],'location_box','body_regular','H3-location',47,28)
        self.group(copy['format_lines'],'format_box','body_regular','H3-format',35,25)
        self.date_node(copy['start_date'],'start_date_box');self.date_node(copy['end_date'],'end_date_box')
        self.group([copy['year']],'year_box','body_regular','H3-year',68,40)
        x,y,w,h=SPEC['year_box'];self.d.line((x,y+75,x+w,y+75),fill=self.palette['line'],width=4)
        self.group([copy['note']],'note_box','body_regular','note',22,18)
    def save(self,out,state,revision):
        assert len({e['font'] for e in self.elements if e['role']=='H1'})==1
        assert all(e['family']=='HarmonyOS Sans SC' for e in self.elements if e['role']!='H1')
        for element in self.elements:
            c=region_contrast(self.background,element['bbox'],rgb(self.ink));element['contrast_lower_bound']=round(c,3)
            if c<4.5:self.errors.append(f"Low contrast: {element['role']}")
        for i,a in enumerate(self.elements):
            for b in self.elements[i+1:]:
                aa,bb=a['bbox'],b['bbox']
                if min(aa[2],bb[2])>max(aa[0],bb[0])+2 and min(aa[3],bb[3])>max(aa[1],bb[1])+2:self.errors.append('Text overlap: '+a['text']+' / '+b['text'])
        if self.errors:raise ValueError('\n'.join(self.errors))
        out.mkdir(parents=True,exist_ok=True);state.mkdir(parents=True,exist_ok=True)
        name=f"{self.brief['project']['id']}_{self.lang}_4x5_review_{revision}.png"
        self.im.save(out/name,dpi=(300,300))
        self.im.resize((600,750),Image.Resampling.LANCZOS).save(out/name.replace('.png','_preview.jpg'),quality=95)
        self.im.resize((375,469),Image.Resampling.LANCZOS).save(state/f'{self.lang}-mobile-375.png')
        write(state/f'layout-{self.lang}.json',self.elements);write(state/f'title-{self.lang}.json',self.title_record);write(state/f'background-{self.lang}.json',self.bg_record)
        return {'path':name,'language':self.lang,'format':'png','width_px':2400,'height_px':3000,'status':'review','errors':[],
                'template_id':SPEC['template_id'],'minimum_text_contrast':min(e['contrast_lower_bound'] for e in self.elements)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--brief',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--state-dir',type=Path,required=True);p.add_argument('--revision',default='v06');a=p.parse_args()
    brief=json.loads(a.brief.read_text());decisions={};files=[]
    for lang in ['zh-CN','en']:
        assets=check(brief['font_topic_evidence'],lang);decisions[lang]=assets
        poster=Poster(lang,assets,brief);poster.draw(brief['poster_copy'][lang]);files.append(poster.save(a.output_dir,a.state_dir,a.revision))
    write(a.state_dir/'font-decision.json',decisions);write(a.state_dir/'delivery-manifest.json',{'files':files,'template_id':SPEC['template_id']})
    print(json.dumps({'files':files,'font_decision':{lang:assets['decision'] for lang,assets in decisions.items()}},ensure_ascii=False,indent=2))
