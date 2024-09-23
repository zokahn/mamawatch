# Mom's Safety Monitor

This web application monitors the status of a Shelby button connected via MQTT and displays a help message when the button is pressed.

## Project Plan

1. Set up MQTT client to listen for button presses
2. Create a web server using Flask
3. Implement real-time updates using WebSocket
4. Design a simple web interface to display button status
5. Add functionality to show "Hulp gevraagd door mama" message when button is pressed
6. (Future) Implement Telegram/WhatsApp integration for notifications

## Directory Structure

```
mom-safety-monitor/
├── app/
│   ├── __init__.py
│   ├── mqtt_client.py
│   ├── routes.py
│   └── websocket.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── config.py
├── requirements.txt
└── run.py
```

## Setup and Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure MQTT settings in `config.py`
4. Run the application: `python run.py`

## Future Enhancements

- Integrate Telegram/WhatsApp messaging for notifications
- Add user authentication for accessing the web interface
- Implement logging and history of button presses
- Create a mobile app for easier monitoring
