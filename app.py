import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_socketio import SocketIO, emit, join_room, leave_room
from dotenv import load_dotenv

from manager import ReversiRoom, RoomUserManager


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app)


room_user_manager = RoomUserManager()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    # Get
    if request.method == 'GET':
        return render_template('create.html', rooms=room_user_manager.room_name_list)

    # Post
    # Early return
    room_name = request.form['room_name']
    if room_user_manager.is_exists_room(room_name):
        return "この部屋名は既に使用されています。", 400
    
    room = room_user_manager.create_reversi_room(room_name)
    if type(room) == ReversiRoom:
        return redirect(url_for('riversi', room_name=room_name))     
    
@app.route('/enter', methods=['GET', 'POST'])
def enter():
    # Get
    if request.method == 'GET':
        return render_template('enter.html', rooms=room_user_manager.room_name_list)
    
    # Post
    # Early return
    room_name = request.form['room_name']
    if not room_user_manager.is_exists_room(room_name):
        return "この部屋は存在しません。", 400
    
    # Early return
    room = room_user_manager.get_room(room_name)
    if room.is_full():
        abort(403, "This room is full. Please try again later.")

    if type(room) == ReversiRoom:
        return redirect(url_for('riversi', room_name=room_name))    
    
@app.route('/riversi/<room_name>')
def riversi(room_name):
    reversi_room = room_user_manager.get_room(room_name)

    # Render toom.html    
    player_color = reversi_room.get_empty_player_color()
    return render_template('riversi.html', room_name=room_name, this_player_color=player_color.name, board=reversi_room.controller.current_board_str, enumerate=enumerate)


@socketio.on('disconnect')
def on_disconnect():
    session_id = request.sid

    # Leave room
    user = room_user_manager.get_user(session_id)
    room_user_manager.remove_user(session_id)
    leave_room(user.room_name)
    
    # Delete room
    room = room_user_manager.get_room(user.room_name)
    if room.is_empty():
        room_user_manager.remove_room(room.room_name)
    
    # Emit leave room event
    if type(room) == ReversiRoom:
        emit('reversi_left_room', {'player_color': user.player_color.name}, room=user.room_name)

@socketio.on('reversi_join_room')
def on_reversi_join_room(message):
    session_id = request.sid
    room_name = message["room_name"]
    player_color = message["player_color"]

    # Join room
    room_user_manager.create_reversi_user_and_assign_to_room(session_id, room_name, player_color)
    join_room(room_name)

    # Game start
    room = room_user_manager.get_room(room_name)
    if room.is_full():
        emit('reversi_game_start', {'next_player_color': room.controller.current_player_color_str}, room=room_name)

@socketio.on('reversi_put_stone')
def on_reversi_put_stone(message):
    session_id = request.sid

    # Early return
    user = room_user_manager.get_user(session_id)
    room = room_user_manager.get_room(user.room_name)
    if not room.is_full():
        return
    if user.player_color != room.controller.current_player_color:
        return
    
    # Update board
    x = int(message['x'])
    y = int(message['y'])
    if room.controller.can_put(x, y):
        room.controller.put(x, y)
        emit('reversi_update_board', {
            'next_board': room.controller.current_board_str, 
            'current_board': room.controller.previous_board_str, 
            'xy_put': room.controller.previous_xy_put, 
            'xy_flips': room.controller.previous_xy_flips,
            'xy_candidates': room.controller.previous_xy_candidates,
            'next_player_color': room.controller.current_player_color_str,
            'black_stone_count': room.controller.black_stone_count,
            'white_stone_count': room.controller.white_stone_count,
            'next_state' : room.controller.current_state_str
        }, room=room.room_name)


if __name__ == '__main__':
    socketio.run(app)
