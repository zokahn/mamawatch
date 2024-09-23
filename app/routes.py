from flask import render_template
from app import app
from app.mqtt_client import MQTTClient

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnostics')
def diagnostics():
    mqtt_status = MQTTClient.get_status()
    button_status = MQTTClient.get_button_status()
    return render_template('diagnostics.html', mqtt_status=mqtt_status, button_status=button_status)
