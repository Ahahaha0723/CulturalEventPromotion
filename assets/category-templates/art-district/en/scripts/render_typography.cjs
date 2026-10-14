const fs = require('fs');
const path = require('path');

// node render_typography.cjs layout-text.json output-dir [skia-canvas-module-path]
// Explicit module path supports bundled runtimes without hard-coded machine paths.
(async () => {
  const [input, output, modulePath] = process.argv.slice(2);
  if (!input || !output) throw Error('Usage: node render_typography.cjs layout-text.json output-dir [skia-canvas-module-path]');
  const { Canvas, FontLibrary } = require(modulePath || 'skia-canvas');
  const root = path.resolve(__dirname, '..');
  const spec = JSON.parse(fs.readFileSync(path.join(root, 'references/fixed-layout.json'), 'utf8'));
  const copy = JSON.parse(fs.readFileSync(input, 'utf8'));
  const fonts = spec.fontFiles;
  const registered = {};
  for (const [alias, [file]] of Object.entries(fonts)) {
    registered[alias] = FontLibrary.use('Exact_' + alias, path.join(root, 'assets/fonts', file));
    if (!registered[alias].length) throw Error('Font registration failed: ' + file);
  }
  const canvas = new Canvas(spec.canvas.width, spec.canvas.height);
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = spec.colors.text;
  ctx.textBaseline = 'alphabetic';
  const metrics = [], labelBoxes = [], adjustments = [], titlePapers = [];
  function measure(value, size, alias) {
    if (typeof value !== 'string' || !value.trim()) throw Error('Missing or empty text');
    if (/\p{Script=Han}/u.test(value)) throw Error('English-only poster: untranslated Chinese text: ' + value);
    const parts = value.match(/[0-9]+|[^0-9]+/g);
    let width = 0, inkLeft = Infinity, inkRight = -Infinity, ascent = 0, descent = 0;
    const runs = [];
    for (const part of parts) {
      const isDigit = /^[0-9]+$/.test(part);
      const runAlias = isDigit ? spec.digitFontByAlias[alias] : alias;
      if (!runAlias || !fonts[runAlias]) throw Error('Missing font role for mixed text: ' + alias);
      ctx.font = `${fonts[runAlias][1]} ${size}px Exact_${runAlias}`;
      const m = ctx.measureText(part);
      if (part.trim()) {
        inkLeft = Math.min(inkLeft, width - m.actualBoundingBoxLeft);
        inkRight = Math.max(inkRight, width + m.actualBoundingBoxRight);
        ascent = Math.max(ascent, m.actualBoundingBoxAscent);
        descent = Math.max(descent, m.actualBoundingBoxDescent);
      }
      runs.push({ value: part, alias: runAlias, fontFile: fonts[runAlias][0], isDigit, offset: width, width: m.width });
      width += m.width;
    }
    return { width, actualBoundingBoxLeft: -inkLeft, actualBoundingBoxRight: inkRight,
      actualBoundingBoxAscent: ascent, actualBoundingBoxDescent: descent, runs };
  }
  function draw(value, x, y, size, alias, maxWidth, id) {
    const m = measure(value, size, alias);
    if (m.width > maxWidth) throw Error(`Fixed-layout overflow: ${id} (${m.width} > ${maxWidth}px). Preserve copy and font size; revise line breaks or report an explicit layout exception.`);
    for (const run of m.runs) {
      ctx.font = `${fonts[run.alias][1]} ${size}px Exact_${run.alias}`;
      ctx.fillText(run.value, x + run.offset, y);
    }
    metrics.push({ id, value, x, y, size, alias, width: m.width,
      left: x - m.actualBoundingBoxLeft, right: x + m.actualBoundingBoxRight,
      top: y - m.actualBoundingBoxAscent, bottom: y + m.actualBoundingBoxDescent,
      runs: m.runs.map(run => ({ ...run, x: x + run.offset, baseline: y, size })) });
  }
  function fittedSize(value, nominal, alias, maxWidth, id) {
    const width = measure(value, nominal, alias).width;
    if (width <= maxWidth) return nominal;
    const size = Math.floor(nominal * maxWidth / width * 10) / 10;
    const minimum = id.startsWith('footer_') ? spec.footerRules.groupMinimumSize : id.startsWith('booking_') ? spec.footerRules.notesMinimumSize : nominal * spec.englishFit.minScale;
    if (size < minimum) throw Error('English copy exceeds permitted fit range: ' + id);
    adjustments.push({ id, nominalSize: nominal, actualSize: size, reason: 'English text exceeds original width', maxWidth });
    return size;
  }
  function fixed(value, item, id) {
    const titleLimit = item.maxWidth;
    const size = fittedSize(value, item.size, item.font, titleLimit, id);
    const m = measure(value, size, item.font);
    const x = item.align === 'right' ? item.right - m.actualBoundingBoxRight :
      item.inkLeft !== undefined ? item.inkLeft + m.actualBoundingBoxLeft : item.x;
    const y = item.inkTop !== undefined ? item.inkTop + m.actualBoundingBoxAscent : item.baseline;
    draw(value, x, y, size, item.font, titleLimit, id);
    return y;
  }
  for (const key of ['title_lines', 'subtitle_lines', 'slogan_lines']) {
    if (!Array.isArray(copy[key]) || copy[key].length !== ({ title_lines: 2, subtitle_lines: 2, slogan_lines: 4 })[key]) {
      throw Error(key + ' must have the fixed number of semantic lines');
    }
  }
  const labelNames = Array.isArray(copy.activity_labels) ? copy.activity_labels.map(value => Array.isArray(value) ? value.join(' ') : value) : [];
  if (labelNames.length !== 4 || labelNames.some(value => typeof value !== 'string' || !value.trim()) ||
      new Set(labelNames.map(value => value.replace(/\s+/g, ' ').trim().toLowerCase())).size !== 4) {
    throw Error('This layout requires four unique complete English activity labels.');
  }
  const firstBaseline = fixed(copy.subtitle_lines[0], spec.text.subtitle[0], 'subtitle_1');
  fixed(copy.subtitle_lines[1], { ...spec.text.subtitle[1], baseline: firstBaseline + 80 }, 'subtitle_2');
  fixed(copy.date, spec.text.date, 'date');
  fixed(copy.opening_hours, spec.text.opening_hours, 'opening_hours');
  const sloganRuns = copy.slogan_lines.map(value => typeof value === 'string' ? [{ text: value, bold: false }] : value);
  let sloganSize = 100;
  sloganRuns.forEach((runs, i) => {
    if (!Array.isArray(runs) || !runs.length) throw Error('Invalid slogan runs');
    const width = runs.reduce((total, run) => total + measure(run.text, 100, run.bold ? 'HB' : 'HR').width, 0);
    if (width > spec.text.slogan[i].maxWidth) sloganSize = Math.min(sloganSize, Math.floor(100 * spec.text.slogan[i].maxWidth / width * 10) / 10);
  });
  if (sloganSize < 100 * spec.englishFit.minScale) throw Error('English slogan exceeds permitted fit range');
  if (sloganSize !== 100) adjustments.push({ id: 'slogan_all_lines', nominalSize: 100, actualSize: sloganSize, reason: 'Preserve equal sizes while fitting English' });
  sloganRuns.forEach((runs, i) => {
    const item = spec.text.slogan[i]; let cursor = item.x;
    for (const run of runs) {
      draw(run.text, cursor, item.baseline, sloganSize, run.bold ? 'HB' : 'HR', item.maxWidth, 'slogan_' + (i + 1));
      cursor += metrics[metrics.length - 1].width;
    }
  });
  // Both title lines share one measured size; paper sheets follow actual ink dimensions.
  const titleRule = spec.titlePaper;
  let titleSize = titleRule.nominalSize;
  copy.title_lines.forEach((value, i) => {
    const item = spec.text.title[i]; const m = measure(value, titleRule.nominalSize, item.font);
    const inkWidth = m.actualBoundingBoxLeft + m.actualBoundingBoxRight;
    if (inkWidth > item.maxWidth) titleSize = Math.min(titleSize, Math.floor(titleRule.nominalSize * item.maxWidth / inkWidth * 10) / 10);
  });
  if (titleSize < titleRule.minimumSize) throw Error('Both title lines need more width than the common-size title region allows.');
  if (titleSize !== titleRule.nominalSize) adjustments.push({ id: 'title_shared', nominalSize: titleRule.nominalSize, actualSize: titleSize, reason: 'One common Trajan size determined by the longer line' });
  const rotatedCorners = (rect, angle, center) => {
    const radians = angle * Math.PI / 180, cosine = Math.cos(radians), sine = Math.sin(radians);
    return [[rect.x, rect.y], [rect.x + rect.width, rect.y], [rect.x + rect.width, rect.y + rect.height], [rect.x, rect.y + rect.height]].map(([x,y]) => ({ x: center.x + (x-center.x)*cosine - (y-center.y)*sine, y: center.y + (x-center.x)*sine + (y-center.y)*cosine }));
  };
  const polygonIntersects = (a,b) => {
    for (const polygon of [a,b]) for (let k=0;k<polygon.length;k++) {
      const p=polygon[k],q=polygon[(k+1)%polygon.length],axis={x:-(q.y-p.y),y:q.x-p.x};
      const project = points => points.map(point => point.x*axis.x + point.y*axis.y);
      const pa=project(a),pb=project(b);
      if (Math.max(...pa)<=Math.min(...pb) || Math.max(...pb)<=Math.min(...pa)) return false;
    }
    return true;
  };
  ctx.fillStyle = spec.colors.title;
  copy.title_lines.forEach((value, i) => {
    const item = spec.text.title[i], m = measure(value, titleSize, item.font);
    let baseline = item.baseline, actualOverlap = null;
    const makeFront = y => ({ x:item.x-titleRule.paddingX, y:y-m.actualBoundingBoxAscent-titleRule.paddingY,
      width:m.actualBoundingBoxLeft+m.actualBoundingBoxRight+titleRule.paddingX*2,
      height:m.actualBoundingBoxAscent+m.actualBoundingBoxDescent+titleRule.paddingY*2 });
    if (i === 1) {
      const first=titlePapers[0];
      actualOverlap=titleRule.groupOverlap;
      // Overlap the blank sheet margins while protecting the upper title glyphs.
      while (actualOverlap >= titleRule.minimumGroupOverlap) {
        const top=first.front.y+first.front.height-actualOverlap;
        baseline=top+titleRule.paddingY+m.actualBoundingBoxAscent;
        const candidate=makeFront(baseline),center={x:candidate.x+candidate.width/2,y:candidate.y+candidate.height/2};
        const upperText={x:first.textBounds.left-6,y:first.textBounds.top-6,width:first.textBounds.right-first.textBounds.left+12,height:first.textBounds.bottom-first.textBounds.top+12};
        const firstCenter={x:first.front.x+first.front.width/2,y:first.front.y+first.front.height/2};
        if (!polygonIntersects(rotatedCorners(candidate,titleRule.frontAngles[i],center),rotatedCorners(upperText,first.frontAngle,firstCenter))) break;
        actualOverlap-=2;
      }
      if (actualOverlap < titleRule.minimumGroupOverlap) throw Error('Title-paper overlap cannot be kept without entering upper title text.');
      adjustments.push({id:'title_stack',preferredBaseline:item.preferredBaseline,actualBaseline:baseline,overlap:actualOverlap,reason:'Restore overlap between the two title-paper groups'});
    }
    const front=makeFront(baseline),center={x:front.x+front.width/2,y:front.y+front.height/2},angle=titleRule.frontAngles[i];
    ctx.save();ctx.translate(center.x,center.y);ctx.rotate(angle*Math.PI/180);ctx.translate(-center.x,-center.y);
    draw(value,item.x+m.actualBoundingBoxLeft,baseline,titleSize,item.font,item.maxWidth+5,'title_'+(i+1));
    ctx.restore();
    const row=metrics[metrics.length-1],ink={x:row.left,y:row.top,width:row.right-row.left,height:row.bottom-row.top};
    const corners=rotatedCorners(ink,angle,center);
    row.rotation={angle,centerX:center.x,centerY:center.y};
    row.renderedBounds={left:Math.min(...corners.map(p=>p.x)),top:Math.min(...corners.map(p=>p.y)),right:Math.max(...corners.map(p=>p.x)),bottom:Math.max(...corners.map(p=>p.y))};
    const back={x:front.x+titleRule.backOffsetX,y:front.y+titleRule.backOffsetY,width:front.width+titleRule.backExtraWidth,height:front.height+titleRule.backExtraHeight};
    titlePapers.push({id:'title_paper_'+(i+1),front,back,frontAngle:angle,backAngle:titleRule.backAngles[i],overlap:actualOverlap,textBounds:{left:row.left,top:row.top,right:row.right,bottom:row.bottom}});
  });
  ctx.fillStyle = spec.colors.text;
  fixed(copy.organizer, spec.text.organizer, 'organizer');
  for (const side of ['left', 'right']) {
    const values = copy['footer_' + side + '_lines'];
    if (!Array.isArray(values) || values.length !== 3) throw Error('Footer ' + side + ' must have three planned semantic rows; do not omit source facts.');
    values.forEach((value, i) => fixed(value, spec.text['footer_' + side][i], 'footer_' + side + '_' + (i + 1)));
  }
  const notes = copy.booking_notes || [];
  if (!Array.isArray(notes) || notes.length > 2) throw Error('booking_notes must contain at most two complete planned rows.');
  // Notes share a common type size and remain left-aligned.
  ctx.fillStyle = spec.colors.bookingNotes;
  let noteSize = spec.text.booking_notes[0].size;
  notes.forEach((value, i) => { noteSize = Math.min(noteSize, fittedSize(value, spec.text.booking_notes[0].size, 'HR', spec.text.booking_notes[i].maxWidth, 'booking_' + (i + 1))); });
  notes.forEach((value, i) => fixed(value, { ...spec.text.booking_notes[i], size: noteSize }, 'booking_' + (i + 1)));
  ctx.fillStyle = spec.colors.text;
  const rule = spec.labelRules;
  const defaultSceneBounds = spec.scene_slots.filter(scene=>scene.label!==null).sort((a,b)=>a.label-b.label).map(scene=>({left:scene.x,top:scene.y,right:scene.x+scene.width,bottom:scene.y+scene.height}));
  const sceneBounds = copy.scene_bounds || defaultSceneBounds;
  if (!Array.isArray(sceneBounds) || sceneBounds.length!==4 || sceneBounds.some(rect=>!['left','top','right','bottom'].every(key=>Number.isFinite(rect[key])) || rect.right<=rect.left || rect.bottom<=rect.top)) throw Error('scene_bounds must contain four valid final visible-outline rectangles.');
  const fullLabelMetrics = labelNames.map(value => measure(value, rule.size, 'HB'));
  const labelAscent = Math.max(...fullLabelMetrics.map(m => m.actualBoundingBoxAscent));
  const labelDescent = Math.max(...fullLabelMetrics.map(m => m.actualBoundingBoxDescent));
  const intersects = (box, rect) => box.x < rect.right && box.x + box.width > rect.left && box.y < rect.bottom && box.y + box.height > rect.top;
  labelNames.forEach((value, i) => {
    const item = spec.text.activity_labels[i], m = fullLabelMetrics[i];
    // Forget inherited manual line breaks: extend the block before any wrapping.
    let lines = [value];
    if (m.width > rule.maximumTextWidth) {
      lines = []; let line = '';
      for (const word of value.trim().split(/\s+/)) {
        const candidate = line ? line + ' ' + word : word;
        if (line && measure(candidate, rule.size, 'HB').width > rule.maximumTextWidth) { lines.push(line); line = word; }
        else line = candidate;
      }
      if (line) lines.push(line);
      if (lines.length > rule.maximumLinesAfterRelocation || lines.some(line => measure(line, rule.size, 'HB').width > rule.maximumTextWidth)) throw Error('Activity label exceeds extended-label capacity: ' + value);
      adjustments.push({ id: 'activity_' + (i + 1), reason: 'Exceptional two-line label after full extension capacity was exceeded' });
    }
    const measured = lines.map(line => measure(line, rule.size, 'HB'));
    const lineHeight = rule.size * spec.englishFit.labelLineHeightRatio;
    const scene=sceneBounds[i];
    const box = { value, x: item.x, y: scene.bottom+rule.attachmentGap,
      width: Math.max(...measured.map(m => m.width)) + rule.paddingX * 2,
      height: labelAscent + labelDescent + rule.paddingY * 2 + (lines.length - 1) * lineHeight, lines: lines.length };
    box.x = Math.max(rule.safeLeft, Math.min((scene.left+scene.right-box.width)/2, rule.safeRight - box.width));
    if (intersects(box, rule.windowBounds)) {
      const leftCandidate = rule.windowBounds.left - rule.windowGap - box.width;
      if (i === 0 && leftCandidate >= rule.safeLeft) box.x = leftCandidate;
      else box.y = rule.windowBounds.bottom + rule.windowGap;
    }
    for (const obstacle of rule.decorativeObstacles || []) {
      if (intersects(box, obstacle)) box.y = obstacle.bottom + rule.windowGap;
    }
    for (const paper of titlePapers) {
      for (const rect of [paper.front, paper.back]) {
        if (intersects(box, { left: rect.x - 12, top: rect.y - 12, right: rect.x + rect.width + 12, bottom: rect.y + rect.height + 12 })) throw Error('Extended label overlaps a title paper; relocate whole label: ' + value);
      }
    }
    const horizontalGap=Math.max(scene.left-(box.x+box.width),box.x-scene.right,0);
    const verticalGap=Math.max(scene.top-(box.y+box.height),box.y-scene.bottom,0);
    box.sceneBounds={...scene};box.sceneIndex=i;box.sceneGap=Math.hypot(horizontalGap,verticalGap);
    box.sceneBoundsSource=copy.scene_bounds?'measured-visible-outline':'configured-slot-fallback';
    if (box.sceneGap>rule.maximumPreferredGap) adjustments.push({id:'activity_'+(i+1),sceneGap:box.sceneGap,reason:'Nearby window/paper/ornament prevents the preferred20-40px gap; adjust actual artwork/ornament before final delivery'});
    const lastBaseline = box.y + rule.paddingY + labelAscent + (lines.length - 1) * lineHeight;
    if (box.x !== item.x || lastBaseline !== item.baseline) adjustments.push({ id: 'activity_' + (i + 1), originalX: item.x, originalBaseline: item.baseline, actualX: box.x, actualBaseline: lastBaseline, reason: 'Attach extended single-line block near its scene; avoid window, decorative circles and title papers' });
    ctx.save(); ctx.fillStyle = spec.colors.labelBackground; ctx.fillRect(box.x, box.y, box.width, box.height);
    ctx.fillStyle = spec.colors.labelText;
    lines.forEach((line, row) => draw(line, box.x + rule.paddingX, lastBaseline - (lines.length - 1 - row) * lineHeight, rule.size, 'HB', rule.maximumTextWidth, 'activity_' + (i + 1)));
    ctx.restore(); labelBoxes.push(box);
  });
  const number = value => Number(value.toFixed(3));
  const sheet = (rect, angle, fill, opacity, strokeWidth, strokeOpacity, fold) => {
    const x = number(rect.x), y = number(rect.y), width = number(rect.width), height = number(rect.height);
    const centerX = number(x + width / 2), centerY = number(y + height / 2);
    const corner = fold ? `<path d="M${number(x + width - 50)} ${number(y + height)} V${number(y + height - 38)} H${number(x + width)}" fill="none" stroke="${spec.colors.outline}" stroke-width="2" stroke-opacity="0.45"/>` : '';
    return `<g transform="rotate(${angle} ${centerX} ${centerY})"><rect x="${x}" y="${y}" width="${width}" height="${height}" fill="${fill}" fill-opacity="${opacity}" stroke="${spec.colors.outline}" stroke-width="${strokeWidth}" stroke-opacity="${strokeOpacity}"/>${corner}</g>`;
  };
  const paperSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="3000" viewBox="0 0 2400 3000"><g id="title-paper-layers">${titlePapers.map(paper => sheet(paper.back, paper.backAngle, spec.colors.paperBack, 0.12, 2, 0.45, false) + sheet(paper.front, paper.frontAngle, spec.colors.paperFront, 0.84, 2.5, 0.65, true)).join('')}</g></svg>`;
  fs.mkdirSync(output, { recursive: true });
  fs.writeFileSync(path.join(output, 'title-paper-layers.svg'), paperSvg);
  fs.writeFileSync(path.join(output, 'typography-outlined.svg'), await canvas.toBuffer('svg', { outline: true }));
  fs.writeFileSync(path.join(output, 'text-metrics.json'), JSON.stringify({ registered, metrics, labelBoxes, titlePapers, adjustments, language: 'en' }, null, 2));
  console.log('Outlined typography generated. Composite with artwork and inspect the final poster before delivery.');
})().catch(error => { console.error(error.message); process.exit(1); });
