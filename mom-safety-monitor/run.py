from app import app, socketio
from app.mqtt_client import MQTTClient
import config

if __name__ == '__main__':
    mqtt_client = MQTTClient(config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_TOPIC)
    mqtt_client.start()
    
    try:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    finally:
        mqtt_client.stop()
