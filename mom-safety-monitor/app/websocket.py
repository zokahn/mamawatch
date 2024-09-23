from flask_socketio import emit
from app import socketio
import logging

@socketio.on('connect')
def handle_connect():
    logging.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    logging.info('Client disconnected')

def send_button_status(status):
    socketio.emit('button_status', {'status': status})
    logging.info(f"Sent button status: {status}")

def send_led_status(status):
    socketio.emit('led_status', {'status': status})
    logging.info(f"Sent LED status: {status}")
