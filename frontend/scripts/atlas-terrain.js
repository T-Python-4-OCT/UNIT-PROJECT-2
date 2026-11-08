import {
  BufferGeometry, Color, DoubleSide, Float32BufferAttribute, LineBasicMaterial,
  LineLoop, LineSegments, Mesh, MeshStandardMaterial, ShapeUtils, Vector2, Vector3,
} from 'three';

const outline = [
  [443, 125], [484, 124], [498, 106], [559, 98], [585, 70], [644, 94], [668, 112],
  [717, 131], [763, 137], [788, 123], [833, 126], [863, 158], [878, 178], [904, 195],
  [906, 215], [934, 224], [961, 247], [948, 267], [965, 282], [980, 308], [992, 324],
  [983, 347], [1029, 353], [1052, 371], [1037, 395], [997, 421], [949, 432],
  [903, 448], [842, 473], [794, 460], [768, 446], [735, 449], [699, 433], [669, 440],
  [641, 426], [625, 433], [614, 403], [596, 393], [591, 374], [572, 362], [557, 342],
  [534, 330], [524, 314], [500, 295], [492, 271], [478, 254], [472, 235], [459, 218],
  [453, 199], [451, 176], [441, 158], [446, 143],
].map(([x, z]) => new Vector2(x, z));

const coast = outline.map((start, index) => {
  const end = outline[(index + 1) % outline.length];
  const dx = end.x - start.x;
  const dz = end.y - start.y;
  return { start, dx, dz, inverseLengthSquared: 1 / (dx * dx + dz * dz) };
});

const hills = [
  [515, 125, 80, 37, 25], [560, 120, 52, 54, 44], [632, 139, 49, 30, 19],
  [502, 192, 31, 67, 38], [530, 263, 26, 72, 26], [571, 325, 25, 58, 34],
  [621, 386, 45, 54, 51], [687, 404, 50, 48, 32], [779, 374, 99, 48, 29],
  [886, 386, 72, 39, 34], [945, 344, 78, 28, 15], [806, 192, 107, 54, 13],
];

export function position(x, y, z) {
  return new Vector3(x - 748, y, z - 278);
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
  const foothill = Math.min(1, coastalDistance(x, z) / 24);
  const ridges = 1 + 0.21 * Math.sin(x * 0.143 + z * 0.07) * Math.cos(z * 0.105 - x * 0.04);
  let height = 0;
  for (const [cx, cz, width, depth, peak] of hills) {
    height += peak * Math.exp(-(((x - cx) / width) ** 2 + ((z - cz) / depth) ** 2));
  }
  return 15 + foothill * (height * ridges + 2 * Math.sin(x * 0.059 + z * 0.063));
}

const limestone = new Color('#e4cca1');
const clay = new Color('#9e7350');
const dune = new Color('#caa171');

function landColor(x, y, z) {
  const ripple = Math.cos(z * 0.066 + Math.sin(x * 0.033) * 1.3);
  const grain = 0.92 + 0.09 * Math.sin(x * 8.37 + z * 17.62);
  return limestone.clone()
    .lerp(dune, Math.max(0, (z - 235) / 400 + ripple * 0.08))
    .lerp(clay, Math.min(0.88, Math.max(0, (y - 18) / 111)))
    .multiplyScalar(grain);
}

function splitTriangle(a, b, c, depth, addTriangle) {
  if (depth === 0) {
    addTriangle(a, b, c);
    return;
  }
  const ab = a.clone().lerp(b, 0.5);
  const bc = b.clone().lerp(c, 0.5);
  const ca = c.clone().lerp(a, 0.5);
  splitTriangle(a, ab, ca, depth - 1, addTriangle);
  splitTriangle(ab, b, bc, depth - 1, addTriangle);
  splitTriangle(ca, bc, c, depth - 1, addTriangle);
  splitTriangle(ab, bc, ca, depth - 1, addTriangle);
}

function contours(a, b, c, result) {
  const min = Math.min(a.y, b.y, c.y);
  const max = Math.max(a.y, b.y, c.y);
  for (let level = Math.max(25, Math.ceil(min / 5) * 5); level < max; level += 5) {
    for (const [from, to] of [[a, b], [b, c], [c, a]]) {
      if ((from.y <= level) === (to.y <= level)) continue;
      const t = (level - from.y) / (to.y - from.y);
      result.push(from.x + t * (to.x - from.x), level + 0.35, from.z + t * (to.z - from.z));
    }
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
    const color = landColor(point.x, y, point.y);
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
    splitTriangle(outline[a], outline[b], outline[c], 4, addTriangle);
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
    for (const point of [a, b, new Vector3(b.x, bottom, b.z), a, new Vector3(b.x, bottom, b.z), new Vector3(a.x, bottom, a.z)]) {
      vertices.push(point.x, point.y, point.z);
    }
  }
  const geometry = new BufferGeometry();
  geometry.setAttribute('position', new Float32BufferAttribute(vertices, 3));
  geometry.computeVertexNormals();
  scene.add(new Mesh(geometry, new MeshStandardMaterial({ color: tint, side: DoubleSide, roughness: 0.98 })));
}

function offshore(scene) {
  for (let band = 1; band <= 5; band++) {
    const points = outline.map(({ x, y }) => {
      const scale = 1 + band * 0.06;
      return position(740 + (x - 740) * scale, 0.15, 274 + (y - 274) * scale);
    });
    scene.add(new LineLoop(new BufferGeometry().setFromPoints(points), new LineBasicMaterial({
      color: '#b6c79c', transparent: true, opacity: 0.32 - 0.043 * band,
    })));
  }
}

export function addTerrain(scene) {
  offshore(scene);
  sediment(scene, 15, 10, '#b0875b');
  sediment(scene, 10, 6, '#9b714c');
  sediment(scene, 6, 0, '#7a5e47');

  const { surface, lines } = reliefGeometry();
  scene.add(new Mesh(surface, new MeshStandardMaterial({ vertexColors: true, roughness: 0.94 })));
  const contourGeometry = new BufferGeometry();
  contourGeometry.setAttribute('position', new Float32BufferAttribute(lines, 3));
  scene.add(new LineSegments(contourGeometry, new LineBasicMaterial({ color: '#795738', transparent: true, opacity: 0.44 })));
}
