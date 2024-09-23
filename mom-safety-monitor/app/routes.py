from flask import Blueprint, render_template, jsonify
from app import socketio
from app.mqtt_client import MQTTClient

bp = Blueprint('main', __name__)
mqtt_client = None

@bp.route('/')
def index():
    return render_template('index.html')

@socketio.on('led_control')
def handle_led_control(message):
    global mqtt_client
    if mqtt_client:
        mqtt_client.publish_led_state(message)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'MQTT client not initialized'})

def init_mqtt_client(broker, port, topic, button_pin, led_pin):
    global mqtt_client
    mqtt_client = MQTTClient(broker, port, topic, button_pin, led_pin)
    mqtt_client.start()
