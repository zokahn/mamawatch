import paho.mqtt.client as mqtt
from app.websocket import send_button_status
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MQTTClient:
    def __init__(self, broker, port, topic):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected to MQTT broker successfully")
            client.subscribe(self.topic)
        else:
            logging.error(f"Failed to connect to MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        logging.info(f"Received message: {payload}")
        if payload == "pressed":
            send_button_status("pressed")
            logging.info("Button pressed, sent 'pressed' status")
        else:
            send_button_status("not_pressed")
            logging.info("Button not pressed, sent 'not_pressed' status")

    def start(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            logging.info(f"MQTT client started and connected to {self.broker}:{self.port}")
        except Exception as e:
            logging.error(f"Failed to start MQTT client: {str(e)}")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        logging.info("MQTT client stopped and disconnected")
