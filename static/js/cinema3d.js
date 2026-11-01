/* Real-time 3D layer (Three.js, self-hosted): four procedural scene objects for the hero story, then one small
   companion in the bottom-right corner that changes with each section (models generated with Higgsfield / Tripo,
   static/models/*.glb). It never covers page content. */
import * as THREE from "./vendor/three.module.min.js";
import { GLTFLoader } from "./vendor/GLTFLoader.js";

const canvas = document.getElementById("core-canvas");
const root = document.documentElement;
const reduced = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
const small = () => window.innerWidth < 760;

function boot() {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: !small(), powerPreference: "high-performance" });
  } catch (e) { root.classList.add("no-webgl"); return; }
  if (!renderer.getContext()) { root.classList.add("no-webgl"); return; }

  let dprCap = small() ? 1.25 : 1.75;
  const setSize = () => {
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, dprCap));
    renderer.setSize(window.innerWidth, window.innerHeight, false);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
  };
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 60);
  camera.position.set(0, 0, 7);

  /* ---- image-based lighting from a tiny studio scene (cool whites, cyan, blue; no warm light) ---- */
  const envScene = new THREE.Scene();
  const panel = (w, h, x, y, z, color, i) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(i), side: THREE.DoubleSide }));
    m.position.set(x, y, z); m.lookAt(0, 0, 0); envScene.add(m);
  };
  envScene.background = new THREE.Color(0x05090a);
  panel(8, 3, 0, 6, 2, 0xeef1f3, 3.2);
  panel(3, 8, -6, 0, 2, 0x7cd0d9, 2.2);
  panel(3, 8, 6, 1, -1, 0x0b6670, 3.0);
  panel(10, 2, 0, -5, 3, 0xc9d3d8, 1.0);
  panel(6, 6, 0, 2, -7, 0x9fd8de, 1.4);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(envScene, 0.03).texture;
  const key = new THREE.DirectionalLight(0xe3f6f8, 1.6); key.position.set(3, 4, 5); scene.add(key);
  const rim = new THREE.DirectionalLight(0x7cd0d9, 1.4); rim.position.set(-4, 1, -3); scene.add(rim);
  scene.add(new THREE.AmbientLight(0x0b6670, 0.35));

  /* ---- materials ---- */
  const CYAN = new THREE.Color(0x7cd0d9);
  const titanium = new THREE.MeshStandardMaterial({ color: 0xc9d3d8, metalness: 1, roughness: 0.34 });
  const graphite = new THREE.MeshStandardMaterial({ color: 0x1a2428, metalness: 0.85, roughness: 0.45 });
  const darkMetal = new THREE.MeshStandardMaterial({ color: 0x2a373c, metalness: 1, roughness: 0.28 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0xcdeaec, metalness: 0, roughness: 0.18, transparent: true, opacity: 0.28, clearcoat: 1, clearcoatRoughness: 0.1, side: THREE.DoubleSide, depthWrite: false });
  const frosted = new THREE.MeshPhysicalMaterial({ color: 0xdbeaeb, metalness: 0, roughness: 0.62, transparent: true, opacity: 0.38, clearcoat: 0.4, side: THREE.DoubleSide, depthWrite: false });
  const glow = new THREE.MeshBasicMaterial({ color: CYAN, toneMapped: false });
  const glowSoft = new THREE.MeshBasicMaterial({ color: CYAN, transparent: true, opacity: 0.55, toneMapped: false });
  const lineMat = (o) => new THREE.LineBasicMaterial({ color: CYAN, transparent: true, opacity: o, toneMapped: false });
  const pulseMats = [glow, glowSoft];
  const pulseLines = [];

  /* ---- builders ---- */
  const seg = small() ? 0.6 : 1;
  const S = (n) => Math.max(6, Math.round(n * seg));
  const mesh = (g, m, x = 0, y = 0, z = 0) => { const o = new THREE.Mesh(g, m); o.position.set(x, y, z); return o; };

  function gear(R, r, teeth, thick) {
    const sh = new THREE.Shape(); const step = (Math.PI * 2) / teeth;
    for (let i = 0; i < teeth; i++) {
      const a = i * step;
      const p = [[R * 0.86, 0], [R, 0.18], [R, 0.42], [R * 0.86, 0.6]];
      p.forEach(([rad, f], k) => { const ang = a + step * f; const x = Math.cos(ang) * rad, y = Math.sin(ang) * rad; if (i === 0 && k === 0) sh.moveTo(x, y); else sh.lineTo(x, y); });
    }
    sh.closePath();
    const hole = new THREE.Path(); hole.absarc(0, 0, r, 0, Math.PI * 2, true); sh.holes.push(hole);
    for (let i = 0; i < 6; i++) { const h = new THREE.Path(); const a = (i / 6) * Math.PI * 2; h.absarc(Math.cos(a) * (R + r) * 0.5 * 0.9, Math.sin(a) * (R + r) * 0.5 * 0.9, (R - r) * 0.16, 0, Math.PI * 2, true); sh.holes.push(h); }
    const g = new THREE.ExtrudeGeometry(sh, { depth: thick, bevelEnabled: true, bevelThickness: thick * 0.12, bevelSize: thick * 0.1, bevelSegments: 2, curveSegments: S(10) });
    g.translate(0, 0, -thick / 2);
    return g;
  }

  function lines(points, o) { const g = new THREE.BufferGeometry().setFromPoints(points); const l = new THREE.LineSegments(g, lineMat(o)); l.userData.base = o; pulseLines.push(l); return l; }

  function chip(w, h, d, pins) {
    const gp = new THREE.Group();
    gp.add(mesh(new THREE.BoxGeometry(w, h, d), graphite));
    gp.add(mesh(new THREE.BoxGeometry(w * 0.55, h * 0.3, d * 0.55), glow, 0, h * 0.5, 0));
    if (pins) {
      const pg = new THREE.BoxGeometry(w * 0.06, h * 0.4, d * 0.18);
      for (let i = 0; i < pins; i++) {
        const t = (i + 0.5) / pins - 0.5;
        [[-0.5, t], [0.5, t]].forEach(([sx, tz]) => gp.add(mesh(pg, titanium, sx * (w + w * 0.06), 0, tz * d * 0.9)));
        [[t, -0.5], [t, 0.5]].forEach(([tx, sz]) => { const p = mesh(new THREE.BoxGeometry(d * 0.18, h * 0.4, w * 0.06), titanium, tx * w * 0.9, 0, sz * (d + w * 0.06)); gp.add(p); });
      }
    }
    return gp;
  }

  /* THE INTELLIGENCE CORE */
  function buildProcessor() {
    const g = new THREE.Group(); const s = new THREE.Group(); g.add(s);
    s.add(mesh(new THREE.BoxGeometry(2.1, 0.12, 2.1), darkMetal));
    s.add(mesh(new THREE.BoxGeometry(1.9, 0.1, 1.9), graphite, 0, 0.11, 0));
    [[1.6, 0.17], [1.25, 0.28], [0.9, 0.39]].forEach(([w, y], i) => s.add(mesh(new THREE.BoxGeometry(w, 0.08, w), i === 2 ? frosted : glass, 0, y, 0)));
    s.add(mesh(new THREE.BoxGeometry(0.52, 0.1, 0.52), glow, 0, 0.47, 0));
    const lid = mesh(new THREE.BoxGeometry(0.7, 0.04, 0.7), titanium, 0, 0.55, 0); s.add(lid);
    for (let i = 0; i < 32; i++) { const a = Math.floor(i / 8) * Math.PI / 2; const o = ((i % 8) - 3.5) * 0.2; const trace = mesh(new THREE.BoxGeometry(0.62, 0.012, 0.014), glowSoft, 0, 0.17 + (i % 3) * 0.11 + 0.045, 0); trace.position.set(Math.cos(a) * 0.62 + (Math.abs(Math.cos(a)) > 0.5 ? 0 : o), trace.position.y, Math.sin(a) * 0.62 + (Math.abs(Math.cos(a)) > 0.5 ? o : 0)); trace.rotation.y = a; s.add(trace); }
    const pin = new THREE.BoxGeometry(0.06, 0.1, 0.18);
    for (let i = 0; i < 16; i++) { const o = (i - 7.5) * 0.115; [[1.14, o, 0], [-1.14, o, 0]].forEach(([x, z]) => s.add(mesh(pin, titanium, x, -0.02, z))); [[o, 1.14], [o, -1.14]].forEach(([x, z]) => { const p = mesh(new THREE.BoxGeometry(0.18, 0.1, 0.06), titanium, x, -0.02, z); s.add(p); }); }
    s.rotation.set(0.5, 0.4, 0); g.userData.spin = s; return g;
  }

  /* Scene 2: neural network sculpture of glass spheres with illuminated pathways */
  function buildNeural() {
    const g = new THREE.Group(); const s = new THREE.Group(); g.add(s);
    const layers = [4, 6, 6, 3]; const L = []; const pts = [];
    layers.forEach((n, li) => { const col = []; for (let i = 0; i < n; i++) { const v = new THREE.Vector3((li - 1.5) * 0.85, (i - (n - 1) / 2) * 0.46, Math.sin(i * 1.7 + li) * 0.28); col.push(v); const r = 0.13 + ((i + li) % 3) * 0.03; s.add(mesh(new THREE.SphereGeometry(r, S(20), S(14)), glass, v.x, v.y, v.z)); s.add(mesh(new THREE.SphereGeometry(r * 0.42, 14, 10), glow, v.x, v.y, v.z)); } L.push(col); });
    for (let li = 0; li < L.length - 1; li++) L[li].forEach((a) => L[li + 1].forEach((b) => pts.push(a, b)));
    s.add(lines(pts, 0.28));
    const base = mesh(new THREE.CylinderGeometry(1.7, 1.8, 0.06, S(48)), graphite, 0, -1.7, 0); s.add(base); s.add(mesh(new THREE.TorusGeometry(1.7, 0.012, 6, S(80)).rotateX(Math.PI / 2), glow, 0, -1.67, 0));
    s.rotation.set(0.15, -0.5, 0); g.userData.spin = s; return g;
  }

  /* Scene 3: robotic assembly: base, jointed arm, gripper, sensors */
  function buildRobot() {
    const g = new THREE.Group(); const s = new THREE.Group(); g.add(s);
    s.add(mesh(new THREE.CylinderGeometry(1.0, 1.1, 0.14, S(48)), graphite, 0, -0.9, 0));
    s.add(mesh(new THREE.TorusGeometry(0.98, 0.014, 6, S(64)).rotateX(Math.PI / 2), glow, 0, -0.82, 0));
    const col = mesh(new THREE.CylinderGeometry(0.28, 0.34, 0.5, S(32)), titanium, 0, -0.55, 0); s.add(col);
    const shoulder = new THREE.Group(); shoulder.position.set(0, -0.28, 0); s.add(shoulder);
    shoulder.add(mesh(new THREE.SphereGeometry(0.26, S(24), S(16)), darkMetal));
    const upper = new THREE.Group(); shoulder.add(upper);
    upper.add(mesh(new THREE.BoxGeometry(0.2, 1.05, 0.24), titanium, 0, 0.55, 0)); upper.add(mesh(new THREE.BoxGeometry(0.06, 0.8, 0.26), glowSoft, 0.1, 0.55, 0));
    const elbow = new THREE.Group(); elbow.position.set(0, 1.08, 0); upper.add(elbow);
    elbow.add(mesh(new THREE.SphereGeometry(0.2, S(20), S(14)), darkMetal)); elbow.add(mesh(new THREE.CylinderGeometry(0.07, 0.07, 0.5, 14).rotateX(Math.PI / 2), glow));
    const fore = new THREE.Group(); elbow.add(fore); fore.add(mesh(new THREE.BoxGeometry(0.16, 0.85, 0.2), titanium, 0, 0.42, 0));
    const wrist = new THREE.Group(); wrist.position.set(0, 0.88, 0); fore.add(wrist); wrist.add(mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.16, 16), darkMetal));
    const f1 = mesh(new THREE.BoxGeometry(0.05, 0.3, 0.1), titanium, -0.1, 0.22, 0), f2 = mesh(new THREE.BoxGeometry(0.05, 0.3, 0.1), titanium, 0.1, 0.22, 0); wrist.add(f1, f2);
    wrist.add(mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.08, 10), glow, 0, 0.1, 0.08));
    [[-0.6, 0.35], [0.55, 0.6]].forEach(([x, z]) => { s.add(mesh(new THREE.BoxGeometry(0.34, 0.16, 0.34), graphite, x, -0.75, z)); s.add(mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.12, 12), glow, x, -0.64, z)); });
    g.userData = { spin: s, joints: { shoulder, elbow, wrist, f1, f2 } }; s.rotation.y = -0.6; s.scale.setScalar(0.95); return g;
  }

  /* Scene 4: learning system: mathematical solids, knowledge nodes, circuit grid */
  function buildLearning() {
    const g = new THREE.Group(); const s = new THREE.Group(); g.add(s);
    const edge = (geo, o) => { const l = new THREE.LineSegments(new THREE.EdgesGeometry(geo), lineMat(o)); pulseLines.push(l); l.userData.base = o; return l; };
    s.add(edge(new THREE.IcosahedronGeometry(1.15, 0), 0.9)); s.add(mesh(new THREE.IcosahedronGeometry(1.14, 0), glass));
    const oct = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.OctahedronGeometry(0.72, 0)), new THREE.LineBasicMaterial({ color: 0xc9d3d8 })); s.add(oct);
    const dod = mesh(new THREE.DodecahedronGeometry(0.34, 0), titanium); s.add(dod);
    s.add(mesh(new THREE.SphereGeometry(0.1, 14, 10), glow));
    const orbit = []; for (let i = 0; i < 5; i++) { const o = new THREE.Group(); o.rotation.set(i * 0.7, i * 1.1, 0); const r = mesh(new THREE.TorusGeometry(1.45 + i * 0.06, 0.006, 6, S(80)), glowSoft); o.add(r); const n = mesh(new THREE.SphereGeometry(0.06, 12, 8), glow, 1.45 + i * 0.06, 0, 0); o.add(n); orbit.push(o); s.add(o); }
    const grid = new THREE.Group(); grid.position.y = -1.7; for (let i = -4; i <= 4; i++) { grid.add(mesh(new THREE.BoxGeometry(3.6, 0.008, 0.01), glowSoft, 0, 0, i * 0.4)); grid.add(mesh(new THREE.BoxGeometry(0.01, 0.008, 3.6), glowSoft, i * 0.4, 0, 0)); } s.add(grid);
    g.userData = { spin: s, orbit, oct, dod }; return g;
  }

  const objs = [buildProcessor(), buildLearning(), buildRobot(), buildNeural()];
  const sceneRoot = new THREE.Group(); scene.add(sceneRoot); objs.forEach((o) => { o.scale.setScalar(0); sceneRoot.add(o); });

  /* ---- corner companion: one generated model per theme, swapped as the sections change ---- */
  const MODEL_FILES = { cap: "cap.glb", chip: "chip.glb", arm: "arm.glb", trophy: "trophy.glb" };
  const THEME = { about: "cap", expertise: "chip", skills: "chip", projects: "arm", videos: "arm", awards: "trophy", gallery: "trophy", contact: "cap" };
  const modelBase = new URL("../models/", import.meta.url);
  const comp = new THREE.Group(); scene.add(comp);
  const models = {};
  const gltf = new GLTFLoader();
  Object.keys(MODEL_FILES).forEach((k) => {
    gltf.load(new URL(MODEL_FILES[k], modelBase).href, (g) => {
      const o = g.scene, box = new THREE.Box3().setFromObject(o), size = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
      o.position.sub(c);
      const inner = new THREE.Group(); inner.add(o); inner.scale.setScalar(1 / (Math.max(size.x, size.y, size.z) || 1));
      const wrap = new THREE.Group(); wrap.add(inner); wrap.scale.setScalar(0); wrap.visible = false; comp.add(wrap);
      models[k] = { wrap, s: 0 };
    }, undefined, () => {});
  });

  /* ---- layout helpers: world size of the viewport at z = 0 ---- */
  const half = () => { const h = Math.tan((camera.fov * Math.PI) / 360) * camera.position.z; return { h, w: h * camera.aspect }; };
  const sec = (id) => document.getElementById(id);
  const ids = ["about", "expertise", "skills", "projects", "videos", "awards", "gallery", "contact"];
  const sideOf = Object.fromEntries(ids.map((k, i) => [k, i % 2 === 0 ? 1 : -1]));

  const smoothTo = (a, b, k) => a + (b - a) * k;
  let lastTheme = "", spinBoost = 0, time = 0;

  /* which section is at the viewport midline -> which model the companion shows */
  function themeNow() {
    const mid = window.innerHeight * 0.5;
    for (const i of ids) { const e = sec(i); if (!e) continue; const r = e.getBoundingClientRect(); if (r.top <= mid && r.bottom > mid) return THEME[i]; }
    return lastTheme || "cap";
  }

  const clock = new THREE.Clock(); let frames = 0, slow = 0, active = true;
  document.addEventListener("visibilitychange", () => { active = !document.hidden; if (active) { clock.getDelta(); loop(); } });
  addEventListener("resize", setSize); setSize();

  function loop() {
    if (!active) return;
    requestAnimationFrame(loop);
    const dt = Math.min(0.05, clock.getDelta()); time += reduced ? 0 : dt;
    const st = window.cineState || { p: 0, sceneWeight: () => 0, sceneCount: 4 };
    const H = half(), narrow = camera.aspect < 1.2;

    /* hero scene objects: placed opposite each statement so they never cover the text or Peter */
    const p = st.p, inHero = p < 0.97;
    objs.forEach((o, i) => {
      const w = st.sceneWeight ? st.sceneWeight(i, p) : 0; o.visible = w > 0.004; if (!o.visible) return;
      const side = i % 2 === 0 ? 1 : -1; // statements 0,2 sit left → object right
      const tx = narrow ? H.w * 0.52 : side * H.w * 0.58, ty = narrow ? H.h * 0.6 : 0.05 * H.h;
      o.position.set(tx + (1 - w) * side * 0.8, ty + Math.sin(time * 0.8 + i) * 0.06, 0);
      const sc = (narrow ? Math.min(0.62, H.w * 0.3) : Math.min(1.05, H.w * 0.27)) * (0.35 + 0.65 * w); o.scale.setScalar(sc);
      const spin = o.userData.spin; if (spin) spin.rotation.y += (reduced ? 0 : dt * 0.35) + (st.target !== undefined ? (st.target - st.p) * 0.08 : 0);
      o.traverse(() => {});
      if (i === 0) { spin.rotation.x = 0.55 + Math.sin(time * 0.5) * 0.08; }
      if (i === 2) { const j = o.userData.joints; j.shoulder.rotation.z = 0.35 + Math.sin(time * 0.9) * 0.35; j.elbow.rotation.z = -0.9 + Math.sin(time * 1.3 + 1) * 0.4; j.wrist.rotation.z = Math.sin(time * 1.7) * 0.4; const o2 = 0.1 + (Math.sin(time * 2) * 0.5 + 0.5) * 0.04; j.f1.position.x = -o2; j.f2.position.x = o2; }
      if (i === 1) { o.userData.orbit.forEach((g, k) => { g.rotation.z += dt * (0.25 + k * 0.08); }); o.userData.oct.rotation.y -= dt * 0.5; o.userData.dod.rotation.x += dt * 0.6; }
    });

    /* corner companion: small, bottom-right, swaps model with the section theme */
    const want = inHero ? "" : themeNow();
    if (want && want !== lastTheme) { lastTheme = want; spinBoost = 1; }
    const k = 1 - Math.exp(-dt / 0.35); spinBoost = Math.max(0, spinBoost - dt * 1.2);
    /* sized and placed in screen pixels: a small badge hugging the bottom-right corner on every device */
    const unit = (2 * H.h) / window.innerHeight, vw = window.innerWidth, vh = window.innerHeight;
    const dia = Math.max(52, Math.min(vw < 700 ? 76 : 120, Math.min(vw, vh) * 0.15)), edge = 10 + dia / 2;
    const size = dia * unit;
    comp.position.set(H.w - edge * unit, -H.h + edge * unit, 0);
    Object.keys(models).forEach((name) => {
      const m = models[name]; m.s = smoothTo(m.s, want === name ? 1 : 0, k);
      m.wrap.visible = m.s > 0.02;
      if (!m.wrap.visible) return;
      m.wrap.scale.setScalar(size * m.s);
      m.wrap.rotation.y += (reduced ? 0 : dt * (0.5 + spinBoost * 5)) * (want === name ? 1 : -1);
      m.wrap.rotation.x = 0.18 + Math.sin(time * 0.6) * 0.06;
      m.wrap.position.y = Math.sin(time * 1.1) * size * 0.04;
    });
    renderer.render(scene, camera);
    canvas.classList.add("is-ready");

    /* adaptive quality: step the pixel ratio down if frames run long */
    frames++; if (dt > 0.034) slow++; if (frames === 90) { if (slow > 30 && dprCap > 1) { dprCap = 1; setSize(); } frames = 0; slow = 0; }
  }
  loop();
}

if (canvas) {
  if (!window.WebGLRenderingContext) root.classList.add("no-webgl");
  else boot();
}
