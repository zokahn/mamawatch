from flask_socketio import emit
from app import socketio
import logging

@socketio.on('connect')
def handle_connect():
    logging.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    logging.info('Client disconnected')

from flask_socketio import emit
from app import socketio

def send_button_status(status):
    socketio.emit('button_status', {'status': status})
    logging.info(f"Sent button status: {status}")

def send_led_status(status):
    socketio.emit('led_status', {'status': status})
    logging.info(f"Sent LED status: {status}")
@socketio.on('connect')
def handle_connect():
    from app.mqtt_client import MQTTClient
    mqtt_client = MQTTClient._instance
    if mqtt_client:
        emit('mqtt_status', {'status': mqtt_client._mqtt_status})
        emit('button_status', {'status': mqtt_client._button_status})

def send_mqtt_status(status):
    socketio.emit('mqtt_status', {'status': status})
