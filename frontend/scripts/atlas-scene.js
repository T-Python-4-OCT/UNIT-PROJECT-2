import {
  BufferGeometry, CanvasTexture, Color, CylinderGeometry, DirectionalLight, Float32BufferAttribute,
  HemisphereLight, LineBasicMaterial, LineLoop, LineSegments, Mesh, MeshBasicMaterial, MeshStandardMaterial,
  NeutralToneMapping, OrthographicCamera, PlaneGeometry, Scene, Sprite, SpriteMaterial, SRGBColorSpace,
  Vector3, WebGLRenderer,
} from 'three';
import { addTerrain, elevation, position } from './atlas-terrain.js';

const entries = {
  neom: { anchor: [480, 157], label: [441, 119] },
  qiddiya: { anchor: [789, 297], label: [799, 353] },
  diriyah: { anchor: [816, 272], label: [849, 230] },
  roshn: { label: [995, 174] },
  'the-red-sea': { anchor: [525, 291], label: [470, 318] },
  amaala: { anchor: [491, 225], label: [443, 233] },
};

function addOcean(scene) {
  const geometry = new PlaneGeometry(2800, 2400, 32, 24).rotateX(-Math.PI / 2);
  const vertices = geometry.getAttribute('position');
  const shallow = new Color('#255649');
  const deep = new Color('#103a32');
  const colors = [];
  for (let i = 0; i < vertices.count; i++) {
    const x = vertices.getX(i);
    const z = vertices.getZ(i);
    const distance = Math.hypot(x * 0.6 + 85, z + 40);
    const shade = shallow.clone().lerp(deep, Math.min(1, distance / 770));
    colors.push(shade.r, shade.g, shade.b);
  }
  geometry.setAttribute('color', new Float32BufferAttribute(colors, 3));
  const water = new Mesh(geometry, new MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
  water.position.y = -0.1;
  scene.add(water);

  const lines = [];
  for (let offset = -1040; offset <= 1040; offset += 40) {
    lines.push(new Vector3(offset, 0, -1080), new Vector3(offset, 0, 1080));
    lines.push(new Vector3(-1080, 0, offset), new Vector3(1080, 0, offset));
  }
  scene.add(new LineSegments(new BufferGeometry().setFromPoints(lines), new LineBasicMaterial({
    color: '#afc7ad', transparent: true, opacity: 0.15, toneMapped: false,
  })));

  const coastIslands = [[458, 239, 4], [474, 264, 6], [489, 288, 4], [502, 309, 6], [518, 328, 5], [581, 399, 6], [582, 410, 3], [973, 274, 5]];
  const islandMaterial = new MeshStandardMaterial({ color: '#bba879', roughness: 0.92 });
  for (const [x, z, radius] of coastIslands) {
    const chip = new Mesh(new CylinderGeometry(radius * 0.72, radius, radius * 0.7, 5), islandMaterial);
    chip.position.copy(position(x, radius * 0.35, z));
    chip.rotation.y = z;
    scene.add(chip);
  }

  const compass = [];
  const corners = [position(1212, 0.25, 101), position(1221, 0.25, 125), position(1212, 0.25, 151), position(1203, 0.25, 125)];
  for (let i = 0; i < corners.length; i++) compass.push(corners[i], corners[(i + 1) % corners.length]);
  compass.push(corners[0], corners[2], position(1188, 0.25, 125), position(1236, 0.25, 125));
  scene.add(new LineSegments(new BufferGeometry().setFromPoints(compass), new LineBasicMaterial({ color: '#d7b77c', toneMapped: false })));
}

function badgeTexture(index, isNetwork, active) {
  const image = document.createElement('canvas');
  image.width = 96;
  image.height = 96;
  const ink = image.getContext('2d');
  ink.beginPath();
  if (isNetwork) {
    ink.moveTo(48, 3);
    ink.lineTo(93, 48);
    ink.lineTo(48, 93);
    ink.lineTo(3, 48);
    ink.closePath();
  } else {
    ink.arc(48, 48, 42, 0, Math.PI * 2);
  }
  ink.fillStyle = active ? '#f2cf88' : '#143a30';
  ink.strokeStyle = '#f2cf88';
  ink.lineWidth = 4;
  ink.fill();
  ink.stroke();
  ink.fillStyle = active ? '#143a30' : '#fff5df';
  ink.font = 'bold 34px sans-serif';
  ink.textAlign = 'center';
  ink.textBaseline = 'middle';
  ink.fillText(index, 48, 50);
  const texture = new CanvasTexture(image);
  texture.colorSpace = SRGBColorSpace;
  return texture;
}

function addMarkers(scene, links) {
  const leaders = [];
  const dot = new CylinderGeometry(3.2, 3.2, 0.8, 14);
  const dotMaterial = new MeshBasicMaterial({ color: '#e6c27c', toneMapped: false });
  const roshn = links.some((link) => link.dataset.project === 'roshn');

  if (roshn) {
    const networkColor = new LineBasicMaterial({ color: '#4f694f', opacity: 0.82, transparent: true, toneMapped: false });
    for (const [x, z] of [[638, 213], [697, 297], [743, 209], [899, 266], [705, 385]]) {
      const ring = Array.from({ length: 26 }, (_, i) => {
        const angle = i / 26 * 2 * Math.PI;
        return position(x + 8 * Math.cos(angle), elevation(x, z) + 3, z + 8 * Math.sin(angle));
      });
      scene.add(new LineLoop(new BufferGeometry().setFromPoints(ring), networkColor));
    }
  }

  const markers = links.flatMap((link, i) => {
    const entry = entries[link.dataset.project];
    if (!entry) return [];
    const index = link.querySelector('.atlas-link-index')?.textContent.trim() || String(i + 1).padStart(2, '0');
    const textures = [badgeTexture(index, !entry.anchor, false), badgeTexture(index, !entry.anchor, true)];
    const material = new SpriteMaterial({ map: textures[0], depthTest: false, depthWrite: false, toneMapped: false });
    const sprite = new Sprite(material);
    sprite.position.copy(position(entry.label[0], 65, entry.label[1]));
    sprite.renderOrder = 2;
    scene.add(sprite);

    if (entry.anchor) {
      const [x, z] = entry.anchor;
      const point = new Mesh(dot, dotMaterial);
      point.position.copy(position(x, elevation(x, z) + 2.6, z));
      scene.add(point);
      leaders.push(point.position, sprite.position);
    }
    return [{ link, sprite, textures }];
  });

  if (markers.length) {
    scene.add(new LineSegments(new BufferGeometry().setFromPoints(leaders), new LineBasicMaterial({
      color: '#e8c68d', opacity: 0.9, transparent: true, depthTest: false, toneMapped: false,
    })));
  } else {
    dot.dispose();
    dotMaterial.dispose();
  }
  return markers;
}

export function mountRelief({ stage, mount, links, onError }) {
  const canvas = document.createElement('canvas');
  const options = { alpha: false, antialias: true, powerPreference: 'low-power' };
  const context = canvas.getContext('webgl2', options);
  if (!context) throw new Error('WebGL 2 unavailable');

  const scene = new Scene();
  const camera = new OrthographicCamera(-1, 1, 1, -1, 1, 2400);
  const listener = new AbortController();
  const { signal } = listener;
  const projection = new Vector3();
  let renderer;
  let markers = [];
  let intersection;
  let resize;
  let frame = 0;
  let visible = false;
  let hovered;
  let focused;
  let badgeSize;

  function dispose() {
    listener.abort();
    intersection?.disconnect();
    resize?.disconnect();
    cancelAnimationFrame(frame);
    canvas.remove();
    const resources = new Set(markers.flatMap(({ textures }) => textures));
    scene.traverse(({ geometry, material }) => {
      if (geometry) resources.add(geometry);
      if (material) resources.add(material);
    });
    for (const resource of resources) resource.dispose();
    renderer?.dispose();
    context.getExtension('WEBGL_lose_context')?.loseContext();
  }

  function render() {
    frame = 0;
    if (!visible || document.hidden) return;
    const { width, height } = mount.getBoundingClientRect();
    if (!width || !height) return;
    const horizontal = Math.max(760, width / height * 455);
    const vertical = horizontal * height / width;
    camera.left = -horizontal / 2;
    camera.right = horizontal / 2;
    camera.top = vertical / 2;
    camera.bottom = -vertical / 2;
    camera.updateProjectionMatrix();

    badgeSize = width < 600 ? 31 : 36;
    for (const marker of markers) {
      const { sprite, textures } = marker;
      const size = badgeSize * horizontal / width;
      sprite.scale.set(size, size, 1);
      sprite.material.map = textures[Number(marker === hovered || marker === focused)];
    }
    const pixelRatio = Math.min(devicePixelRatio, 1.5);
    if (canvas.width !== Math.floor(width * pixelRatio) || canvas.height !== Math.floor(height * pixelRatio)) {
      renderer.setDrawingBufferSize(width, height, pixelRatio);
    }
    try {
      renderer.render(scene, camera);
      if (context.isContextLost()) throw new Error('WebGL context lost');
      canvas.style.visibility = '';
    } catch {
      onError();
    }
  }

  function schedule() {
    if (frame || !visible || document.hidden || signal.aborted) return;
    frame = requestAnimationFrame(render);
  }

  function markerAt(event) {
    const rect = canvas.getBoundingClientRect();
    let nearest;
    let nearestDistance = badgeSize / 2;
    for (const marker of markers) {
      projection.copy(marker.sprite.position).project(camera);
      const x = rect.left + (projection.x + 1) * rect.width / 2;
      const y = rect.top + (1 - projection.y) * rect.height / 2;
      const distance = Math.hypot(event.clientX - x, event.clientY - y);
      if (distance < nearestDistance) {
        nearestDistance = distance;
        nearest = marker;
      }
    }
    return nearest;
  }

  try {
    renderer = new WebGLRenderer({ ...options, canvas, context });
    renderer.toneMapping = NeutralToneMapping;
    renderer.debug.onShaderError = () => { throw new Error('Relief shader failed'); };
    camera.position.set(66, 550, 380);
    camera.lookAt(0, 22, 0);
    scene.background = new Color('#133c33');
    scene.add(new HemisphereLight('#fff4e1', '#7c6048', 1.25));
    const sunlight = new DirectionalLight('#fff2db', 2.0);
    sunlight.position.set(-280, 360, -240);
    scene.add(sunlight);
    addOcean(scene);
    addTerrain(scene);
    markers = addMarkers(scene, links);

    canvas.style.visibility = 'hidden';
    mount.append(canvas);
    canvas.addEventListener('webglcontextlost', (event) => {
      event.preventDefault();
      onError();
    }, { signal });
    canvas.addEventListener('pointermove', (event) => {
      const marker = markerAt(event);
      if (marker === hovered) return;
      hovered = marker;
      canvas.style.cursor = hovered ? 'pointer' : '';
      schedule();
    }, { signal });
    canvas.addEventListener('pointerleave', () => {
      hovered = undefined;
      canvas.style.cursor = '';
      schedule();
    }, { signal });
    canvas.addEventListener('click', (event) => markerAt(event)?.link.click(), { signal });
    for (const marker of markers) {
      marker.link.addEventListener('focus', () => {
        focused = marker;
        schedule();
      }, { signal });
      marker.link.addEventListener('blur', () => {
        focused = undefined;
        schedule();
      }, { signal });
    }

    resize = new ResizeObserver(schedule);
    resize.observe(stage);
    intersection = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      schedule();
    });
    intersection.observe(stage);
    document.addEventListener('visibilitychange', schedule, { signal });
    return { dispose };
  } catch (error) {
    dispose();
    throw error;
  }
}
