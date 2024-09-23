# Mom's Safety Monitor

This web application monitors the status of a Shelby button connected via MQTT, displays a help message when the button is pressed, and allows remote control of an LED light.

## Project Plan

1. Set up MQTT client to listen for button presses and control LED
2. Create a web server using Flask
3. Implement real-time updates using WebSocket
4. Design a simple web interface to display button status and control LED
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
3. MQTT settings are pre-configured in `mom-safety-monitor/config.py` (no action required)
4. Connect the LED to the Raspberry Pi (refer to hardware setup instructions)
5. Run the application: `python run.py`

## Latest Developments

- Implemented basic Flask application structure
- Created MQTT client to listen for button presses and control LED
- Set up WebSocket for real-time updates
- Designed a simple web interface with CSS styling
- Implemented JavaScript for updating button status and controlling LED in real-time
- Added error handling and logging throughout the application
- Updated MQTT configuration with correct broker details

## Development Log

- 2023-09-23: Initial project setup and implementation of core functionality
- 2023-09-23: Fixed file path issues in run.py and moved requirements.txt to project root
- 2023-09-24: Implemented error handling and logging for MQTT client
- 2023-09-24: Added logging and error handling to run.py
- 2023-09-24: Integrated button press detection with MQTT client
- 2023-09-24: Updated WebSocket communication and frontend UI to display button status
- 2023-09-25: Added LED control functionality and updated MQTT client
- 2023-09-25: Updated MQTT configuration with correct broker details

## Things to Do

1. Test the MQTT connection with a real Shelby button and LED
2. Implement user authentication for the web interface
3. Design and implement Telegram/WhatsApp integration for notifications
4. Create a mobile-friendly version of the web interface
5. Set up automated testing for critical components
6. Optimize performance for handling multiple concurrent connections
7. Implement a database to store historical data of button presses and LED states

## Future Enhancements

- Integrate Telegram/WhatsApp messaging for notifications
- Add user authentication for accessing the web interface
- Implement logging and history of button presses and LED states
- Create a mobile app for easier monitoring and control
- Add support for multiple buttons and LEDs
