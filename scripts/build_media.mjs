import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const root = path.resolve(import.meta.dirname, '..');
const masters = path.join(root, '.media-archive', 'masters');
const output = path.join(root, 'static', 'atlas', 'media');
const jobs = JSON.parse(fs.readFileSync(path.join(root, 'scripts', 'media-jobs.json'), 'utf8'));
const report = {};

for (const [name, job] of Object.entries(jobs)) {
  const source = path.join(masters, job.master);
  let image = sharp(source);
  if (job.crop) {
    const { width, height } = await image.metadata();
    const [x0, y0, x1, y1] = job.crop;
    const left = Math.round(width * x0);
    const top = Math.round(height * y0);
    image = sharp(source).extract({ left, top, width: Math.round(width * x1) - left, height: Math.round(height * y1) - top });
  }
  const buffer = await image.toBuffer();
  const meta = await sharp(buffer).metadata();
  const { dominant } = await sharp(buffer).stats();
  const widths = [480, 960, 1600].filter((width) => width < meta.width);
  widths.push(Math.min(meta.width, 1600));
  const unique = [...new Set(widths)];
  for (const width of unique) {
    await sharp(buffer).resize({ width }).webp({ quality: 74, effort: 5 }).toFile(path.join(output, `${name}-${width}.webp`));
    await sharp(buffer).resize({ width }).avif({ quality: 50, effort: 4 }).toFile(path.join(output, `${name}-${width}.avif`));
  }
  const largest = unique.at(-1);
  report[name] = {
    src: `atlas/media/${name}`,
    widths: unique,
    width: largest,
    height: Math.round((meta.height * largest) / meta.width),
    color: `#${[dominant.r, dominant.g, dominant.b].map((value) => value.toString(16).padStart(2, '0')).join('')}`,
  };
}

console.log(JSON.stringify(report, null, 1));
