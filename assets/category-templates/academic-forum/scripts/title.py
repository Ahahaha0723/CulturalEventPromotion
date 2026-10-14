"""Display-only year removal and real-glyph title spacing; no bitmap scaling."""
import re

YEAR=re.compile(r'(?<!第)(?<!\d)(?:1\d{3}|2\d{3})(?!\d|届|人|元)')

def strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,dict):
        for item in value.values():yield from strings(item)
    elif isinstance(value,list):
        for item in value:yield from strings(item)

def display_title(copy):
    source=copy.get('title_source_lines',copy['title_lines'])
    excluded={'title_lines','title_source_lines','title_spacing_reference'}
    other=' '.join(strings({k:v for k,v in copy.items() if k not in excluded}))
    has_year=bool(YEAR.search(other))
    lines=[];removed=[]
    for line in source:
        if has_year:
            removed+=YEAR.findall(line)
            line=re.sub(YEAR.pattern+r'(?:\s*年)?','',line)
        line=re.sub(r'\s+',' ',line).strip(' /—–-')
        if line:lines.append(line)
    if not lines:raise ValueError('Removing years left no academic title text')
    return lines,{'source_lines':source,'display_lines':lines,'non_title_has_year':has_year,'removed_years':removed}

def packed_line(font,text,factor=0.5):
    positions=[];gaps=[];x=0.0
    boxes=[]
    for char in text:
        mask,offset=font.getmask2(char,mode='L',anchor='ls')
        ink=mask.getbbox()
        boxes.append(tuple(ink[i]+offset[i%2] for i in range(4)) if ink else (0,0,0,0))
    for i,char in enumerate(text):
        positions.append((char,x))
        if i==len(text)-1:break
        following=text[i+1]
        advance=font.getlength(char+following)-font.getlength(following)
        if char.isspace():
            actual=advance*factor
            gaps.append({'type':'word_space','original':advance,'actual':actual})
        elif following.isspace():actual=advance
        else:
            original=max(0.0,advance+boxes[i+1][0]-boxes[i][2])
            actual=advance-original*(1-factor)
            if original:gaps.append({'type':'positive_glyph_gap','original':original,'actual':original*factor})
        x+=actual
    visible=[(px+b[0],b[1],px+b[2],b[3]) for (_,px),b in zip(positions,boxes) if b[3]>b[1]]
    bounds=(min(b[0] for b in visible),min(b[1] for b in visible),max(b[2] for b in visible),max(b[3] for b in visible))
    return positions,bounds,gaps
