from flask import Blueprint, render_template
from app.mqtt_client import MQTTClient

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

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

def init_mqtt_client(broker, port, topic, username, password):
    mqtt_client = MQTTClient(broker, port, topic, username, password)
    mqtt_client.start()
