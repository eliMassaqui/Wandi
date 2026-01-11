from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView


class SimulationView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.webview = QWebEngineView(self)
        layout.addWidget(self.webview)

        self._load_scene()

    def _load_scene(self):
        html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Wandi 3D</title>
<style>
html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #555555;  /* fundo cinza */
}
canvas {
    display: block;
}
</style>
</head>
<body>

<script src="https://unpkg.com/three@0.158.0/build/three.min.js"></script>

<script>
    // Cena
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x555555); // fundo cinza

    // Câmera
    const camera = new THREE.PerspectiveCamera(
        60,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(4, 4, 6);
    camera.lookAt(0, 0, 0);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x555555, 1);  // fundo cinza
    document.body.appendChild(renderer.domElement);

    // Luz
    scene.add(new THREE.AmbientLight(0x404040));
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5);
    scene.add(light);

    // Plano cartesiano (grid)
    const grid = new THREE.GridHelper(10, 10, 0x888888, 0xaaaaaa);
    scene.add(grid);

    // Eixos XYZ
    scene.add(new THREE.AxesHelper(5));

    // Cubo azul
    const cube = new THREE.Mesh(
        new THREE.BoxGeometry(1, 1, 1),
        new THREE.MeshStandardMaterial({ color: 0x0066ff })
    );
    scene.add(cube);

    // Velocidade aleatória
    const speed = {
        x: Math.random() * 0.02 + 0.005,
        y: Math.random() * 0.02 + 0.005,
        z: Math.random() * 0.02 + 0.005
    };

    function animate() {
        requestAnimationFrame(animate);

        cube.rotation.x += speed.x;
        cube.rotation.y += speed.y;
        cube.rotation.z += speed.z;

        renderer.render(scene, camera);
    }

    animate();

    window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
</script>

</body>
</html>
        """

        self.webview.setHtml(html)
