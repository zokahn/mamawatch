from flask import Blueprint, render_template
from app.mqtt_client import MQTTClient

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/diagnostics')
def diagnostics():
    mqtt_status = MQTTClient.get_status()
    button_status = MQTTClient.get_button_status()
    last_error = MQTTClient.get_last_error()
    connection_details = MQTTClient.get_connection_details()
    return render_template('diagnostics.html', 
                           mqtt_status=mqtt_status, 
                           button_status=button_status, 
                           last_error=last_error, 
                           connection_details=connection_details)

def init_mqtt_client(broker, port, topic, username, password):
    mqtt_client = MQTTClient(broker, port, topic, username, password)
    mqtt_client.start()
