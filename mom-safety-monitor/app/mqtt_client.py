import paho.mqtt.client as mqtt
from app.websocket import send_button_status
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MQTTClient:
    _instance = None
    _button_status = "unknown"
    _mqtt_status = "disconnected"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MQTTClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, broker, port, topic, username, password):
        if not hasattr(self, 'client'):
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.broker = broker
            self.port = port
            self.topic = topic
            self.username = username
            self.password = password

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
            self._button_status = "pressed"
            send_button_status("pressed")
            logging.info("Button pressed, sent 'pressed' status")
        else:
            self._button_status = "not_pressed"
            send_button_status("not_pressed")
            logging.info("Button not pressed, sent 'not_pressed' status")

    def start(self):
        try:
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            self._mqtt_status = "connected"
            logging.info(f"MQTT client started and connected to {self.broker}:{self.port}")
        except Exception as e:
            self._mqtt_status = "error"
            logging.error(f"Failed to start MQTT client: {str(e)}")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        self._mqtt_status = "disconnected"
        logging.info("MQTT client stopped and disconnected")

    @classmethod
    def get_status(cls):
        return cls._mqtt_status

    @classmethod
    def get_button_status(cls):
        return cls._button_status
