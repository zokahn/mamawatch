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
from datetime import datetime

def send_button_status(status, action):
    from app.database import add_message
    message_id = add_message(status, action)
    socketio.emit('button_status', {
        'id': message_id,
        'status': status,
        'action': action,
        'button_name': 'Mom\'s Button',
        'timestamp': datetime.now().isoformat()
    })
    logging.info(f"Sent button status: {status}, action: {action}")
    
    if status == "normal":
        socketio.emit('emergency_reset', {
            'message': 'Emergency has been reset'
        })
        logging.info("Emergency reset signal sent")

def send_led_status(status):
    socketio.emit('led_status', {'status': status})
    logging.info(f"Sent LED status: {status}")

@socketio.on('connect')
def handle_connect(auth):
    from app.mqtt_client import MQTTClient
    mqtt_client = MQTTClient._instance
    if mqtt_client:
        emit('mqtt_status', {'status': mqtt_client._mqtt_status})
        emit('button_status', {
            'status': mqtt_client._button_status,
            'action': mqtt_client._last_action if hasattr(mqtt_client, '_last_action') else None,
            'button_name': 'Mom\'s Button',
            'timestamp': datetime.now().isoformat()
        })
        emit('device_status', {
            'battery': mqtt_client._battery_status,
            'charger': mqtt_client._charger_status,
            'wifi': mqtt_client._wifi_status,
            'last_seen': mqtt_client._last_seen
        })

@socketio.on('acknowledge_event')
def handle_acknowledge(data):
    note = data.get('note', '')
    logging.info(f"Event acknowledged with note: {note}")
    # Here you would typically update a database or perform some action

def send_mqtt_status(status):
    socketio.emit('mqtt_status', {'status': status})

def send_device_status(status):
    socketio.emit('device_status', status)
    logging.info(f"Sent device status: {status}")
