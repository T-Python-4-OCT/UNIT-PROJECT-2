import { Color, PerspectiveCamera, Scene, Vector3 } from 'three';
import geography from '../../data/atlas-map.json';
import { addTerrain, elevation, position } from './atlas-terrain.js';
import {
  FIELD_OF_VIEW,
  HEAD_PIXELS,
  addLights,
  addOcean,
  aim,
  clamp,
  country,
  createCanvas,
  createRenderer,
  disposeScene,
  distanceFor,
  easeInOut,
  easeOut,
  fitCanvas,
  pin,
  worldPerPixel,
} from './scene-kit.js';

export { loadTerrain } from './atlas-terrain.js';

export function mountLocator({ stage, mount, accent, anchor, onReady, onError }) {
  const { canvas, context } = createCanvas();
  const scene = new Scene();
  const camera = new PerspectiveCamera(FIELD_OF_VIEW, 1, 10, 4000);
  const listener = new AbortController();
  const { signal } = listener;
  const color = new Color(accent);
  const target = new Vector3();
  const places = [];
  let close;
  let renderer;
  let land;
  let contourMaterial;
  let intersection;
  let resize;
  let started = 0;
  let frame = 0;
  let visible = false;
  let ready = false;

  function dispose() {
    listener.abort();
    intersection?.disconnect();
    resize?.disconnect();
    cancelAnimationFrame(frame);
    disposeScene({ scene, renderer, context, canvas });
  }

  function addPlace(x, z, marker, order) {
    const place = { x, z, marker, order };
    scene.add(marker);
    places.push(place);
  }

  function animate(now, width, height) {
    started ||= now;
    const elapsed = (now - started) / 1000;
    const aspect = width / height;
    const fly = close ? easeInOut((elapsed - 1.1) / 2.6) : 0;
    const distance =
      distanceFor(country, aspect) +
      (close ? (distanceFor(close, aspect) - distanceFor(country, aspect)) * fly : 0);
    const yaw = 0.3 * Math.sin(elapsed * 0.22) * (0.35 + 0.65 * (close ? fly : 1));

    land.scale.y = 0.04 + 0.96 * easeOut(elapsed / 1.4);
    contourMaterial.opacity = 0.44 * clamp((elapsed - 0.6) / 0.8);
    target.copy(country.target);
    if (close) target.lerp(close.target, fly);
    camera.aspect = aspect;
    aim(camera, target, distance, yaw);
    camera.updateProjectionMatrix();

    const unit = HEAD_PIXELS * worldPerPixel(distance, height);
    for (const { x, z, marker, order } of places) {
      const grow = easeOut((elapsed - 0.9 - order * 0.12) / 0.7);
      const ground = position(x, elevation(x, z) * land.scale.y + 0.6, z);
      marker.position.copy(ground);
      marker.scale.setScalar(Math.max(0.001, unit * grow));
    }
  }

  function render(now) {
    frame = 0;
    if (!visible || document.hidden) return;
    const { width, height } = mount.getBoundingClientRect();
    if (!width || !height) return;
    fitCanvas(renderer, canvas, width, height);
    try {
      animate(now, width, height);
      renderer.render(scene, camera);
      if (context.isContextLost()) throw new Error('WebGL context lost');
      if (!ready) {
        ready = true;
        canvas.style.visibility = '';
        onReady();
      }
      schedule();
    } catch {
      onError();
    }
  }

  function schedule() {
    if (frame || !visible || document.hidden || signal.aborted) return;
    frame = requestAnimationFrame(render);
  }

  try {
    renderer = createRenderer(canvas, context, 'Locator');
    addLights(scene);
    addOcean(scene);
    ({ land, contourMaterial } = addTerrain(scene));

    if (anchor) {
      const [x, z] = anchor;
      close = { target: position(x, elevation(x, z), z), width: 400, depth: 270 };
      addPlace(x, z, pin(color), 0);
    } else {
      geography.communities.forEach(([x, z], index) => addPlace(x, z, pin(color), index));
    }

    canvas.style.visibility = 'hidden';
    mount.append(canvas);
    canvas.addEventListener(
      'webglcontextlost',
      (event) => {
        event.preventDefault();
        onError();
      },
      { signal },
    );
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
