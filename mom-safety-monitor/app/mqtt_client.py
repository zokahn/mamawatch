import paho.mqtt.client as mqtt
from app.websocket import send_button_status

class MQTTClient:
    def __init__(self, broker, port, topic):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Received message: {payload}")
        if payload == "pressed":
            send_button_status("pressed")
        else:
            send_button_status("not_pressed")

    def start(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
