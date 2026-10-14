// Rasterize the coverage mask only; the artwork and Harmony glyphs remain vector.
// node build_overlap_mask.cjs artwork.svg typography.svg mask.png report.json [sharp-module-path]
const fs = require('fs');
(async () => {
  const [art, type, mask, report, modulePath] = process.argv.slice(2);
  if (!report) throw Error('Expected artwork.svg typography.svg mask.png report.json [sharp-module-path]');
  const sharp = require(modulePath || 'sharp');
  const a = await sharp(art).flatten({background:'#FFFFFF'}).removeAlpha().raw().toBuffer({resolveWithObject:true});
  const t = await sharp(type).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  if (a.info.width !== t.info.width || a.info.height !== t.info.height) throw Error('Artwork and typography dimensions differ');
  const linear = Array.from({length:256}, (_,v) => { const c=v/255; return c<=0.04045 ? c/12.92 : ((c+0.055)/1.055)**2.4; });
  const rgba = Buffer.alloc(a.info.width*a.info.height*4);
  let darkText=0, lightText=0, minContrast=Infinity;
  for (let i=0;i<a.info.width*a.info.height;i++) {
    const r=a.data[i*3],g=a.data[i*3+1],b=a.data[i*3+2];
    const contrast=1.05/(0.2126*linear[r]+0.7152*linear[g]+0.0722*linear[b]+0.05);
    const dark=contrast>=4.5;
    rgba[i*4]=rgba[i*4+1]=rgba[i*4+2]=255;
    rgba[i*4+3]=dark?255:0;
    if(t.data[i*4+3]>220 && Math.min(r,g,b)<235) {
      if(dark) { darkText++; minContrast=Math.min(minContrast,contrast); }
      else lightText++;
    }
  }
  const lightFraction=lightText/Math.max(1,darkText+lightText);
  const result={policy:'actual-glyph-intersection-white',white:'#FFFFFF',minimumWhiteContrast:4.5,
    measuredMinimumWhiteContrast:Number.isFinite(minContrast)?minContrast:null,
    darkGraphicGlyphPixels:darkText,lightGraphicGlyphPixels:lightText,lightFraction,
    antialiasAllowance:0.03,status:lightFraction>0.03?'fail':'pass'};
  fs.writeFileSync(report,JSON.stringify(result,null,2));
  if(result.status==='fail') throw Error('Light artwork crosses text. Darken the crossing shapes (white contrast >=4.5), or move the light portions. See '+report);
  await sharp(rgba,{raw:{width:a.info.width,height:a.info.height,channels:4}}).png().toFile(mask);
  console.log(JSON.stringify(result));
})().catch(e=>{console.error(e.message);process.exit(1);});
