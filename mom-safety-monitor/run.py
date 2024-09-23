import os
import sys
import logging

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, socketio
from app.mqtt_client import MQTTClient
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    mqtt_client = MQTTClient(config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_TOPIC)
    
    try:
        mqtt_client.start()
        logging.info("MQTT client started successfully")
        
        logging.info("Starting Flask-SocketIO server")
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        try:
            mqtt_client.stop()
            logging.info("MQTT client stopped")
        except Exception as e:
            logging.error(f"Error stopping MQTT client: {str(e)}")
