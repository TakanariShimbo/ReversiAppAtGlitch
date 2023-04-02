

// Update Message
function updateMessage(message) {
    const messageElement = document.getElementById('turn-message');
    messageElement.textContent = message;
}

function updateMessageByTurn(turn) {           
    let message;
    if (turn == your_color) {
        message = "YOUR(" + turn + ") TURN";
    } else {
        message = "ENEMY(" + turn + ") TURN";
    }

    updateMessage(message);
}

// Get Fov
function getFovByAspect(aspect) {
    const minAspect = 0.1; // 最小横幅
    const maxAspect = 1;   // 最大横幅
    const minFov = 125;    // 最大視野角
    const maxFov = 75;     // 最小視野角

    const fov = ((aspect - minAspect) / (maxAspect - minAspect)) * (maxFov - minFov) + minFov;
    return Math.max(maxFov, Math.min(minFov, fov));
}