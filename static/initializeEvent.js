

// Prepare Static instance
const scene = generateScene();
const camera = generateCamera();
const renderer = generateRenderer();

const boardMesh = generateBoard();
scene.add(boardMesh);

const gridLines = generateGridLines();
scene.add(gridLines);

const ambientLight = generateAmbientLight();
scene.add(ambientLight);

const pointLight = generatePointLight();
scene.add(pointLight);

const stoneMeshs = [];
for (let i = 0; i < 8; i++) {
    stoneMeshs[i] = [];
    for (let j = 0; j < 8; j++) {
        stoneMeshs[i][j] = null;
    }
}

// threeFunction
function updateStoneMesh(x, y, stoneKind) {
    // Remove current stoneMaterial
    if (stoneMeshs[x][y] != null){
        scene.remove(stoneMeshs[x][y]);
    }

    // Add stoneMesh
    const stoneMesh = generateStone(x, y, stoneKind);
    scene.add(stoneMesh);
    stoneMeshs[x][y] = stoneMesh;
}

function updateStoneMeshByBoard(x, y, board){
    updateStoneMesh(x, y, board[x][y]);
}

// Initialize
for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
        updateStoneMesh(i, j, initial_board[i][j]);
    }
}

// Define and Run animation
const animate = function () {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
};

animate();

// Prepare Event Listener
function onMouseDownEvent(event) {
    onMouseDownAndTouchStartEvent(event.clientX, event.clientY, socket);
}
window.addEventListener('mousedown', onMouseDownEvent, false);

function onTouchStartEvent(event) {
    const touch = event.touches[0] || event.changedTouches[0];
    onMouseDownAndTouchStartEvent(touch.clientX, touch.clientY, socket);
}
window.addEventListener('touchstart', onTouchStartEvent, false);

window.addEventListener('resize', onResizeEvent(camera, renderer), false);