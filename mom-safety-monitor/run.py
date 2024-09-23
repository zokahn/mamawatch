import os
import sys
import logging
from dotenv import load_dotenv
from flask import Flask

# Load environment variables
load_dotenv()

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import socketio
from app.mqtt_client import MQTTClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, template_folder='templates')

# Import routes after creating the app
from app import routes

# Register the Blueprint
app.register_blueprint(routes.bp)

def main():
    mqtt_client = MQTTClient(
        os.getenv('MQTT_BROKER', 'mqtt.zokahn.com'),
        int(os.getenv('MQTT_PORT', '1883')),
        os.getenv('MQTT_TOPIC', 'shellies/shellybutton1-485519F00C7B'),
        os.getenv('MQTT_USERNAME', 'bvandenh'),
        os.getenv('MQTT_PASSWORD', 'SJBC9]-+78bs')
    )
    
    try:
        mqtt_client.start()
        logger.info("MQTT client started successfully")
        
        logger.info("Starting Flask-SocketIO server")
        socketio.run(app, debug=os.getenv('DEBUG', 'False').lower() == 'true', host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        try:
            mqtt_client.stop()
            logger.info("MQTT client stopped")
        except Exception as e:
            logger.error(f"Error stopping MQTT client: {str(e)}")

if __name__ == '__main__':
    main()
