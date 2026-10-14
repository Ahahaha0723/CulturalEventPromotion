// Typography demonstration, not a completed key visual.
// node render_layout.cjs copy.json output-dir [skia-canvas-module-path]
const fs = require('fs');
const path = require('path');
(async () => {
  const [input, output, modulePath] = process.argv.slice(2);
  if (!input || !output) throw Error('Expected copy.json output-dir [skia-canvas-module-path]');
  const {Canvas, FontLibrary} = require(modulePath || 'skia-canvas');
  const root = path.resolve(__dirname, '..');
  const spec = JSON.parse(fs.readFileSync(path.join(root, 'references/layout-spec.json'), 'utf8'));
  const data = JSON.parse(fs.readFileSync(input, 'utf8'));
  const mode = spec.modes[data.layout_mode];
  if (!mode) throw Error('Choose central or bottom-band');
  if (!data.copy.title_lines?.length) throw Error('Provide upstream-approved title_lines or map the title before rendering');
  const standardSlots = new Set(['year','title_lines','subtitle','slogan','location','date_lines','venue_lines','organizers','sponsor_lines','extra_text_blocks','slogan_lines','organizer_lines']);
  const unmapped = Object.keys(data.copy).filter(key => !standardSlots.has(key));
  if (unmapped.length) throw Error('Unmapped layout data: '+unmapped.join(', ')+'. Put approved text in extra_text_blocks; this is a mapping issue, not an information-scope rejection.');
  const registered = {};
  for (const [name,[file]] of Object.entries(spec.fonts)) {
    registered[name] = FontLibrary.use('Sports_'+name, path.join(root,spec.fontDirectory,file));
    if (!registered[name].length) throw Error('Font registration failed: '+file);
  }
  const canvas = new Canvas(spec.canvas.width,spec.canvas.height);
  const ctx = canvas.getContext('2d');
  // Typography stays transparent; the gradient and hero are separate scene assets.
  const metrics=[],adjustments=[];
  function measure(value,size,font) {ctx.font=`${spec.fonts[font][1]} ${size}px Sports_${font}`;return ctx.measureText(value);}
  function wrapEnglish(values,item) {
    const output=[];
    for(const value of values) {
      let current='';
      for(const word of value.trim().split(/\s+/)) {
        if(measure(word,item.size,item.font).width>item.width) throw Error('English word exceeds available width: '+word+'. Supply an approved shorter term; do not split letters.');
        const candidate=current?current+' '+word:word;
        if(current && measure(candidate,item.size,item.font).width>item.width) { output.push(current);current=word; }
        else current=candidate;
      }
      if(current) output.push(current);
    }
    return output;
  }
  function rows(id,values,item) {
    if (!values.length) return null;
    if(item.lockSize) values=wrapEnglish(values,item);
    if (item.maxLines && values.length>item.maxLines) throw Error('Too many title lines; revise the selected mechanism');
    let size=item.size;
    if(item.lockSize && values.some(value=>measure(value,item.size,item.font).width>item.width)) throw Error('Fixed-size block overflow: '+id+'. Reflow semantic lines; keep the address/header size equal.');
    for(const value of values) {
      if(typeof value!=='string' || !value.trim()) throw Error('Empty visible copy: '+id);
      const m=measure(value,item.size,item.font);size=Math.min(size,item.size*item.width/Math.max(1,m.width));
    }
    if(size<item.size*(id==='title'?spec.minimumTitleScale:0.75)) throw Error('Text too long: '+id+'. Reflow semantic lines instead of excessive shrinking.');
    if(size<item.size) adjustments.push({id,nominalSize:item.size,actualSize:size});
    const role=item.textRole || (Object.prototype.hasOwnProperty.call(spec.textColors,id)?id:'other');
    const color=spec.textColors[role];
    if(!color) throw Error('Unknown text color role: '+role);
    const result=[];
    const lastMetrics = measure(values.at(-1),size,item.font);
    values.forEach((value,i)=>{
      const m=measure(value,size,item.font);
      const x=item.align==='right'?item.x-m.actualBoundingBoxRight:item.align==='center'?item.x-(m.actualBoundingBoxRight-m.actualBoundingBoxLeft)/2:item.x+m.actualBoundingBoxLeft;
      const baseline=item.bottom !== undefined ? item.bottom-lastMetrics.actualBoundingBoxDescent-(values.length-1-i)*(item.lineHeight||size*1.3) : item.top+i*(item.lineHeight||size*1.3)+m.actualBoundingBoxAscent;
      const top=baseline-m.actualBoundingBoxAscent;
      const box={id:id+'_'+(i+1),value,size,font:item.font,color,textRole:role,left:x-m.actualBoundingBoxLeft,right:x+m.actualBoundingBoxRight,top,bottom:baseline+m.actualBoundingBoxDescent};
      ctx.fillStyle=color;ctx.fillText(value,x,baseline);
      metrics.push(box);result.push(box);
    });
    return {id,top:result[0].top,bottom:Math.max(...result.map(v=>v.bottom)),left:Math.min(...result.map(v=>v.left)),right:Math.max(...result.map(v=>v.right))};
  }
  const c=data.copy;const one=v=>v?[v]:[];
  const sloganText=c.slogan_lines?.length ? c.slogan_lines.reduce((all,line)=>all+(/[a-z0-9]$/i.test(all)&&/^[a-z0-9]/i.test(line)?' ':'')+line,'') : c.slogan;
  const sloganLines=sloganText ? [sloganText] : [];
  const organizerLines=c.organizer_lines || (c.organizers ? c.organizers.split(/\s*[|｜]\s*/) : []);
  rows('slogan',sloganLines,mode.slogan);
  const organizers=rows('organizers',organizerLines,mode.organizers);
  const sponsors=rows('sponsors',c.sponsor_lines||[],mode.sponsors);
  if(Math.max(organizers?.bottom||0,sponsors?.bottom||0)+60>mode.slogan.top) throw Error('Header groups approach the single-line slogan. Move the slogan, hero and title group together without changing the equal edge margins.');
  rows('year',one(c.year),mode.year);
  const title=rows('title',c.title_lines,mode.title);
  rows('subtitle',one(c.subtitle),{...mode.subtitle,top:Math.max(mode.subtitle.top,title.bottom+65)});
  rows('date',c.date_lines||[],mode.date);
  const venues=[...(c.venue_lines||[])];
  // Consolidate city into the address once; no separate city label is drawn.
  if(c.location && !venues.some(value=>value.includes(c.location))) {
    if(venues.length) venues[venues.length-1]=venues[venues.length-1]+', '+c.location;
    else venues.push(c.location);
  }
  rows('venue',venues,mode.venue);
  for (const block of c.extra_text_blocks || []) {
    if (!block.id || !Array.isArray(block.lines) || !block.style) throw Error('Each extra text block needs id, lines and a measured style');
    rows(block.id,block.lines,block.style);
  }
  for(const row of metrics) if(/[\u3400-\u9fff]/.test(row.value)) throw Error('English poster contains visible Chinese copy: '+row.id);
  for(const r of metrics) if(r.left<0||r.right>spec.canvas.width||r.top<0||r.bottom>spec.canvas.height) throw Error('Outside canvas: '+r.id);
  for(let i=0;i<metrics.length;i++)for(let j=i+1;j<metrics.length;j++) {
    const a=metrics[i],b=metrics[j];
    if(Math.min(a.right,b.right)>Math.max(a.left,b.left) && Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)) throw Error('Text collision: '+a.id+' / '+b.id);
  }
  fs.mkdirSync(output,{recursive:true});
  fs.writeFileSync(path.join(output,'layout-outlined.svg'),await canvas.toBuffer('svg',{outline:true}));
  fs.writeFileSync(path.join(output,'layout-preview.png'),await canvas.toBuffer('png'));
  fs.writeFileSync(path.join(output,'layout-metrics.json'),JSON.stringify({kind:'typography-demo-not-final-poster',mode:data.layout_mode,registered,metrics,adjustments},null,2));
  console.log('Typography layout demonstration generated: '+data.layout_mode);
})().catch(e=>{console.error(e.message);process.exit(1);});
