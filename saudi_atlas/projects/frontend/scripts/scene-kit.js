import {
  BufferGeometry,
  CircleGeometry,
  Color,
  CylinderGeometry,
  DirectionalLight,
  Float32BufferAttribute,
  Group,
  HemisphereLight,
  LineBasicMaterial,
  LineSegments,
  Mesh,
  MeshBasicMaterial,
  NeutralToneMapping,
  PlaneGeometry,
  RingGeometry,
  SphereGeometry,
  Vector3,
  WebGLRenderer,
} from 'three';
import { position } from './atlas-terrain.js';

export const FIELD_OF_VIEW = 30;
export const TILT = 0.6;
export const HEAD_PIXELS = 11;
export const country = { target: new Vector3(27, 22, 7), width: 640, depth: 560 };

const options = { alpha: false, antialias: true, powerPreference: 'low-power' };

export const clamp = (value) => Math.min(1, Math.max(0, value));
export const easeOut = (value) => 1 - (1 - clamp(value)) ** 3;
export const easeInOut = (value) => {
  const t = clamp(value);
  return t * t * (3 - 2 * t);
};

export function createCanvas() {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('webgl2', options);
  if (!context) throw new Error('WebGL 2 unavailable');
  return { canvas, context };
}

export function createRenderer(canvas, context, name) {
  const renderer = new WebGLRenderer({ ...options, canvas, context });
  renderer.toneMapping = NeutralToneMapping;
  renderer.debug.onShaderError = () => {
    throw new Error(`${name} shader failed`);
  };
  return renderer;
}

export function addLights(scene) {
  scene.background = new Color('#133c33');
  scene.add(new HemisphereLight('#fff4e1', '#7c6048', 1.25));
  const sunlight = new DirectionalLight('#fff2db', 2.0);
  sunlight.position.set(-280, 360, -240);
  scene.add(sunlight);
}

export function fitCanvas(renderer, canvas, width, height) {
  const pixelRatio = Math.min(devicePixelRatio, 1.5);
  if (canvas.width !== Math.floor(width * pixelRatio) || canvas.height !== Math.floor(height * pixelRatio)) {
    renderer.setDrawingBufferSize(width, height, pixelRatio);
  }
}

export function disposeScene({ scene, renderer, context, canvas }) {
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

export function addOcean(scene) {
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
  scene.add(
    new LineSegments(
      new BufferGeometry().setFromPoints(lines),
      new LineBasicMaterial({
        color: '#afc7ad',
        transparent: true,
        opacity: 0.15,
        toneMapped: false,
      }),
    ),
  );

  const compass = [];
  const corners = [
    position(1212, 0.25, 101),
    position(1221, 0.25, 125),
    position(1212, 0.25, 151),
    position(1203, 0.25, 125),
  ];
  for (let i = 0; i < corners.length; i++) compass.push(corners[i], corners[(i + 1) % corners.length]);
  compass.push(corners[0], corners[2], position(1188, 0.25, 125), position(1236, 0.25, 125));
  scene.add(
    new LineSegments(
      new BufferGeometry().setFromPoints(compass),
      new LineBasicMaterial({ color: '#d7b77c', toneMapped: false }),
    ),
  );
}

export function distanceFor({ width, depth }, aspect) {
  const reach = Math.tan((FIELD_OF_VIEW * Math.PI) / 360);
  return 1.08 * Math.max((depth * Math.cos(TILT)) / 2 / reach, width / 2 / (reach * aspect));
}

export function worldPerPixel(distance, height) {
  return (2 * distance * Math.tan((FIELD_OF_VIEW * Math.PI) / 360)) / height;
}

export function pulseRing(color) {
  const ring = new Mesh(
    new RingGeometry(1.25, 1.5, 48).rotateX(-Math.PI / 2),
    new MeshBasicMaterial({
      color,
      transparent: true,
      opacity: 0,
      depthTest: false,
      toneMapped: false,
    }),
  );
  ring.renderOrder = 2;
  return ring;
}

export function pin(color) {
  const group = new Group();
  const material = new MeshBasicMaterial({ color, depthTest: false, toneMapped: false });
  const stem = new Mesh(new CylinderGeometry(0.16, 0.16, 5, 10).translate(0, 2.5, 0), material);
  const head = new Mesh(new SphereGeometry(1, 24, 16).translate(0, 5.6, 0), material);
  const foot = new Mesh(
    new CylinderGeometry(0.5, 0.5, 0.1, 20),
    new MeshBasicMaterial({ color: '#fff5dd', depthTest: false, toneMapped: false }),
  );
  for (const part of [foot, stem, head]) part.renderOrder = 3;
  group.add(foot, stem, head);
  return group;
}

export function communityRing(color) {
  const group = new Group();
  const part = (geometry, tint, opacity) => {
    const mesh = new Mesh(
      geometry.rotateX(-Math.PI / 2),
      new MeshBasicMaterial({
        color: tint,
        transparent: true,
        opacity,
        depthTest: false,
        toneMapped: false,
      }),
    );
    mesh.renderOrder = 3;
    mesh.userData.opacity = opacity;
    group.add(mesh);
  };
  part(new CircleGeometry(0.72, 40), color, 0.22);
  part(new RingGeometry(1, 1.22, 48), '#153a31', 0.6);
  part(new RingGeometry(0.72, 1, 48), color, 1);
  return group;
}

export function aim(camera, target, distance, yaw) {
  camera.position.set(
    target.x + Math.sin(yaw) * Math.sin(TILT) * distance,
    target.y + Math.cos(TILT) * distance,
    target.z + Math.cos(yaw) * Math.sin(TILT) * distance,
  );
  camera.lookAt(target);
}
