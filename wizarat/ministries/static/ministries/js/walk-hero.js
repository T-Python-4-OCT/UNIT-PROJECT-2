(() => {
  const hero = document.querySelector("[data-walk-hero]");
  if (!hero) return;

  const root = document.documentElement;
  const stage = hero.querySelector(".walk-stage");
  const canvas = hero.querySelector(".wh-dust");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const isCalm = () => reducedMotion.matches;
  const clamp = (value) => Math.min(1, Math.max(0, value));

  // Scroll progress through the tall section: 0 at the top, 1 when the scene hands over to the page.
  let progress = 0;
  const readProgress = () => {
    if (isCalm()) return 0;
    const stickyTop = parseFloat(getComputedStyle(stage).top) || 0;
    const travel = hero.offsetHeight - stage.offsetHeight;
    return travel > 0 ? clamp((stickyTop - hero.getBoundingClientRect().top) / travel) : 0;
  };
  const applyProgress = () => {
    hero.classList.toggle("is-still", isCalm());
    progress = readProgress();
    stage.style.setProperty("--p", progress.toFixed(4));
    hero.classList.toggle("is-walking", progress > 0.3);
  };
  let scrollQueued = false;
  const onScroll = () => {
    if (scrollQueued) return;
    scrollQueued = true;
    requestAnimationFrame(() => {
      scrollQueued = false;
      applyProgress();
    });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  applyProgress();

  // Drifting haze over the city: sand-coloured by day, blue with a warm city glow at night.
  const gl = canvas.getContext("webgl2", { alpha: true, premultipliedAlpha: true, antialias: false });
  if (!gl) {
    canvas.remove();
    return;
  }
  const vertexSource = `#version 300 es
  void main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.-1.,0,1);}`;
  const fragmentSource = `#version 300 es
  precision highp float;
  uniform vec2 R;uniform float T,K,P;out vec4 O;
  float h(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
  float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
    return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
  float fbm(vec2 p){float a=.5,s=0.;mat2 m=mat2(1.6,1.2,-1.2,1.6);p=mat2(.8,.6,-.6,.8)*p+5.3;for(int i=0;i<5;i++){s+=a*n(p);p=m*p;a*=.5;}return s;}
  void main(){
    vec2 uv=gl_FragCoord.xy/R;uv.y=1.-uv.y;
    vec2 p=vec2(uv.x*R.x/R.y,uv.y);
    float t=T*.05;
    vec2 w=vec2(fbm(p*1.3+vec2(t,-t*.6)),fbm(p*1.3+vec2(-t*.8,t)+7.));
    float d=fbm(p*1.9+w*1.7+vec2(t*1.6,-t*1.1+P*.8));
    float e=fbm(p*.9-w+vec2(-t,t*.5)+3.);
    float low=smoothstep(.70,1.04,uv.y+(d-.5)*.34);
    float side=(smoothstep(.2,.0,uv.x+(e-.5)*.28)+smoothstep(.8,1.,uv.x+(e-.5)*.28))*smoothstep(.25,.6,uv.y)*.2;
    float wisps=smoothstep(.5,.78,d)*smoothstep(.22,.5,uv.y)*smoothstep(.86,.6,uv.y)*(.18+P*.25);
    float a=clamp(low+side+wisps,0.,1.);
    vec3 c=mix(mix(vec3(.79,.70,.55),vec3(.97,.90,.78),d*1.15),mix(vec3(.15,.19,.29),vec3(.40,.45,.57),d*1.1),K);
    vec2 g=(uv-vec2(.62,.8))*vec2(1.7,2.6);
    c=mix(c,vec3(.86,.55,.27),K*exp(-dot(g,g)*3.2)*.42);
    O=vec4(c*a,a);
  }`;
  const compile = (type, source) => {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) console.error(gl.getShaderInfoLog(shader));
    return shader;
  };
  const program = gl.createProgram();
  gl.attachShader(program, compile(gl.VERTEX_SHADER, vertexSource));
  gl.attachShader(program, compile(gl.FRAGMENT_SHADER, fragmentSource));
  gl.linkProgram(program);
  gl.useProgram(program);
  const uniforms = Object.fromEntries(["R", "T", "K", "P"].map((name) => [name, gl.getUniformLocation(program, name)]));

  const isNight = () => (root.dataset.bsTheme === "dark" ? 1 : 0);
  let night = isNight();
  const draw = (now) => {
    night += (isNight() - night) * 0.08;
    gl.uniform2f(uniforms.R, canvas.width, canvas.height);
    gl.uniform1f(uniforms.T, now / 1000);
    gl.uniform1f(uniforms.K, night);
    gl.uniform1f(uniforms.P, progress);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
  const resize = () => {
    const width = Math.round(Math.min(stage.clientWidth, 960));
    const height = Math.round((width * stage.clientHeight) / Math.max(stage.clientWidth, 1));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      gl.viewport(0, 0, width, height);
    }
    night = isNight();
    draw(performance.now());
  };
  window.addEventListener("resize", resize);
  resize();

  // Animate the haze only while the stage is on screen and motion is allowed.
  let visible = true;
  let rafId = 0;
  const loop = (now) => {
    draw(now);
    rafId = requestAnimationFrame(loop);
  };
  const updateLoop = () => {
    applyProgress();
    const run = visible && !document.hidden && !isCalm();
    if (run && !rafId) rafId = requestAnimationFrame(loop);
    if (!run && rafId) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
    if (!run) resize();
  };
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      updateLoop();
    }).observe(stage);
  }
  document.addEventListener("visibilitychange", updateLoop);
  reducedMotion.addEventListener("change", updateLoop);
  new MutationObserver(updateLoop).observe(root, { attributes: true, attributeFilter: ["data-bs-theme"] });
  updateLoop();
})();
