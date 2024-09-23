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

## Latest Developments

- Implemented basic Flask application structure
- Created MQTT client to listen for button presses
- Set up WebSocket for real-time updates
- Designed a simple web interface with CSS styling
- Implemented JavaScript for updating button status in real-time

## Development Log

- 2023-09-23: Initial project setup and implementation of core functionality
- 2023-09-23: Fixed file path issues in run.py and moved requirements.txt to project root

## Things to Do

1. Test the MQTT connection with a real Shelby button
2. Implement error handling for MQTT connection failures
3. Add logging functionality to track button presses and system events
4. Create a configuration file for easy customization of MQTT settings and other parameters
5. Implement user authentication for the web interface
6. Design and implement Telegram/WhatsApp integration for notifications
7. Create a mobile-friendly version of the web interface
8. Set up automated testing for critical components
9. Optimize performance for handling multiple concurrent connections
10. Implement a database to store historical data of button presses

## Future Enhancements

- Integrate Telegram/WhatsApp messaging for notifications
- Add user authentication for accessing the web interface
- Implement logging and history of button presses
- Create a mobile app for easier monitoring
