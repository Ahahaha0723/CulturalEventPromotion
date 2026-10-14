// Compose a generated paper/illustration scene with actual local-font lettering.
// node render_poster.cjs input.json output-dir [skia-canvas-module-path] [--type-only] [--diagnostics]
const fs=require('fs'),path=require('path');
(async()=>{
  const [input,out,...options]=process.argv.slice(2);
  if(!input||!out)throw Error('Expected input.json output-dir [module-path] [--type-only] [--diagnostics]');
  const typeOnly=options.includes('--type-only'),diagnostics=options.includes('--diagnostics');
  const modulePath=options.find(v=>!v.startsWith('--'));
  const {Canvas,FontLibrary,loadImage}=require(modulePath||'skia-canvas');
  const root=path.resolve(__dirname,'..');
  const spec=JSON.parse(fs.readFileSync(path.join(root,'references/layout-spec.json'),'utf8'));
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'references/font-assets.json'),'utf8'));
  const data=JSON.parse(fs.readFileSync(input,'utf8'));
  if(typeOnly && data.status!=='review')throw Error('Typography-only output must be marked review');
  if(!typeOnly && !data.sceneImage)throw Error('Generate the content-related paper/illustration scene before completing a poster');
  const registered={};
  for(const f of manifest.fonts){registered[f.style]=FontLibrary.use('Market_'+f.style,path.join(root,'fonts',f.file));if(!registered[f.style].length)throw Error('Font registration failed: '+f.file)}
  const canvas=new Canvas(spec.canvas.width,spec.canvas.height),ctx=canvas.getContext('2d');
  const textCanvas=new Canvas(spec.canvas.width,spec.canvas.height),textCtx=textCanvas.getContext('2d');
  ctx.fillStyle=data.paperColor||'#F5F1E8';ctx.fillRect(0,0,canvas.width,canvas.height);
  let scenePlacement=null;
  if(!typeOnly){
    const img=await loadImage(path.resolve(path.dirname(input),data.sceneImage));
    // Proportional fit, never distort the generated scene. Inspect crops in final QA.
    const scale=data.sceneFit==='contain'?Math.min(canvas.width/img.width,canvas.height/img.height):Math.max(canvas.width/img.width,canvas.height/img.height);
    const w=img.width*scale,h=img.height*scale,x=(canvas.width-w)/2,y=(canvas.height-h)/2;
    ctx.drawImage(img,x,y,w,h);scenePlacement={sourceWidth:img.width,sourceHeight:img.height,x,y,width:w,height:h,fit:data.sceneFit||'cover'};
  }
  const headers=spec.headerAlignment.sizeOrder.map(id=>data.blocks.find(b=>b.id===id));
  if(headers.some(b=>!b))throw Error('Main title, subtitle and slogan are required');
  if(!(headers[0].size>headers[1].size&&headers[1].size>headers[2].size))throw Error('Main title, subtitle and slogan must use descending font sizes');
  const columns=spec.detailColumns.columns;
  if(columns[0].anchor!==canvas.width-columns[2].anchor || columns[1].anchor!==canvas.width/2)throw Error('Detail columns require equal outer margins and a centered venue');
  const metrics=[];
  for(const block of data.blocks){
    const header=['title','subtitle','slogan'].includes(block.id);
    if(header && (block.align!=='center'||block.x!==spec.headerAlignment.actualCenter))throw Error('Title, subtitle and slogan must share the visible center axis');
    if(block.id==='title'&&block.font!=='Ximai')throw Error('Main title must use the actual 字制区喜脉喜欢体 font file');
    if(!header&&block.size!==spec.detailColumns.sharedFontSize)throw Error('Three-column detail text must share one size; use font weight for hierarchy');
    const column=!header&&block.id!=='test-notice'?columns.find(c=>c.id===block.column):null;
    if(!header&&block.id!=='test-notice'&&!column)throw Error('Specify time, venue or organizer column: '+block.id);
    if(column&&(block.align!==column.align||block.x!==column.anchor||block.width>column.right-column.left))throw Error('Incorrect detail column alignment or anchor: '+block.id);
    if(!spec.fontRoles[block.font] || !block.lines?.length)throw Error('Valid font and non-empty lines required: '+block.id);
    const leading=block.lineHeight||block.size*(block.id==='title'?spec.leading.title:spec.leading.body);
    ctx.font=`${spec.fontRoles[block.font]} ${block.size}px Market_${block.font}`;
    textCtx.font=ctx.font;
    let previousBottom=null;
    for(let i=0;i<block.lines.length;i++){
      const value=block.lines[i];
      if(/[\u3400-\u9fff]/.test(value))throw Error('Untranslated Chinese typeset copy: '+block.id);
      const m=ctx.measureText(value),inkWidth=m.actualBoundingBoxLeft+m.actualBoundingBoxRight;
      if(inkWidth>block.width)throw Error('Text exceeds width: '+block.id+'. Reflow whole phrases; retain locked copy.');
      const x=block.align==='right'?block.x-m.actualBoundingBoxRight:block.align==='center'?block.x+(m.actualBoundingBoxLeft-m.actualBoundingBoxRight)/2:block.x+m.actualBoundingBoxLeft;
      let baseline=block.top+i*leading+m.actualBoundingBoxAscent;
      if(block.baselineWith){const peer=metrics.find(v=>v.id===block.baselineWith);if(!peer||block.lines.length!==1)throw Error('Single-row baseline peer must already be measured');baseline=peer.baseline;}
      const box={id:block.id,value,font:block.font,size:block.size,baseline,left:x-m.actualBoundingBoxLeft,right:x+m.actualBoundingBoxRight,top:baseline-m.actualBoundingBoxAscent,bottom:baseline+m.actualBoundingBoxDescent,color:block.color||data.textColor||'#2D2D2D'};
      if(column&&(box.left<column.left-0.01||box.right>column.right+0.01))throw Error('Text outside its detail column: '+block.id);
      if(previousBottom!==null && box.top-previousBottom<12)throw Error('Insufficient ink-to-ink line gap: '+block.id);
      previousBottom=box.bottom;
      if(box.left<0||box.right>canvas.width||box.top<0||box.bottom>canvas.height)throw Error('Outside canvas: '+block.id);
      textCtx.fillStyle=box.color;textCtx.fillText(value,x,baseline);metrics.push(box);
    }
  }
  for(let i=0;i<metrics.length;i++)for(let j=i+1;j<metrics.length;j++){
    const a=metrics[i],b=metrics[j];if(Math.min(a.right,b.right)>Math.max(a.left,b.left)&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top))throw Error('Text overlap: '+a.id+' / '+b.id);
  }
  const inkReport={enabled:data.inkTexture!==false&&spec.printTexture.typographyInkTexture,method:'light density variation inside actual glyph alpha',affectedPixels:0,microDropouts:0};
  if(inkReport.enabled){
    const layer=textCtx.getImageData(0,0,canvas.width,canvas.height),pixels=layer.data;
    const titleBounds=metrics.filter(m=>m.id==='title');
    for(let y=0;y<canvas.height;y++)for(let x=0;x<canvas.width;x++){
      const i=(y*canvas.width+x)*4,a=pixels[i+3];if(!a)continue;
      const title=titleBounds.some(b=>x>=b.left&&x<=b.right&&y>=b.top&&y<=b.bottom);
      let hash=((x>>1)*73856093)^((y>>1)*19349663)^0x52fe13;
      hash=Math.imul(hash^(hash>>>13),1274126177);const noise=(hash>>>0)/4294967296;
      const variation=title?spec.printTexture.inkDensityVariation.title:spec.printTexture.inkDensityVariation.body;
      const probability=title?spec.printTexture.microDropoutProbability.title:spec.printTexture.microDropoutProbability.body;
      let density=1-variation+variation*noise;
      // Micro ink loss only inside thick ink regions; preserve thin stems and contours.
      const interior=a>220&&x>0&&y>0&&x<canvas.width-1&&y<canvas.height-1&&pixels[i-4+3]>200&&pixels[i+4+3]>200&&pixels[i-canvas.width*4+3]>200&&pixels[i+canvas.width*4+3]>200;
      if(interior&&noise<probability){density*=.80;inkReport.microDropouts++;}
      pixels[i+3]=Math.round(a*density);inkReport.affectedPixels++;
    }
    textCtx.putImageData(layer,0,0);
  }
  ctx.drawImage(textCanvas,0,0);
  fs.mkdirSync(out,{recursive:true});
  await canvas.toFile(path.join(out,typeOnly?'typography-review.png':'poster.png'));
  if(diagnostics)fs.writeFileSync(path.join(out,'layout-metrics.json'),JSON.stringify({kind:typeOnly?'typography-review-not-final-poster':'scene-and-typography-composition',status:data.status,registered,scenePlacement,metrics,inkReport},null,2));
  console.log(typeOnly?'Rendered typography review only':'Composed scene and real-font text into PNG');
})().catch(e=>{console.error(e.message);process.exit(1)});
