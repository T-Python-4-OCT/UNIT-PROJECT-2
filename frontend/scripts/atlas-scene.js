import {
  BufferGeometry, Color, CylinderGeometry, DirectionalLight, Float32BufferAttribute,
  HemisphereLight, LineBasicMaterial, LineLoop, LineSegments, Mesh, MeshBasicMaterial, MeshStandardMaterial,
  NeutralToneMapping, OrthographicCamera, PlaneGeometry, Scene, Vector3, WebGLRenderer,
} from 'three';
import geography from '../../projects/data/atlas-map.json';
import { addTerrain, elevation, position } from './atlas-terrain.js';

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

  const compass = [];
  const corners = [position(1212, 0.25, 101), position(1221, 0.25, 125), position(1212, 0.25, 151), position(1203, 0.25, 125)];
  for (let i = 0; i < corners.length; i++) compass.push(corners[i], corners[(i + 1) % corners.length]);
  compass.push(corners[0], corners[2], position(1188, 0.25, 125), position(1236, 0.25, 125));
  scene.add(new LineSegments(new BufferGeometry().setFromPoints(compass), new LineBasicMaterial({ color: '#d7b77c', toneMapped: false })));
}

function addMarkers(scene, links) {
  const leaders = [];
  const dot = new CylinderGeometry(3.2, 3.2, 0.8, 14);
  const dotMaterial = new MeshBasicMaterial({ color: '#e6c27c', toneMapped: false });
  const roshn = links.some((link) => link.dataset.project === 'roshn');

  if (roshn) {
    const networkColor = new LineBasicMaterial({ color: '#4f694f', opacity: 0.82, transparent: true, toneMapped: false });
    for (const [x, z] of geography.communities) {
      const height = elevation(x, z) + 3;
      const ring = Array.from({ length: 26 }, (_, i) => {
        const angle = i / 26 * 2 * Math.PI;
        return position(x + 6 * Math.cos(angle), height, z + 6 * Math.sin(angle));
      });
      scene.add(new LineLoop(new BufferGeometry().setFromPoints(ring), networkColor));
    }
  }

  const markers = links.flatMap((link) => {
    const entry = geography.projects[link.dataset.project];
    if (!entry) return [];
    const label = position(entry.label[0], 22, entry.label[1]);

    if (entry.anchor) {
      const [x, z] = entry.anchor;
      const point = new Mesh(dot, dotMaterial);
      point.position.copy(position(x, elevation(x, z) + 2.6, z));
      scene.add(point);
      leaders.push(point.position, label);
    }
    return [{ link, label }];
  });

  if (leaders.length) {
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

  function dispose() {
    listener.abort();
    intersection?.disconnect();
    resize?.disconnect();
    cancelAnimationFrame(frame);
    mount.removeAttribute('data-relief-ready');
    canvas.remove();
    const resources = new Set();
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
    const horizontal = Math.max(700, width / height * 500);
    const vertical = horizontal * height / width;
    camera.left = -horizontal / 2;
    camera.right = horizontal / 2;
    camera.top = vertical / 2;
    camera.bottom = -vertical / 2;
    camera.updateProjectionMatrix();

    const pixelRatio = Math.min(devicePixelRatio, 1.5);
    if (canvas.width !== Math.floor(width * pixelRatio) || canvas.height !== Math.floor(height * pixelRatio)) {
      renderer.setDrawingBufferSize(width, height, pixelRatio);
    }
    try {
      renderer.render(scene, camera);
      if (context.isContextLost()) throw new Error('WebGL context lost');
      for (const { link, label } of markers) {
        projection.copy(label).project(camera);
        link.style.setProperty('--relief-x', `${(projection.x + 1) * 50}%`);
        link.style.setProperty('--relief-y', `${(1 - projection.y) * 50}%`);
      }
      mount.setAttribute('data-relief-ready', '');
      canvas.style.visibility = '';
    } catch {
      onError();
    }
  }

  function schedule() {
    if (frame || !visible || document.hidden || signal.aborted) return;
    frame = requestAnimationFrame(render);
  }

  try {
    renderer = new WebGLRenderer({ ...options, canvas, context });
    renderer.toneMapping = NeutralToneMapping;
    renderer.debug.onShaderError = () => { throw new Error('Relief shader failed'); };
    camera.position.set(0, 700, 220);
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
