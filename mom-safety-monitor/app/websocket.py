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
import logging

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
        emit('device_status', {
            'battery': mqtt_client._battery_status,
            'charger': mqtt_client._charger_status,
            'wifi': mqtt_client._wifi_status,
            'last_seen': mqtt_client._last_seen
        })

def send_mqtt_status(status):
    socketio.emit('mqtt_status', {'status': status})

def send_device_status(status):
    socketio.emit('device_status', status)
    logging.info(f"Sent device status: {status}")
