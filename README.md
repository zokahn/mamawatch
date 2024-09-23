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
.
├── README.md
├── app
│   ├── mqtt_client.py
│   └── routes.py
├── config.py
└── mom-safety-monitor
    ├── app
    │   ├── __init__.py
    │   ├── database.py
    │   ├── mqtt_client.py
    │   ├── routes.py
    │   └── websocket.py
    ├── config.py
    ├── messages.db
    ├── requirements.txt
    ├── run.py
    ├── static
    │   ├── css
    │   │   └── style.css
    │   └── js
    │       ├── diagnostics.js
    │       └── main.js
    └── templates
        ├── archived_logs.html
        ├── diagnostics.html
        └── index.html
```

## Setup and Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with the correct MQTT broker details (a sample is provided)
4. Run the application: `python run.py`

## Latest Developments

- Implemented a database system for storing messages (messages.db)
- Added an archived logs feature with a new template (archived_logs.html)
- Restructured the project directory for better organization
- Implemented a database module (database.py) for handling data persistence
- Updated the MQTT client and routes to work with the new structure

## Current Features

- Real-time monitoring of Shelly Button1 status
- Display of button press events (single press, long press, double press)
- Detailed diagnostic information including battery status, WiFi connection, and more
- Event logging with acknowledgment functionality
- WebSocket-based real-time updates
- Data persistence using SQLite database
- Archived logs view for historical data

## Things to Do

1. Implement user authentication for the web interface
2. Implement Telegram/WhatsApp integration for notifications
3. Create a mobile-friendly version of the web interface
4. Set up automated testing for critical components
5. Optimize performance for handling multiple concurrent connections
6. Implement support for multiple Shelly Button1 devices
7. Enhance the archived logs feature with filtering and sorting options

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
