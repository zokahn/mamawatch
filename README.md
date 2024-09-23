# Mom's Safety Monitor

This web application monitors the status of a Shelly Button1 connected via MQTT and displays real-time updates on button presses and device status.

## Project Overview

The Mom's Safety Monitor is designed to provide a simple and effective way to monitor a Shelly Button1 device, typically used as an emergency or assistance button. It displays real-time updates on button presses and provides detailed diagnostic information about the device's status.

## Features

- Real-time monitoring of Shelly Button1 status
- Display of button press events (single press, long press, double press)
- Detailed diagnostic information including battery status, WiFi connection, and more
- Event logging with acknowledgment functionality
- WebSocket-based real-time updates

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
│       ├── main.js
│       └── diagnostics.js
├── templates/
│   ├── index.html
│   └── diagnostics.html
├── config.py
├── requirements.txt
├── run.py
└── .env
```

## Setup and Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with the correct MQTT broker details (a sample is provided)
4. Run the application: `python run.py`

## Latest Developments

- Implemented comprehensive MQTT client to handle various Shelly Button1 events and status updates
- Created a detailed diagnostics page for monitoring device status
- Added event logging functionality with acknowledgment feature
- Improved error handling and logging throughout the application
- Updated the web interface to display more detailed device information

## Development Log

- 2023-09-23: Initial project setup and implementation of core functionality
- 2023-09-24: Implemented error handling and logging for MQTT client
- 2023-09-25: Added comprehensive device status monitoring and diagnostics page
- 2023-09-26: Implemented event logging and acknowledgment functionality
- 2023-09-27: Refactored MQTT client to handle various Shelly Button1 topics and payloads

## Things to Do

1. Implement user authentication for the web interface
2. Add data persistence for event logs and device status history
3. Implement Telegram/WhatsApp integration for notifications
4. Create a mobile-friendly version of the web interface
5. Set up automated testing for critical components
6. Optimize performance for handling multiple concurrent connections
7. Implement support for multiple Shelly Button1 devices

## Future Enhancements

- Add user authentication and multi-user support
- Implement a database to store historical data of button presses and device status
- Create a mobile app for easier monitoring on-the-go
- Add support for other Shelly devices
- Implement customizable alert thresholds (e.g., low battery warnings)

## Contributing

Contributions to the Mom's Safety Monitor project are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is open-source and available under the MIT License.
