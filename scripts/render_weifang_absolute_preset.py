from pathlib import Path
import json,hashlib,argparse
from PIL import Image,ImageDraw,ImageFont,ImageFilter

SKILL_ROOT=Path(__file__).resolve().parents[1]

def prepare_job(c,l,job,job_base,output):
    import copy,math
    c=copy.deepcopy(c);l=copy.deepcopy(l)
    if job.get('preset_id')!='weifang-kite-digital-v1':raise ValueError('Wrong preset ID')
    review=job.get('content_master',{})
    if review.get('status')!='confirmed' or not review.get('user_confirmation_source'):raise ValueError('Current content master is not confirmed')
    selection=job.get('selection',{});ids=selection.get('selected_ids',[]);sprites=selection.get('sprites',[])
    if selection.get('status')!='confirmed' or not selection.get('user_confirmation_source'):raise ValueError('Eight-asset selection is not confirmed')
    if len(ids)!=8 or len(set(ids))!=8:raise ValueError('Choose exactly eight distinct source IDs')
    if len(sprites)!=8 or [s.get('id') for s in sprites]!=ids:raise ValueError('Sprite mapping must match eight selected IDs in order')
    paths=[]
    for item in sprites:
        if not item.get('original_source'):raise ValueError('Missing original source evidence')
        p=Path(item['path']);p=p if p.is_absolute() else job_base/p;p=p.resolve()
        if not p.is_file():raise ValueError('Missing sprite: '+str(p))
        paths.append(p)
    if len(set(paths))!=8:raise ValueError('Eight IDs cannot reuse the same sprite file')
    for p in paths:
        im=Image.open(p).convert('RGBA')
        if im.getchannel('A').getextrema()[0]==255:raise ValueError('Prepare a transparent foreground sprite before rendering')
    for n,(slot,item,p) in enumerate(zip(c['foreground'],sprites,paths)):
        key='selected-'+str(n);c['assets'][key]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        slot['id']=item['id'];slot['asset_key']=key;slot['bbox']=None
    logo=job.get('logo',{})
    if not logo.get('path') or not logo.get('source'):raise ValueError('Current real logo and source are required')
    p=Path(logo['path']);p=p if p.is_absolute() else job_base/p
    if not p.is_file():raise ValueError('Missing current logo')
    c['assets']['logo']={'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    def normalized(value):
        s=str(value).strip().upper();s=s[1:] if s.startswith('K') else s
        return str(int(s)) if s.isdigit() else s
    if len({normalized(v) for v in ids})!=8:raise ValueError('Alias IDs cannot repeat the same foreground source')
    bg=job.get('background',{});sid=bg.get('source_id') or '02';mode=bg.get('choice_mode','default_02')
    if mode=='default_02':
        if normalized(sid)!='2':raise ValueError('Default background must be current asset 02')
    elif mode=='user_selected':
        if not bg.get('user_selection_source'):raise ValueError('Background override needs the actual user selection source')
    else:raise ValueError('Unknown background choice mode')
    matching=[n for n,v in enumerate(ids) if normalized(v)==normalized(sid)]
    if bg.get('path'):
        if not bg.get('original_source'):raise ValueError('Background original source is required')
        p=Path(bg['path']);p=p if p.is_absolute() else job_base/p
    elif matching:p=paths[matching[0]]
    else:raise ValueError('Provide the current default 02 or user-selected background source')
    if not p.is_file():raise ValueError('Missing current background source')
    job['_resolved_background']={'source_id':sid,'choice_mode':mode,'source_path':str(p.resolve()),'user_selection_source':bg.get('user_selection_source') or 'D28 fixed default 02','distinct_subject_source_ids':list(dict.fromkeys([normalized(v) for v in ids]+[normalized(sid)]))}
    copy_map=job.get('copy',{}).get(l['language'],{})
    if set(copy_map)!=set(t['id'] for t in l['texts']):raise ValueError('Supply all fixed text IDs for the current language')
    if any(not isinstance(copy_map[t['id']],str) or (t['field'] is not None and not copy_map[t['id']].strip()) for t in l['texts']):raise ValueError('Missing current confirmed copy')
    a=Image.open(p).convert('RGBA');bb=a.getchannel('A').getbbox()
    if not bb:raise ValueError('Background source is fully transparent')
    a=a.crop(bb);a=a.crop((0,0,a.width,math.ceil(a.height/3)))
    target=tuple(c['background']['resize_px']);a.thumbnail(target,Image.Resampling.LANCZOS)
    # Allow enlargement while preserving proportions inside the prescribed frame.
    scale=min(target[0]/a.width,target[1]/a.height)
    a=a.resize((round(a.width*scale),round(a.height*scale)),Image.Resampling.LANCZOS)
    frame=Image.new('RGBA',target,(0,0,0,0));frame.paste(a,((target[0]-a.width)//2,target[1]-a.height))
    output.mkdir(parents=True,exist_ok=True);derived=output/f'job-background-upper-third-{l["language"]}.png'
    if derived.exists():raise RuntimeError('Refusing to overwrite derived background')
    frame.save(derived);c['assets']['background_K02_upper_third']={'path':str(derived.resolve()),'source_id':sid}
    copy_map=job.get('copy',{}).get(l['language'],{})
    if set(copy_map)!=set(t['id'] for t in l['texts']):raise ValueError('Supply all fixed text IDs for the current language')
    measure=ImageDraw.Draw(Image.new('RGB',tuple(c['canvas_px'])))
    ticket_bottom=None
    for t in l['texts']:
        value=copy_map[t['id']]
        if not isinstance(value,str) or (t['field'] is not None and not value.strip()):raise ValueError('Missing current copy: '+t['id'])
        t['text']=value
        f=ImageFont.truetype(str(SKILL_ROOT/t['font_path']),t['size_px'])
        if t['actual_variation_axes']:f.set_variation_by_axes(t['actual_variation_axes'])
        rb=measure.textbbox((0,0),value,font=f,anchor=t['anchor']);x,y=t['draw_xy']
        if t['alignment']=='center':x=round(t['alignment_reference_x']-(rb[0]+rb[2])/2)
        elif t['alignment']=='right':x=round(t['alignment_reference_x']-(rb[2]-rb[0]))
        if l['language']=='en' and t['id']=='en-T16':y=ticket_bottom-(rb[3]-rb[1])
        t['draw_xy']=[x,y];t['bbox']=list(measure.textbbox((x,y),value,font=f,anchor=t['anchor']))
        if t['field']=='C07':ticket_bottom=t['bbox'][3]
        if not (0<=t['bbox'][0]<=t['bbox'][2]<=c['canvas_px'][0] and 0<=t['bbox'][1]<=t['bbox'][3]<=c['canvas_px'][1]):raise ValueError('Copy overflows fixed canvas: '+t['id'])
    return c,l

def render(skill_root,output,lang,verify=True,job_path=None):
    preset=skill_root/'assets/layout-presets/weifang-kite-digital-v1'
    c=json.loads((preset/'canvas.json').read_text(encoding='utf-8'))
    l=json.loads((preset/f'{lang}.json').read_text(encoding='utf-8'))
    job_mode=job_path is not None
    job=None
    if job_mode:
        job_path=Path(job_path).resolve();job=json.loads(job_path.read_text(encoding='utf-8'))
        c,l=prepare_job(c,l,job,job_path.parent,output);verify=False
    output.mkdir(parents=True,exist_ok=True)
    dest=output/f'weifang-kite_{lang}.png'
    report=output/f'weifang-kite_{lang}_verification.json'
    if dest.exists() or report.exists():raise RuntimeError('Refusing to overwrite a previous output')
    size=tuple(c['canvas_px'])
    def asset(key):return skill_root/c['assets'][key]['path']
    im=Image.open(asset('paper')).convert('RGB').resize(size,Image.Resampling.LANCZOS)
    for block in [c['background']]:
        a=Image.open(asset(block['asset'])).convert('RGBA').resize(tuple(block['resize_px']),Image.Resampling.LANCZOS)
        a.putalpha(a.getchannel('A').point(lambda q:round(q*block['opacity_multiplier'])))
        im.paste(a,tuple(block['bbox'][:2]),a)
    q=c['quiet_overlay'];mask=Image.new('L',size,0);ImageDraw.Draw(mask).rectangle(tuple(q['rectangle']),fill=q['mask_alpha'])
    mask=mask.filter(ImageFilter.GaussianBlur(q['blur_radius']))
    im.paste(Image.new('RGB',size,q['fill']),(0,0),mask)
    block=c['header_decoration'];a=Image.open(asset(block['asset'])).convert('RGBA')
    a.putalpha(a.getchannel('A').point(lambda v:round(v*block['opacity_multiplier'])))
    im.paste(a,tuple(block['bbox'][:2]),a)
    placements=[]
    for item in c['foreground']:
        a=Image.open(asset(item['asset_key'])).convert('RGBA');slot=item['slot']
        a.thumbnail((slot[2]-slot[0],slot[3]-slot[1]),Image.Resampling.LANCZOS)
        x=round((slot[0]+slot[2]-a.width)/2);y=round((slot[1]+slot[3]-a.height)/2)
        actual=[x,y,x+a.width,y+a.height]
        if item['bbox'] is not None and actual!=item['bbox']:raise RuntimeError('Subject bounding box mismatch: '+item['id'])
        im.paste(a,(x,y),a);placements.append({'id':item['id'],'bbox':actual})
    d=ImageDraw.Draw(im)
    for line in c['process_tracks']:d.rectangle(tuple(line['rectangle']),fill=line['fill'])
    logo=Image.open(asset('logo')).resize(tuple(c['logo']['resize_px']),Image.Resampling.LANCZOS)
    im.paste(logo,tuple(c['logo']['bbox'][:2]),logo)
    bboxes=[]
    for index,t in enumerate(l['texts']):
        if index==1:d.rectangle(tuple(c['header_bar']['rectangle']),fill=c['header_bar']['fill'])
        f=ImageFont.truetype(str(skill_root/t['font_path']),t['size_px'])
        if t['actual_variation_axes']:f.set_variation_by_axes(t['actual_variation_axes'])
        xy=tuple(t['draw_xy']);bb=list(d.textbbox(xy,t['text'],font=f,anchor=t['anchor']))
        if verify and bb!=t['bbox']:raise RuntimeError('Glyph bbox mismatch: '+t['id'])
        d.text(xy,t['text'],font=f,fill=t['color'],anchor=t['anchor'])
        bboxes.append({'id':t['id'],'bbox':bb})
    pixel_sha=hashlib.sha256(im.tobytes()).hexdigest()
    match=pixel_sha==l['expected_original_pixel_sha256']
    if verify and not match:raise RuntimeError('Pixel mismatch against the accepted same-case poster')
    im.save(dest,dpi=tuple(c['png_dpi']))
    result={'language':lang,'canvas':list(size),'source':'current confirmed task' if job_mode else 'T2_v11 accepted D24 / S01 R13','preset_skill':'S04','pixel_sha256':pixel_sha,'pixel_identical_to_original':match,'png_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'png_file_identical_to_original':hashlib.sha256(dest.read_bytes()).hexdigest()==l['expected_original_png_sha256'],'text_bboxes':bboxes,'subject_bboxes':placements,'classification':'current confirmed eight-asset fixed-layout job' if job_mode else 'same-case deterministic verification export, not a new poster design candidate','selected_ids':job['selection']['selected_ids'] if job_mode else [x['id'] for x in c['foreground']],'current_job_mode':job_mode,'background_choice':job.get('_resolved_background') if job_mode else {'source_id':'02','choice_mode':'D24 reference case'},'current_user_selection_source':job['selection']['user_confirmation_source'] if job_mode else 'D24 reference case','current_content_master_review':job['content_master'] if job_mode else None,'reference_pixel_hash_is_acceptance_criterion':not job_mode}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Render the locked bilingual kite-poster preset; never overwrite outputs.')
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--language',choices=['zh-CN','en','both'],default='both')
    parser.add_argument('--job',type=Path,help='Confirmed current master, eight selected sprites, current logo and bilingual copy')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    results=[render(root,args.output,lang,job_path=args.job) for lang in (['zh-CN','en'] if args.language=='both' else [args.language])]
    print(json.dumps([{'language':r['language'],'pixel_identical_to_original':r['pixel_identical_to_original'],'png_file_identical_to_original':r['png_file_identical_to_original']} for r in results],ensure_ascii=False,indent=2))
