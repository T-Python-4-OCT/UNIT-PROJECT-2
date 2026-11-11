import {
  BufferGeometry,
  Color,
  DoubleSide,
  Float32BufferAttribute,
  Group,
  LineBasicMaterial,
  LineSegments,
  Mesh,
  MeshStandardMaterial,
  ShapeUtils,
  Vector2,
  Vector3,
} from 'three';
import geography from '../../data/atlas-map.json';
import heightUrl from '../assets/saudi-height.png';

const outline = geography.outline.map(([x, z]) => new Vector2(x, z));

const coast = outline.map((start, index) => {
  const end = outline[(index + 1) % outline.length];
  const dx = end.x - start.x;
  const dz = end.y - start.y;
  return { start, dx, dz, inverseLengthSquared: 1 / (dx * dx + dz * dz) };
});

const terrain = geography.terrain;

const RELIEF = 57;
const BASE = 15;
const unitsPerLevel = RELIEF / 255;
let heights;
let loading;

export function loadTerrain() {
  loading ??= (async () => {
    const response = await fetch(heightUrl);
    if (!response.ok) throw new Error(`Heightmap ${response.status}`);
    const bitmap = await createImageBitmap(await response.blob(), {
      colorSpaceConversion: 'none',
      premultiplyAlpha: 'none',
    });
    if (bitmap.width !== terrain.columns || bitmap.height !== terrain.rows) throw new Error('Heightmap size');
    const canvas = document.createElement('canvas');
    canvas.width = bitmap.width;
    canvas.height = bitmap.height;
    const context = canvas.getContext('2d', { willReadFrequently: true });
    if (!context) throw new Error('Canvas 2D unavailable');
    context.drawImage(bitmap, 0, 0);
    bitmap.close();
    const { data } = context.getImageData(0, 0, canvas.width, canvas.height);
    const red = new Uint8Array(canvas.width * canvas.height);
    for (let i = 0; i < red.length; i++) red[i] = data[i * 4];
    heights = red;
  })().catch((error) => {
    loading = undefined;
    throw error;
  });
  return loading;
}

function level(x, z) {
  if (!heights) return 0;
  const { columns, rows, cell } = terrain;
  const fx = (x - terrain.x) / cell - 0.5;
  const fz = (z - terrain.y) / cell - 0.5;
  if (fx < -0.5 || fz < -0.5 || fx > columns - 0.5 || fz > rows - 0.5) return 0;
  const x0 = Math.max(0, Math.min(columns - 2, Math.floor(fx)));
  const z0 = Math.max(0, Math.min(rows - 2, Math.floor(fz)));
  const tx = Math.max(0, Math.min(1, fx - x0));
  const tz = Math.max(0, Math.min(1, fz - z0));
  const at = (column, row) => heights[row * columns + column];
  const top = at(x0, z0) * (1 - tx) + at(x0 + 1, z0) * tx;
  const bottom = at(x0, z0 + 1) * (1 - tx) + at(x0 + 1, z0 + 1) * tx;
  return top * (1 - tz) + bottom * tz;
}

export function position(x, y, z) {
  return new Vector3(x - 725, y, z - 276);
}

function coastalDistance(x, z) {
  let closest = Infinity;
  for (const { start, dx, dz, inverseLengthSquared } of coast) {
    const xOffset = x - start.x;
    const zOffset = z - start.y;
    const t = Math.max(0, Math.min(1, (xOffset * dx + zOffset * dz) * inverseLengthSquared));
    closest = Math.min(closest, (xOffset - t * dx) ** 2 + (zOffset - t * dz) ** 2);
  }
  return Math.sqrt(closest);
}

export function elevation(x, z) {
  const ramp = Math.min(1, coastalDistance(x, z) / 8);
  return BASE + ramp * level(x, z) * unitsPerLevel;
}

const limestone = new Color('#e6d1a8');
const sand = new Color('#cfa978');
const clay = new Color('#97694a');

function landColor(x, y) {
  const height = Math.max(0, Math.min(1, (y - BASE) / RELIEF));
  return limestone
    .clone()
    .lerp(sand, Math.min(1, height / 0.35))
    .lerp(clay, Math.max(0, Math.min(1, (height - 0.3) / 0.55)))
    .multiplyScalar(0.96);
}

const edge = 4.5;

function midpoint(a, b) {
  return new Vector2((a.x + b.x) / 2, (a.y + b.y) / 2);
}

function refine(a, b, c, addTriangle) {
  const ab = a.distanceToSquared(b);
  const bc = b.distanceToSquared(c);
  const ca = c.distanceToSquared(a);
  const longest = Math.max(ab, bc, ca);
  if (longest <= edge * edge) {
    addTriangle(a, b, c);
  } else if (longest === ab) {
    const middle = midpoint(a, b);
    refine(a, middle, c, addTriangle);
    refine(middle, b, c, addTriangle);
  } else if (longest === bc) {
    const middle = midpoint(b, c);
    refine(a, b, middle, addTriangle);
    refine(a, middle, c, addTriangle);
  } else {
    const middle = midpoint(c, a);
    refine(a, b, middle, addTriangle);
    refine(middle, b, c, addTriangle);
  }
}

function isoline(a, b, c, level, y, result) {
  for (const [from, to] of [
    [a, b],
    [b, c],
    [c, a],
  ]) {
    if (from.y <= level === to.y <= level) continue;
    const t = (level - from.y) / (to.y - from.y);
    result.push(from.x + t * (to.x - from.x), y, from.z + t * (to.z - from.z));
  }
}

const contourStep = (300 / terrain.max_metres) * RELIEF;

function contours(a, b, c, result) {
  const min = Math.min(a.y, b.y, c.y);
  const max = Math.max(a.y, b.y, c.y);
  const first = Math.max(1, Math.ceil((min - BASE) / contourStep));
  for (let height = BASE + first * contourStep; height < max; height += contourStep) {
    isoline(a, b, c, height, height + 0.35, result);
  }
}

function reliefGeometry() {
  const vertices = [];
  const colors = [];
  const indices = [];
  const lines = [];
  const points = [];
  const weld = new Map();

  function vertex(point) {
    const key = `${point.x.toFixed(4)},${point.y.toFixed(4)}`;
    if (weld.has(key)) return weld.get(key);
    const y = elevation(point.x, point.y);
    const world = position(point.x, y, point.y);
    const color = landColor(point.x, y);
    const index = points.push(world) - 1;
    vertices.push(world.x, world.y, world.z);
    colors.push(color.r, color.g, color.b);
    weld.set(key, index);
    return index;
  }

  function addTriangle(a, b, c) {
    const one = vertex(a);
    const two = vertex(b);
    const three = vertex(c);
    const positiveArea = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x) > 0;
    indices.push(one, positiveArea ? three : two, positiveArea ? two : three);
    contours(points[one], points[two], points[three], lines);
  }

  for (const [a, b, c] of ShapeUtils.triangulateShape(outline, [])) {
    refine(outline[a], outline[b], outline[c], addTriangle);
  }

  const surface = new BufferGeometry();
  surface.setAttribute('position', new Float32BufferAttribute(vertices, 3));
  surface.setAttribute('color', new Float32BufferAttribute(colors, 3));
  surface.setIndex(indices);
  surface.computeVertexNormals();
  return { surface, lines };
}

function sediment(scene, top, bottom, tint) {
  const vertices = [];
  for (const { start, dx, dz } of coast) {
    const a = position(start.x, top, start.y);
    const b = position(start.x + dx, top, start.y + dz);
    for (const point of [
      a,
      b,
      new Vector3(b.x, bottom, b.z),
      a,
      new Vector3(b.x, bottom, b.z),
      new Vector3(a.x, bottom, a.z),
    ]) {
      vertices.push(point.x, point.y, point.z);
    }
  }
  const geometry = new BufferGeometry();
  geometry.setAttribute('position', new Float32BufferAttribute(vertices, 3));
  geometry.computeVertexNormals();
  scene.add(new Mesh(geometry, new MeshStandardMaterial({ color: tint, side: DoubleSide, roughness: 0.98 })));
}

function inland(x, z) {
  let inside = false;
  for (const { start, dx, dz } of coast) {
    if (start.y > z !== start.y + dz > z && x < start.x + ((z - start.y) / dz) * dx) inside = !inside;
  }
  return inside;
}

function offshore(scene) {
  const spacing = 11;
  const bands = 5;
  const cell = 4;
  const reach = spacing * bands + cell;
  const west = Math.min(...outline.map(({ x }) => x)) - reach;
  const north = Math.min(...outline.map(({ y }) => y)) - reach;
  const columns = Math.ceil((Math.max(...outline.map(({ x }) => x)) + reach - west) / cell);
  const rows = Math.ceil((Math.max(...outline.map(({ y }) => y)) + reach - north) / cell);
  const samples = [];
  for (let row = 0; row <= rows; row++) {
    for (let column = 0; column <= columns; column++) {
      const x = west + column * cell;
      const z = north + row * cell;
      samples.push(position(x, inland(x, z) ? 0 : coastalDistance(x, z), z));
    }
  }

  const rings = Array.from({ length: bands }, () => []);
  for (let row = 0; row < rows; row++) {
    for (let column = 0; column < columns; column++) {
      const corner = row * (columns + 1) + column;
      const a = samples[corner];
      const b = samples[corner + 1];
      const c = samples[corner + columns + 2];
      const d = samples[corner + columns + 1];
      for (let band = 1; band <= bands; band++) {
        const level = band * spacing;
        if (Math.min(a.y, b.y, c.y, d.y) >= level || Math.max(a.y, b.y, c.y, d.y) <= level) continue;
        isoline(a, b, c, level, 0.15, rings[band - 1]);
        isoline(a, c, d, level, 0.15, rings[band - 1]);
      }
    }
  }

  rings.forEach((ring, index) => {
    const geometry = new BufferGeometry();
    geometry.setAttribute('position', new Float32BufferAttribute(ring, 3));
    scene.add(
      new LineSegments(
        geometry,
        new LineBasicMaterial({
          color: '#b6c79c',
          transparent: true,
          opacity: 0.32 - 0.043 * (index + 1),
        }),
      ),
    );
  });
}

export function addTerrain(scene) {
  offshore(scene);
  const land = new Group();
  sediment(land, 15, 10, '#b0875b');
  sediment(land, 10, 6, '#9b714c');
  sediment(land, 6, 0, '#7a5e47');

  const { surface, lines } = reliefGeometry();
  land.add(new Mesh(surface, new MeshStandardMaterial({ vertexColors: true, roughness: 0.94 })));
  const contourGeometry = new BufferGeometry();
  contourGeometry.setAttribute('position', new Float32BufferAttribute(lines, 3));
  const contourMaterial = new LineBasicMaterial({ color: '#795738', transparent: true, opacity: 0.44 });
  land.add(new LineSegments(contourGeometry, contourMaterial));
  scene.add(land);
  return { land, contourMaterial };
}
