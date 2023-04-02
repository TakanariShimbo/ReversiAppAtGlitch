

// Define socket
var socket = io();

// Emmit Connect Event and Disconnect Event
socket.on('connect', function() {
    socket.emit('join_room', {room_name: room_name, player_color: your_color});
});

socket.on('game_start', function (data) {
    const turn = data.turn;
    updateMessageByTurn(turn);
});

socket.on('left_room', function (data) {
    const leftPlayerColor = data.player_color;
    const message = "Player " + leftPlayerColor + " has left the room.";
    updateMessage(message);
});

socket.on('disconnect', function() {
    const message = "Disconnected from server. Please refresh the page.";
    updateMessage(message);
});



// Update turn message
function gameFinishEvent(black_stone_count, white_stone_count) {
    updateMessage("COUNTING");

    // Prepare Empty state
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            updateStoneMesh(i, j, null);
        }
    }
    
    // Put Black Stones
    for (let i = 0; i < black_stone_count; i++) {
        setTimeout(function() {
            const x = Math.floor(i / 8);
            const y = i % 8;
            updateStoneMesh(x, y, "BLACK");
        }, 150*(i+1));
    }

    // Put White Stones
    for (let i = 0; i < white_stone_count; i++) {
        setTimeout(function() {
            const x = Math.floor(i / 8);
            const y = i % 8;
            updateStoneMesh(7-x, 7-y, "WHITE");
        }, 150*(i+1));
    }

    // Update Message
    let result_message;
    let wait_count;
    if (black_stone_count > white_stone_count) {
        wait_count = black_stone_count;
        if ("BLACK" == your_color) {
            result_message = "YOU(BLACK) WIN";
        } else {
            result_message = "ENEMY(BLACK) WIN";
        }
    } else if (black_stone_count < white_stone_count) {
        wait_count = white_stone_count;
        if ("WHITE" == your_color) {
            result_message = "YOU(WHITE) WIN";
        } else {
            result_message = "ENEMY(WHITE) WIN";
        }            
    } else {
        result_message = "DRAW";
        wait_count = black_stone_count;
    }
    setTimeout(function(){
        updateMessage(result_message);
    }, 150*wait_count);
}


socket.on('update_board', function (data) {
    const current_board = data.current_board;
    const previous_board = data.previous_board;
    const xy_put = data.xy_put;
    const xy_flips = data.xy_flips;
    const xy_candidates = data.xy_candidates;
    const black_stone_count = data.black_stone_count;
    const white_stone_count = data.white_stone_count;

    // Prepare Previous state
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            updateStoneMeshByBoard(i, j, previous_board);
        }
    }
    
    // Put Stone
    updateStoneMeshByBoard(xy_put[0], xy_put[1], current_board);
    
    // Flip stones
    for (let i = 0; i < xy_flips.length; i++) {
        let xy_flip = xy_flips[i];
        setTimeout(function() {
            updateStoneMeshByBoard(xy_flip[0], xy_flip[1], current_board);
        }, 150*(i+1));
    }
    
    // Put Candidate stones
    setTimeout(function() {
        for (let i = 0; i < xy_candidates.length; i++) {
            let xy_candidate = xy_candidates[i];
            updateStoneMeshByBoard(xy_candidate[0], xy_candidate[1], current_board);
        }

        if (data.turn == "EMPTY") {
            gameFinishEvent(black_stone_count, white_stone_count);
        } else {
            updateMessageByTurn(data.turn);
        }
    }, 150*xy_flips.length);
});
