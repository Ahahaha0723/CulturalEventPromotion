// Render explicit measured line blocks; this is a review helper, not copy selection.
const fs=require('fs'),path=require('path');
(async()=>{
  const [input,out,modulePath,diagnosticsFlag]=process.argv.slice(2);
  if(!input||!out)throw Error('Expected input.json output-dir [skia-canvas-module-path]');
  const {Canvas,FontLibrary,loadImage}=require(modulePath||'skia-canvas');
  const root=path.resolve(__dirname,'..');
  const spec=JSON.parse(fs.readFileSync(path.join(root,'references/layout-spec.json'),'utf8'));
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'references/font-assets.json'),'utf8'));
  const data=JSON.parse(fs.readFileSync(input,'utf8'));
  if(data.bodyColor && data.bodyColor.toUpperCase()!=='#4B4B4B')throw Error('Body color must be #4B4B4B');
  if(!data.themeColor && data.status!=='review')throw Error('Confirmed emblem themeColor required for final typography');
  if(data.themeColor && !/^#[0-9a-f]{6}$/i.test(data.themeColor))throw Error('themeColor must be a six-digit hex color');
  const schoolBlock=data.blocks.find(b=>b.id==='school'),anniversaryBlock=data.blocks.find(b=>b.id==='anniversary');
  if(schoolBlock && anniversaryBlock && schoolBlock.size!==anniversaryBlock.size)throw Error('School and anniversary must share one font size');
  if(schoolBlock && schoolBlock.top!==spec.header.emblem.top)throw Error('School ink top must align with emblem ink top');
  const canvas=new Canvas(spec.canvas.width,spec.canvas.height),ctx=canvas.getContext('2d');
  const registered={};for(const f of manifest.fonts){registered[f.style]=FontLibrary.use('Anniversary_'+f.style,path.join(root,'fonts',f.file));if(!registered[f.style].length)throw Error('Font registration failed: '+f.file)}
  ctx.fillStyle=data.background||'#FFFFFF';ctx.fillRect(0,0,canvas.width,canvas.height);
  const metrics=[],separators=[];
  for(const block of data.blocks){
    if(block.lines.some(v=>v.replace(/\s/g,'').includes('校友返校·校园开放日')))throw Error('Removed subtitle must not appear: '+block.id);
    if(/^(participation|streaming)(-|$)/.test(block.id) && (block.align!=='right'||block.x!==spec.header.emblem.right))throw Error('Participation and streaming must align right with emblem: '+block.id);
    if(!['title','body'].includes(block.role))throw Error('Explicit title/body role required: '+block.id);
    const color=block.role==='title'?(data.themeColor||'#2D2D2D'):'#4B4B4B';
    if(block.color && block.color.toUpperCase()!==color.toUpperCase())throw Error('Color conflicts with role policy: '+block.id);
    if(!Object.hasOwn(spec.fontRoles,block.font))throw Error('Unknown font style: '+block.font);
    ctx.font=`${spec.fontRoles[block.font]} ${block.size}px Anniversary_${block.font}`;
    for(let i=0;i<block.lines.length;i++){
      const value=block.lines[i],m=ctx.measureText(value);
      const width=m.actualBoundingBoxLeft+m.actualBoundingBoxRight;
      if(width>block.width)throw Error('Reflow text block instead of silently shrinking: '+block.id);
      const align=block.align||'left';
      const x=align==='right'?block.x-m.actualBoundingBoxRight:align==='center'?block.x+(m.actualBoundingBoxLeft-m.actualBoundingBoxRight)/2:block.x+m.actualBoundingBoxLeft;
      const baseline=block.top+i*(block.lineHeight||block.size*1.5)+m.actualBoundingBoxAscent;
      const box={id:block.id,value,font:block.font,size:block.size,role:block.role,color,left:x-m.actualBoundingBoxLeft,right:x+m.actualBoundingBoxRight,top:baseline-m.actualBoundingBoxAscent,bottom:baseline+m.actualBoundingBoxDescent};
      if(box.left<0||box.right>canvas.width||box.top<0||box.bottom>canvas.height)throw Error('Outside canvas: '+block.id);
      ctx.fillStyle=color;ctx.fillText(value,x,baseline);metrics.push(box);
    }
  }
  if(data.emblem){
    const image=await loadImage(path.resolve(path.dirname(input),data.emblem.file));
    // Measure visible emblem ink, excluding transparent/near-white perimeter.
    const probe=new Canvas(image.width,image.height),pc=probe.getContext('2d');pc.drawImage(image,0,0);
    const pixels=pc.getImageData(0,0,image.width,image.height).data;
    let hasClearBackground=false;
    for(let i=3;i<pixels.length;i+=4)if(pixels[i]<32){hasClearBackground=true;break}
    if(!hasClearBackground)throw Error('Remove emblem background first and supply a transparent PNG');
    let l=image.width,t=image.height,r=-1,b=-1;
    for(let y=0;y<image.height;y++)for(let x=0;x<image.width;x++){
      const i=(y*image.width+x)*4;if(pixels[i+3]>=32 && Math.min(pixels[i],pixels[i+1],pixels[i+2])<245){l=Math.min(l,x);t=Math.min(t,y);r=Math.max(r,x);b=Math.max(b,y)}
    }
    if(r<l)throw Error('Emblem has no measurable visible ink');
    const schoolInk=metrics.filter(v=>v.id==='school'),anniversaryInk=metrics.filter(v=>v.id==='anniversary');
    if(!schoolInk.length||!anniversaryInk.length)throw Error('Measured school and anniversary text required for emblem sizing');
    const topTarget=Math.min(...schoolInk.map(v=>v.top));
    const iw=r-l+1,ih=b-t+1,cfg=spec.header.emblem;
    const ref=cfg.referenceCanvas;
    const h=cfg.visibleHeight*Math.min(canvas.width/ref.width,canvas.height/ref.height);
    const bottomTarget=topTarget+h;
    if(h<=0)throw Error('Invalid header span for proportional emblem');
    const scale=h/ih,w=iw*scale,x=cfg.right-w,y=topTarget;
    if(x<spec.margin || y+h>canvas.height)throw Error('Proportional emblem does not fit header; revise title spacing without distorting the asset');
    // Retain the original asset; offset its padding so its actual ink is aligned.
    ctx.drawImage(image,x-l*scale,y-t*scale,image.width*scale,image.height*scale);
    metrics.push({id:'actual-emblem',left:x,right:x+w,top:y,bottom:y+h,sourceInkBounds:{left:l,top:t,right:r+1,bottom:b+1},alignmentTargets:{schoolTop:topTarget,sharedVisibleHeight:h,participationRight:cfg.right},scale});
  }else if(data.status!=='review')throw Error('Real emblem required for a final version');
  for(let i=0;i<metrics.length;i++)for(let j=i+1;j<metrics.length;j++){
    const a=metrics[i],b=metrics[j];if(Math.min(a.right,b.right)>Math.max(a.left,b.left)&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top))throw Error('Overlap: '+a.id+' / '+b.id);
  }
  if(spec.separatorRules.required){
    const cfg=spec.separatorRules;
    const detailIds=['schedule','more-activities','subvenues','participation','streaming'];
    const detailInk=metrics.filter(m=>detailIds.some(id=>m.id===id||m.id===id+'-title'));
    const footerInk=metrics.filter(m=>['organizer','test-status'].includes(m.id));
    const venueInk=metrics.filter(m=>m.id==='venue');
    if(!detailInk.length||!footerInk.length||!venueInk.length)throw Error('Two group rules require measured venue, details and footer blocks');
    const gaps=[
      [Math.max(...venueInk.map(m=>m.bottom)),Math.min(...detailInk.map(m=>m.top))],
      [Math.max(...detailInk.map(m=>m.bottom)),Math.min(...footerInk.map(m=>m.top))]
    ];
    gaps.forEach(([above,below],i)=>{
      if(below-above<2*cfg.minimumInkClearance+cfg.strokeWidth)throw Error('Insufficient space for required separator '+(i+1)+': reflow details without omitting the line');
      const y=(above+below)/2,color=data.themeColor||'#2D2D2D';
      ctx.save();ctx.globalAlpha=cfg.opacity;ctx.strokeStyle=color;ctx.lineWidth=cfg.strokeWidth;
      ctx.beginPath();ctx.moveTo(cfg.left,y);ctx.lineTo(cfg.right,y);ctx.stroke();ctx.restore();
      separators.push({id:'separator-'+(i+1),left:cfg.left,right:cfg.right,y,strokeWidth:cfg.strokeWidth,opacity:cfg.opacity,color});
    });
  }
  fs.mkdirSync(out,{recursive:true});
  await canvas.toFile(path.join(out,'typography-review.png'));
  if(diagnosticsFlag==='--diagnostics')fs.writeFileSync(path.join(out,'layout-metrics.json'),JSON.stringify({status:data.status,paletteStatus:data.paletteStatus,registered,metrics,separators},null,2));
  console.log('Rendered PNG with actual NotoSerifSC glyphs; checked text boundaries');
})().catch(e=>{console.error(e.message);process.exit(1)});
