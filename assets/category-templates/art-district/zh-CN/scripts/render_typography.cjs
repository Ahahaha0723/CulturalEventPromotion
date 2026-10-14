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
  const fonts = {
    DY: ['澹雅明体DYmingB.ttf', 400], HB: ['HarmonyOS_Sans_SC_Bold.ttf', 700],
    HM: ['HarmonyOS_Sans_SC_Medium.ttf', 400], HR: ['HarmonyOS_Sans_SC_Regular.ttf', 400]
  };
  const registered = {};
  for (const [alias, [file]] of Object.entries(fonts)) {
    registered[alias] = FontLibrary.use('Exact_' + alias, path.join(root, 'assets/fonts', file));
    if (!registered[alias].length) throw Error('Font registration failed: ' + file);
  }
  const canvas = new Canvas(spec.canvas.width, spec.canvas.height);
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = spec.colors.text;
  ctx.textBaseline = 'alphabetic';
  const metrics = [], labelBoxes = [];
  function measure(value, size, alias) {
    if (typeof value !== 'string' || !value.trim()) throw Error('Missing or empty text');
    ctx.font = `${fonts[alias][1]} ${size}px Exact_${alias}`;
    return ctx.measureText(value);
  }
  function draw(value, x, y, size, alias, maxWidth, id) {
    const m = measure(value, size, alias);
    if (m.width > maxWidth) throw Error(`Fixed-layout overflow: ${id} (${m.width} > ${maxWidth}px). Preserve copy and font size; revise line breaks or report an explicit layout exception.`);
    ctx.fillText(value, x, y);
    metrics.push({ id, value, x, y, size, alias, width: m.width,
      left: x - m.actualBoundingBoxLeft, right: x + m.actualBoundingBoxRight,
      top: y - m.actualBoundingBoxAscent, bottom: y + m.actualBoundingBoxDescent });
  }
  function fixed(value, item, id) {
    const m = measure(value, item.size, item.font);
    const x = item.align === 'right' ? item.right - m.actualBoundingBoxRight :
      item.inkLeft !== undefined ? item.inkLeft + m.actualBoundingBoxLeft : item.x;
    const y = item.inkTop !== undefined ? item.inkTop + m.actualBoundingBoxAscent : item.baseline;
    draw(value, x, y, item.size, item.font, item.maxWidth, id);
    return y;
  }
  for (const key of ['title_lines', 'subtitle_lines', 'slogan_lines']) {
    if (!Array.isArray(copy[key]) || copy[key].length !== ({ title_lines: 2, subtitle_lines: 2, slogan_lines: 4 })[key]) {
      throw Error(key + ' must have the fixed number of semantic lines');
    }
  }
  if (!Array.isArray(copy.activity_labels) || copy.activity_labels.length !== 4 ||
      copy.activity_labels.some(v => typeof v !== 'string' || !v.trim()) || new Set(copy.activity_labels).size !== 4) {
    throw Error('This four-scene layout requires four unique activity labels; other counts need an explicit layout exception.');
  }
  const firstBaseline = fixed(copy.subtitle_lines[0], spec.text.subtitle[0], 'subtitle_1');
  fixed(copy.subtitle_lines[1], { ...spec.text.subtitle[1], baseline: firstBaseline + 80 }, 'subtitle_2');
  fixed(copy.date, spec.text.date, 'date');
  fixed(copy.opening_hours, spec.text.opening_hours, 'opening_hours');
  for (let i = 0; i < 4; i++) {
    const item = spec.text.slogan[i];
    const runs = typeof copy.slogan_lines[i] === 'string' ? [{ text: copy.slogan_lines[i], bold: false }] : copy.slogan_lines[i];
    if (!Array.isArray(runs) || !runs.length) throw Error('Invalid slogan runs');
    let width = 0;
    for (const run of runs) width += measure(run.text, item.size, run.bold ? 'HB' : 'HR').width;
    if (width > item.maxWidth) throw Error('Fixed-layout overflow: slogan_' + (i + 1));
    let cursor = item.x;
    for (const run of runs) {
      draw(run.text, cursor, item.baseline, item.size, run.bold ? 'HB' : 'HR', item.maxWidth, 'slogan_' + (i + 1));
      cursor += metrics[metrics.length - 1].width;
    }
  }
  ctx.fillStyle = spec.colors.title;
  copy.title_lines.forEach((line, i) => fixed(line, spec.text.title[i], 'title_' + (i + 1)));
  ctx.fillStyle = spec.colors.text;
  for (const key of ['venue', 'address', 'participation', 'call_to_action', 'organizer']) fixed(copy[key], spec.text[key], key);
  copy.activity_labels.forEach((value, i) => {
    const item = spec.text.activity_labels[i], m = measure(value, item.size, item.font);
    const box = { value, x: item.x, y: item.baseline - m.actualBoundingBoxAscent - 12,
      width: m.width + 36, height: m.actualBoundingBoxAscent + m.actualBoundingBoxDescent + 24 };
    if (box.x + box.width > spec.canvas.width - 150) throw Error('Label exceeds right safe margin: ' + value);
    ctx.save();
    ctx.fillStyle = spec.colors.labelBackground;
    ctx.fillRect(box.x, box.y, box.width, box.height);
    ctx.fillStyle = spec.colors.labelText;
    draw(value, item.x + 18, item.baseline, item.size, item.font, item.maxWidth, 'activity_' + (i + 1));
    ctx.restore();
    labelBoxes.push(box);
  });
  fs.mkdirSync(output, { recursive: true });
  fs.writeFileSync(path.join(output, 'typography-outlined.svg'), await canvas.toBuffer('svg', { outline: true }));
  fs.writeFileSync(path.join(output, 'text-metrics.json'), JSON.stringify({ registered, metrics, labelBoxes }, null, 2));
  console.log('Outlined typography generated. Composite with artwork and inspect the final poster before delivery.');
})().catch(error => { console.error(error.message); process.exit(1); });
