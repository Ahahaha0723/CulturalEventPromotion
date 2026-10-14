"""Return emblem color candidates, not verified official brand colors.
python sample_emblem_color.py emblem.png palette.json
"""
from pathlib import Path
from PIL import Image
from collections import Counter, defaultdict
import colorsys, json, sys

def sample(source):
    im=Image.open(source).convert('RGBA');im.thumbnail((500,500))
    buckets=Counter();sums=defaultdict(lambda:[0,0,0])
    for r,g,b,a in im.getdata():
        if a<200: continue
        h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        if s<.18 or v<.12 or min(r,g,b)>235:continue
        key=int(h*36)%36;buckets[key]+=1
        for i,c in enumerate((r,g,b)):sums[key][i]+=c
    total=sum(buckets.values());candidates=[]
    for key,count in buckets.most_common(3):
        rgb=[round(c/count) for c in sums[key]]
        candidates.append({'hex':'#'+''.join(f'{c:02X}' for c in rgb),'share_of_filtered_color_pixels':round(count/total,4),'hue_bin':key})
    return {'source':str(Path(source).resolve()),'status':'emblem-sampling-reference-not-official-standard','candidates':candidates,'selected':None,'needs_visual_confirmation':True}
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    result=sample(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Saved',len(result['candidates']),'reference color candidates')
