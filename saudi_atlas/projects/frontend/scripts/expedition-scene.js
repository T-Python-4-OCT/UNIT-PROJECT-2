import { Color, CylinderGeometry, Mesh, MeshBasicMaterial, PerspectiveCamera, Scene, Vector3 } from 'three';
import geography from '../../data/atlas-map.json';
import { addTerrain, elevation, position } from './atlas-terrain.js';
import {
  FIELD_OF_VIEW,
  HEAD_PIXELS,
  addLights,
  addOcean,
  aim,
  clamp,
  communityRing,
  country,
  createCanvas,
  createRenderer,
  disposeScene,
  distanceFor,
  easeInOut,
  easeOut,
  fitCanvas,
  pin,
  pulseRing,
  worldPerPixel,
} from './scene-kit.js';

export { loadTerrain } from './atlas-terrain.js';

const REGION = { width: 440, depth: 300 };

const HEADINGS = [-0.16, 0.12, -0.05, 0, 0.15, -0.1, 0.07];
const DOT_PIXELS = 4;
const RESPONSE = 3.2;

export function mountExpedition({ stage, mount, stops, direction, onReady, onError }) {
  const { canvas, context } = createCanvas();
  const scene = new Scene();
  const camera = new PerspectiveCamera(FIELD_OF_VIEW, 1, 10, 4000);
  const listener = new AbortController();
  const { signal } = listener;
  const side = direction === 'rtl' ? -1 : 1;
  const wide = { ...country, yaw: 0 };
  const last = stops.length - 1;
  const pose = { target: new Vector3(), distance: 0, yaw: 0 };
  const goal = { target: new Vector3(), distance: 0, yaw: 0 };
  let views = [];
  let sites = [];
  let communities = [];
  let renderer;
  let land;
  let contourMaterial;
  let intersection;
  let resize;
  let started = 0;
  let previous = 0;
  let frame = 0;
  let visible = false;
  let ready = false;
  let progress = -1;
  let shown = -1;
  let shift = 0;
  let measured = '';

  function dispose() {
    listener.abort();
    intersection?.disconnect();
    resize?.disconnect();
    cancelAnimationFrame(frame);
    disposeScene({ scene, renderer, context, canvas });
  }

  function reach(view, aspect) {
    return distanceFor(view, aspect * (1 - 2 * shift));
  }

  function aimFor(value, aspect) {
    let from;
    let to;
    let t;
    let lift = false;
    if (value <= -1 || value >= last + 1) {
      from = wide;
      to = wide;
      t = 0;
    } else if (value < 0) {
      from = wide;
      to = views[0];
      t = easeInOut(value + 1);
    } else if (value > last) {
      from = views[last];
      to = wide;
      t = easeInOut(value - last);
    } else {
      const index = Math.min(last - 1, Math.floor(value));
      from = views[index];
      to = views[index + 1];
      t = easeInOut(clamp((value - index - 0.18) / 0.64));
      lift = true;
    }
    const near = reach(from, aspect);
    const far = reach(to, aspect);
    goal.target.lerpVectors(from.target, to.target, t);
    goal.yaw = from.yaw + (to.yaw - from.yaw) * t;
    goal.distance = near + (far - near) * t;
    if (lift) {
      const middle = (near + far) / 2;
      const peak = Math.max(
        middle,
        Math.min(reach(wide, aspect) * 1.05, Math.max(near, far) + from.target.distanceTo(to.target) * 0.9),
      );
      goal.distance += (peak - middle) * Math.sin(Math.PI * t);
    }
  }

  function animate(now, width, height) {
    started ||= now;
    const elapsed = (now - started) / 1000;
    const step = Math.min(0.1, (now - (previous || now)) / 1000);
    previous = now;
    const follow = ready ? 1 - Math.exp(-step * RESPONSE) : 1;
    const aspect = width / height;

    land.scale.y = 0.04 + 0.96 * easeOut(elapsed / 1.4);
    contourMaterial.opacity = 0.44 * clamp((elapsed - 0.6) / 0.8);

    aimFor(progress, aspect);
    pose.target.lerp(goal.target, follow);
    pose.distance += (goal.distance - pose.distance) * follow;
    pose.yaw += (goal.yaw - pose.yaw) * follow;
    shown += (progress - shown) * follow;

    camera.aspect = aspect;
    aim(camera, pose.target, pose.distance, pose.yaw);
    if (shift) camera.setViewOffset(width, height, -side * shift * width, 0, width, height);
    else camera.clearViewOffset();
    camera.updateProjectionMatrix();

    const current = shown > -0.5 && shown < last + 0.5 ? Math.round(shown) : -1;
    const intro = easeOut((elapsed - 0.9) / 0.7);
    const pixel = worldPerPixel(pose.distance, height);
    for (const site of sites) {
      const ground = position(site.x, elevation(site.x, site.z) * land.scale.y + 0.6, site.z);
      site.grow += ((site.index === current ? 1 : 0) - site.grow) * (ready ? 1 - Math.exp(-step * 5) : 1);
      const head = HEAD_PIXELS * pixel * intro * site.grow;
      site.dot.position.copy(ground);
      site.dot.scale.setScalar(Math.max(0.001, DOT_PIXELS * pixel * intro * (1 - site.grow)));
      site.pin.position.copy(ground);
      site.pin.scale.setScalar(Math.max(0.001, head));
      site.pulses.forEach((pulse, index) => {
        const cycle = (elapsed * 0.4 + index * 0.5) % 1;
        pulse.position.copy(ground);
        pulse.scale.setScalar(Math.max(0.001, head * (1 + cycle * 4)));
        pulse.material.opacity = site.grow * 0.8 * (1 - cycle) ** 2;
      });
    }
    for (const ring of communities) {
      ring.grow += ((ring.index === current ? 1 : 0) - ring.grow) * (ready ? 1 - Math.exp(-step * 5) : 1);
      ring.mesh.position.copy(position(ring.x, elevation(ring.x, ring.z) * land.scale.y + 0.6, ring.z));
      ring.mesh.scale.setScalar(HEAD_PIXELS * pixel);
      for (const part of ring.mesh.children)
        part.material.opacity = part.userData.opacity * intro * ring.grow;
      ring.mesh.visible = ring.grow > 0.01;
    }
  }

  function render(now) {
    frame = 0;
    if (!visible || document.hidden) return;
    const { width, height } = mount.getBoundingClientRect();
    if (!width || !height) return;
    const size = `${width}x${height}`;
    if (size !== measured) {
      measured = size;
      shift = clamp(parseFloat(getComputedStyle(stage).getPropertyValue('--frame-shift')) || 0) * 0.9;
    }
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
    renderer = createRenderer(canvas, context, 'Expedition');
    addLights(scene);
    addOcean(scene);
    ({ land, contourMaterial } = addTerrain(scene));

    const dot = new CylinderGeometry(1, 1, 0.3, 16);
    const dotMaterial = new MeshBasicMaterial({ color: '#e6c27c', depthTest: false, toneMapped: false });
    views = stops.map((stop, index) => {
      if (!stop.anchor) {
        const color = new Color(stop.accent);
        geography.communities.forEach(([x, z]) => {
          const mesh = communityRing(color);
          scene.add(mesh);
          communities.push({ x, z, index, mesh, grow: 0 });
        });
        return wide;
      }
      const [x, z] = stop.anchor;
      const color = new Color(stop.accent);
      const site = {
        x,
        z,
        index,
        grow: 0,
        dot: new Mesh(dot, dotMaterial),
        pin: pin(color),
        pulses: [pulseRing(color), pulseRing(color)],
      };
      site.dot.renderOrder = 1;
      scene.add(site.dot, site.pin, ...site.pulses);
      sites.push(site);
      return { ...REGION, target: position(x, elevation(x, z), z), yaw: HEADINGS[index % HEADINGS.length] };
    });

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
      previous = 0;
      schedule();
    });
    intersection.observe(stage);
    document.addEventListener(
      'visibilitychange',
      () => {
        previous = 0;
        schedule();
      },
      { signal },
    );
    return {
      setProgress(value) {
        if (Number.isFinite(value)) progress = Math.max(-1.5, Math.min(last + 1.5, value));
      },
      dispose,
    };
  } catch (error) {
    dispose();
    throw error;
  }
}
