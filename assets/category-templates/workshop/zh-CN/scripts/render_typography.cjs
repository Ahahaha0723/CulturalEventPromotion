const fs = require('fs');
const path = require('path');

// node render_typography.cjs layout-text.json output-dir [skia-canvas-module-path]
(async () => {
  const [input, output, modulePath] = process.argv.slice(2);
  if (!input || !output) throw Error('Usage: node render_typography.cjs layout-text.json output-dir [skia-canvas-module-path]');
  const { Canvas, FontLibrary } = require(modulePath || 'skia-canvas');
  const root = path.resolve(__dirname, '..');
  const spec = JSON.parse(fs.readFileSync(path.join(root, 'references/layout-spec.json'), 'utf8'));
  const copy = JSON.parse(fs.readFileSync(input, 'utf8'));
  const registered = {};
  for (const [alias, [file]] of Object.entries(spec.fonts)) {
    registered[alias] = FontLibrary.use('Workshop_' + alias, path.join(root, spec.fontDirectory || 'fonts', file));
    if (!registered[alias].length) throw Error('Font registration failed: ' + file);
  }
  const canvas = new Canvas(spec.canvas.width, spec.canvas.height);
  const ctx = canvas.getContext('2d');
  ctx.textBaseline = 'alphabetic';
  const metrics = [], groups = [], adjustments = [];
  function measure(value, size, font) {
    if (typeof value !== 'string' || !value.trim()) throw Error('Missing visible copy');
    if (!spec.fonts[font]) throw Error('Unsupported Harmony font: ' + font);
    ctx.font = `${spec.fonts[font][1]} ${size}px Workshop_${font}`;
    return ctx.measureText(value);
  }
  function fitted(value, nominal, font, maxWidth, id) {
    const m = measure(value, nominal, font);
    if (m.width <= maxWidth) return nominal;
    const size = Math.floor(nominal * maxWidth / m.width * 10) / 10;
    if (size < nominal * spec.fit.minimumScale) throw Error('Text overflow: ' + id + '. Split at a semantic boundary without deleting facts.');
    adjustments.push({ id, nominalSize: nominal, actualSize: size, reason: 'Actual Harmony glyph width' });
    return size;
  }
  function draw(value, item, id) {
    if (item.lockSize && measure(value, item.size, item.font).width > item.maxWidth) throw Error('Uniform-size text overflow: ' + id + '. Split at a semantic boundary; do not shrink this line.');
    const size = item.lockSize ? item.size : fitted(value, item.size, item.font, item.maxWidth, id);
    const m = measure(value, size, item.font);
    const x = item.right !== undefined ? item.right - m.actualBoundingBoxRight : item.x + m.actualBoundingBoxLeft;
    const y = item.inkTop !== undefined ? item.inkTop + m.actualBoundingBoxAscent : item.baseline;
    if (!spec.colors[item.role]) throw Error('Unsupported text color role: ' + item.role);
    ctx.fillStyle = spec.colors[item.role];
    ctx.fillText(value, x, y);
    const row = { id, value, x, baseline: y, size, font: item.font,
      fontFile: spec.fonts[item.font][0], role: item.role, color: spec.colors[item.role],
      left: x - m.actualBoundingBoxLeft, top: y - m.actualBoundingBoxAscent,
      right: x + m.actualBoundingBoxRight, bottom: y + m.actualBoundingBoxDescent };
    metrics.push(row);
    return row;
  }
  function recordGroup(id, rows) {
    if (!rows.length) return null;
    const group = { id, left: Math.min(...rows.map(x => x.left)), top: Math.min(...rows.map(x => x.top)),
      right: Math.max(...rows.map(x => x.right)), bottom: Math.max(...rows.map(x => x.bottom)) };
    groups.push(group);
    return group;
  }
  function lines(values, item, id) {
    if (!Array.isArray(values) || values.length > item.maxLines) throw Error('Invalid line count: ' + id);
    const size = values.reduce((minimum, value) => Math.min(minimum, fitted(value, item.size, item.font, item.maxWidth, id)), item.size);
    const rows = values.map((value, i) => draw(value, { ...item, size, inkTop: item.inkTop + i * item.lineHeight }, id + '_' + (i + 1)));
    return recordGroup(id, rows);
  }
  if (!Array.isArray(copy.main_title_lines) || !copy.main_title_lines.length ||
      !Array.isArray(copy.right_title_lines) || !copy.right_title_lines.length) throw Error('Both semantic title columns are required.');
  const main = lines(copy.main_title_lines, spec.mainTitle, 'main_title');
  const rightTitle = lines(copy.right_title_lines, spec.rightTitle, 'right_title');
  const support = lines(copy.left_support_lines || [], { ...spec.leftSupport, inkTop: Math.max(spec.leftSupport.inkTop, main.bottom + 54, rightTitle.bottom + 54) }, 'left_support');
  const processGroup = lines(copy.left_process_lines || [], { ...spec.leftProcess, inkTop: Math.max(spec.leftProcess.inkTop, support ? support.bottom + 64 : spec.leftProcess.inkTop) }, 'left_process');
  const dateRow = draw(copy.date, { ...spec.date, inkTop: support ? support.top : spec.date.inkTop }, 'date');
  const timeRow = draw(copy.time, { ...spec.time, inkTop: dateRow.bottom + spec.time.gapAfterDate }, 'time');
  recordGroup('date_time', [dateRow, timeRow]);
  if (!Array.isArray(copy.detail_groups) || !copy.detail_groups.length) throw Error('Missing grouped event details.');
  let cursor = processGroup ? processGroup.top : spec.details.inkTop;
  if (cursor < timeRow.bottom + 54) throw Error('Date/time approaches the aligned details too closely. Reflow both linked left/right rows together; preserve their top alignment.');
  for (let i = 0; i < copy.detail_groups.length; i++) {
    const group = copy.detail_groups[i];
    if (!Array.isArray(group.lines) || !group.lines.length) throw Error('Empty detail group');
    const rows = [];
    for (let j = 0; j < group.lines.length; j++) {
      const line = group.lines[j];
      const actualSize = spec.details.uniformSize;
      if (line.size && line.size !== actualSize) adjustments.push({ id: 'detail_' + i + '_' + j, nominalSize: line.size, actualSize, reason: 'Uniform detail size; emphasis by weight only' });
      const emphasis = line.emphasis ?? (j === 0 && ['venue','tutor','booking'].includes(group.category || group.id));
      const item = { x: spec.details.x, inkTop: cursor, maxWidth: spec.details.maxWidth,
        size: actualSize, lockSize: true,
        font: emphasis ? spec.details.emphasisFont : 'Regular', role: line.role || 'general' };
      const row = draw(line.text, item, 'detail_' + i + '_' + j);
      rows.push(row);
      cursor = row.bottom + spec.details.lineGap;
    }
    recordGroup(group.id || 'detail_' + i, rows);
    cursor += spec.details.groupGap;
  }
  if (cursor - spec.details.groupGap - spec.details.lineGap > spec.details.maxBottom) throw Error('Detail groups exceed vertical capacity. Re-group facts; do not remove reservations or shrink to microtext.');
  // The lower block shares the actual rightmost ink edge of the upper column.
  const upperRight = Math.max(...metrics.filter(row => row.id.startsWith('right_title_') || row.id.startsWith('detail_') || ['date','time'].includes(row.id)).map(row => row.right));
  const footer = copy.footer_lines || [];
  if (!Array.isArray(footer) || footer.length > spec.footer.maxLines) throw Error('Footer exceeds the planned left-column rows. Reflow without shrinking.');
  const footerGroup = recordGroup('footer', footer.map((value, i) => draw(value, { ...spec.footer, baseline: spec.footer.firstBaseline + i * spec.footer.lineHeight }, 'footer_' + (i + 1))));
  const lowerLines = copy.lower_right_participation_lines || copy.fee_capacity_lines || [];
  const lowerSpec = spec.lowerRightParticipation;
  if (!Array.isArray(lowerLines) || lowerLines.length > lowerSpec.maxLines) throw Error('Lower-right participation block exceeds the planned rows');
  const right = Number.isFinite(upperRight) ? upperRight : lowerSpec.fallbackRight;
  const bottom = footerGroup ? footerGroup.bottom : lowerSpec.fallbackBottom;
  const normalized = lowerLines.map((line, i) => typeof line === 'string' ? {text:line,emphasis:i===0} : line);
  const measurements = normalized.map(line => measure(line.text, lowerSpec.size, line.emphasis ? 'Bold' : 'Regular'));
  const lastDescent = measurements.length ? measurements.at(-1).actualBoundingBoxDescent : 0;
  const lowerRows = normalized.map((line, i) => draw(line.text, { ...lowerSpec, right,
    baseline: bottom - lastDescent - (normalized.length - 1 - i) * lowerSpec.lineHeight,
    font: line.emphasis ? 'Bold' : 'Regular' }, 'lower_right_participation_' + (i + 1)));
  const lowerGroup = recordGroup('lower_right_participation', lowerRows);
  if (lowerGroup && (cursor > lowerGroup.top - lowerSpec.minGap ||
      (footerGroup && footerGroup.right > lowerGroup.left - lowerSpec.minGap))) throw Error('Lower-right participation block collides with upper text or left footer. Reflow the left footer and semantic lines without changing facts or font size.');
  for (const row of metrics) {
    if (row.left < 0 || row.right > spec.canvas.width || row.top < 0 || row.bottom > spec.canvas.height) throw Error('Text outside canvas: ' + row.id);
  }
  const padding = spec.graphic.maskPadding;
  const clearZones = groups.map(group => ({ id: group.id, x: Math.max(0, group.left - padding),
    y: Math.max(0, group.top - padding), width: Math.min(spec.canvas.width, group.right + padding) - Math.max(0, group.left - padding),
    height: Math.min(spec.canvas.height, group.bottom + padding) - Math.max(0, group.top - padding) }));
  const n = value => Number(value.toFixed(3));
  const mask = `<svg xmlns="http://www.w3.org/2000/svg" width="${spec.canvas.width}" height="${spec.canvas.height}" viewBox="0 0 ${spec.canvas.width} ${spec.canvas.height}"><defs><mask id="abstract-text-clearance" maskUnits="userSpaceOnUse" x="0" y="0" width="${spec.canvas.width}" height="${spec.canvas.height}" style="mask-type:luminance"><rect width="${spec.canvas.width}" height="${spec.canvas.height}" fill="white"/>${clearZones.map(rect => `<rect x="${n(rect.x)}" y="${n(rect.y)}" width="${n(rect.width)}" height="${n(rect.height)}" fill="black"/>`).join('')}</mask></defs></svg>`;
  fs.mkdirSync(output, { recursive: true });
  fs.writeFileSync(path.join(output, 'typography-outlined.svg'), await canvas.toBuffer('svg', { outline: true }));
  fs.writeFileSync(path.join(output, 'text-clearance-mask.svg'), mask);
  fs.writeFileSync(path.join(output, 'layout-metrics.json'), JSON.stringify({ registered, metrics, groups, clearZones, adjustments }, null, 2));
  console.log('Harmony typography generated. Clearance mask is legacy-only; compose dark graphic intersections as partial white glyphs.');
})().catch(error => { console.error(error.message); process.exit(1); });
