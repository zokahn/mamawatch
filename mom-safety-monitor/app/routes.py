from flask import Blueprint, render_template, jsonify, request
from app.mqtt_client import MQTTClient
from app.database import get_messages, acknowledge_message, get_archived_messages
from datetime import datetime
import pytz

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    messages = get_messages(limit=10, include_unacknowledged=True)
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    formatted_messages = []
    for message in messages:
        utc_time = datetime.fromisoformat(message[1])
        amsterdam_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(amsterdam_tz)
        formatted_time = amsterdam_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_messages.append([message[0], formatted_time] + list(message[2:]))
    return render_template('index.html', messages=formatted_messages)

@bp.route('/archived_logs')
def archived_logs():
    messages = get_archived_messages()
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    formatted_messages = []
    for message in messages:
        utc_time = datetime.fromisoformat(message[1])
        amsterdam_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(amsterdam_tz)
        formatted_time = amsterdam_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_messages.append([message[0], formatted_time] + list(message[2:]))
    return render_template('archived_logs.html', messages=formatted_messages)

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

@bp.route('/acknowledge_bulk_events', methods=['POST'])
def acknowledge_bulk_events():
    message_ids = request.json.get('message_ids', [])
    note = request.json.get('note', '')
    acknowledge_multiple_messages(message_ids, note)
    return jsonify({"status": "success", "message": "Events acknowledged"})

@bp.route('/get_latest_data')
def get_latest_data():
    mqtt_client = MQTTClient._instance
    messages = get_messages()[:5]  # Get the 5 most recent messages
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    formatted_messages = []
    for message in messages:
        utc_time = datetime.fromisoformat(message[1])
        amsterdam_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(amsterdam_tz)
        formatted_time = amsterdam_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_messages.append({
            "id": message[0],
            "timestamp": formatted_time,
            "status": message[2],
            "action": message[3],
            "acknowledged": bool(message[4]),
            "note": message[5]
        })
    
    return jsonify({
        "button_status": {
            "status": mqtt_client._button_status,
            "action": mqtt_client._last_action if hasattr(mqtt_client, '_last_action') else None
        },
        "device_status": {
            "battery": mqtt_client._battery_status,
            "charger": mqtt_client._charger_status,
            "wifi": mqtt_client._wifi_status,
            "last_seen": mqtt_client._last_seen
        },
        "events": formatted_messages
    })

def init_mqtt_client(broker, port, topic, username, password):
    mqtt_client = MQTTClient(broker, port, topic, username, password)
    mqtt_client.start()
