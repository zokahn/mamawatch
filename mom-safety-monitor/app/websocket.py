from flask_socketio import emit
from app import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def send_button_status(status):
    socketio.emit('button_status', {'status': status})
