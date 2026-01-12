import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

// Cena
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x555555);

// Câmara
const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);
camera.position.set(6, 6, 8);

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Controles
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Luz
scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const dir = new THREE.DirectionalLight(0xffffff, 1);
dir.position.set(5, 10, 7);
scene.add(dir);

// Grid cartesiano
scene.add(new THREE.GridHelper(10, 10));

// LEDs (esferas)
const geo = new THREE.SphereGeometry(0.5, 32, 32);

const leds = {
  1: new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0x00ff00 })),
  2: new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0xffff00 })),
  3: new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0xffff00 })),
  4: new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0xff0000 })),
};

let x = -3;
Object.values(leds).forEach(led => {
  led.position.set(x, 0, 0);
  scene.add(led);
  x += 2;
});

// API para Python / WebSocket depois
window.setLed = (id, state) => {
  const colors = {
    1: 0x00ff00,
    2: 0xffff00,
    3: 0xffff00,
    4: 0xff0000,
  };
  leds[id].material.color.set(state ? colors[id] : 0xffffff);
};

// Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();
