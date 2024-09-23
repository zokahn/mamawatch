from flask import Blueprint, render_template, jsonify, request
from app.mqtt_client import MQTTClient
from app.database import get_messages, acknowledge_message
from datetime import datetime
import pytz

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    messages = get_messages()
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    for message in messages:
        utc_time = datetime.fromisoformat(message[1])
        amsterdam_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(amsterdam_tz)
        message[1] = amsterdam_time.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', messages=messages)

@bp.route('/diagnostics')
def diagnostics():
    mqtt_client = MQTTClient._instance
    if mqtt_client:
        mqtt_status = mqtt_client._mqtt_status
        button_status = mqtt_client._button_status
        last_error = mqtt_client._last_error
        connection_details = mqtt_client._connection_details
    else:
        mqtt_status = "unknown"
        button_status = "unknown"
        last_error = "MQTT client not initialized"
        connection_details = {}
    return render_template('diagnostics.html', 
                           mqtt_status=mqtt_status, 
                           button_status=button_status, 
                           last_error=last_error, 
                           connection_details=connection_details)

@bp.route('/acknowledge_event', methods=['POST'])
def acknowledge_event():
    message_id = request.json.get('message_id')
    note = request.json.get('note', '')
    acknowledge_message(message_id, note)
    return jsonify({"status": "success", "message": "Event acknowledged"})

def init_mqtt_client(broker, port, topic, username, password):
    mqtt_client = MQTTClient(broker, port, topic, username, password)
    mqtt_client.start()
