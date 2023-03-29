import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_socketio import SocketIO, emit, join_room, leave_room
from dotenv import load_dotenv

from stone import ReversiStone
from manager import RoomUserManager


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
    if not room_user_manager.can_create_room(room_name):
        return "この部屋名は既に使用されています。", 400
    
    room_user_manager.create_room(room_name)
    return redirect(url_for('room', room_name=room_name))    
    
@app.route('/enter', methods=['GET', 'POST'])
def enter():
    # Get
    if request.method == 'GET':
        return render_template('enter.html', rooms=room_user_manager.room_name_list)
    
    # Post
    # Early return
    room_name = request.form['room_name']
    if not room_user_manager.can_enter_room(room_name):
        return "この部屋は存在しません。", 400
    
    return redirect(url_for('room', room_name=room_name))    
    
@app.route('/room/<room_name>')
def room(room_name):
    # Early return
    room = room_user_manager.get_room(room_name)
    if room.is_full():
        abort(403, "This room is full. Please try again later.")

    # Render toom.html    
    if room.is_empty():
        player_color = ReversiStone.BLACK
    else:
        stone_kind = room.get_empty_stone_kind()
        player_color = stone_kind
    return render_template('room.html', room_name=room_name, your_color=player_color.name, board=room.controller.board_str, enumerate=enumerate)


@socketio.on('join_room')
def on_join_room(message):
    session_id = request.sid
    room_name = message["room_name"]
    player_color = getattr(ReversiStone, message["player_color"])

    # Join room
    room_user_manager.create_user_and_assign_to_room(session_id, room_name, player_color)
    join_room(room_name)

    # Game start
    room = room_user_manager.get_room(room_name)
    if room.is_full():
        emit('game_start', {'turn': room.controller.turn_str}, room=room_name)

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

@socketio.on('put')
def put(message):
    session_id = request.sid

    # Early return
    user = room_user_manager.get_user(session_id)
    room = room_user_manager.get_room(user.room_name)
    if not room.is_full():
        return
    if user.stone_kind != room.controller.turn:
        return
    
    # Update board
    x = int(message['x'])
    y = int(message['y'])
    if room.controller.put(x, y):
        emit('update_board', {'board': room.controller.board_str, 'turn': room.controller.turn_str}, room=room.room_name)


if __name__ == '__main__':
    socketio.run(app)