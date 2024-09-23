import paho.mqtt.client as mqtt
from app.websocket import send_button_status
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MQTTClient:
    _instance = None
    _button_status = "unknown"
    _mqtt_status = "disconnected"
    _last_error = None
    _connection_details = {}
    _battery_status = None
    _charger_status = None
    _wifi_status = None
    _last_seen = None

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
            self._connection_details = {
                "broker": broker,
                "port": port,
                "topic": topic,
                "username": username
            }

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected to MQTT broker successfully")
            client.subscribe(self.topic)
            self._mqtt_status = "connected"
        else:
            logging.error(f"Failed to connect to MQTT broker with result code {rc}")
            self._mqtt_status = "error"
        self._last_error = f"Connection result code: {rc}"

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        logging.info(f"Received message on topic {topic}: {payload}")

        if topic.endswith('/input_event/0'):
            self._process_button_event(payload)
        elif topic.endswith('/sensor'):
            self._process_sensor_data(payload)
        elif topic.endswith('/info'):
            self._process_info_data(payload)

    def _process_button_event(self, payload):
        event_data = json.loads(payload)
        if event_data.get('event') == 'S':
            self._button_status = "call_request"
            send_button_status("call_request")
            logging.info("Button pressed once, call request")
        elif event_data.get('event') == 'L':
            self._button_status = "emergency"
            send_button_status("emergency")
            logging.info("Button long press, emergency")
        elif event_data.get('event') == 'SS':
            self._button_status = "reset"
            send_button_status("reset")
            logging.info("Button pressed twice, reset action")
        else:
            self._button_status = "unknown"
            send_button_status("unknown")
            logging.info(f"Unknown button action: {payload}")

    def _process_sensor_data(self, payload):
        sensor_data = json.loads(payload)
        self._battery_status = sensor_data.get('battery')
        self._charger_status = sensor_data.get('charger')
        self._last_seen = datetime.now().isoformat()
        self._update_status()

    def _process_info_data(self, payload):
        info_data = json.loads(payload)
        wifi_sta = info_data.get('wifi_sta', {})
        self._wifi_status = {
            'connected': wifi_sta.get('connected'),
            'ssid': wifi_sta.get('ssid'),
            'ip': wifi_sta.get('ip'),
            'rssi': wifi_sta.get('rssi')
        }
        self._update_status()

    def _update_status(self):
        from app.websocket import send_device_status
        status = {
            'battery': self._battery_status,
            'charger': self._charger_status,
            'wifi': self._wifi_status,
            'last_seen': self._last_seen
        }
        send_device_status(status)

    def start(self):
        try:
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            self._mqtt_status = "connecting"
            self._last_error = None
            logging.info(f"MQTT client started and connecting to {self.broker}:{self.port}")
        except Exception as e:
            self._mqtt_status = "error"
            self._last_error = str(e)
            logging.error(f"Failed to start MQTT client: {str(e)}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._mqtt_status = "connected"
            logging.info("Connected to MQTT broker successfully")
            base_topic = self.topic.rsplit('/', 1)[0]  # Remove the last part of the topic
            client.subscribe(f"{base_topic}/+")  # Subscribe to all subtopics
        else:
            self._mqtt_status = "error"
            self._last_error = f"Connection failed with result code {rc}"
            logging.error(f"Failed to connect to MQTT broker with result code {rc}")
        self._connection_details = {
            "broker": self.broker,
            "port": self.port,
            "topic": self.topic,
            "username": self.username
        }
        from app.websocket import send_mqtt_status
        send_mqtt_status(self._mqtt_status)

    def on_disconnect(self, client, userdata, rc):
        self._mqtt_status = "disconnected"
        logging.info("Disconnected from MQTT broker")
        from app.websocket import send_mqtt_status
        send_mqtt_status(self._mqtt_status)

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

    @classmethod
    def get_last_error(cls):
        return cls._last_error

    @classmethod
    def get_connection_details(cls):
        return cls._connection_details
