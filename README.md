# Mom's Safety Monitor

This web application monitors the status of a Shelly Button1 connected via MQTT and displays real-time updates on button presses and device status.

## Project Overview

The Mom's Safety Monitor is designed to provide a simple and effective way to monitor a Shelly Button1 device, typically used as an emergency or assistance button. It displays real-time updates on button presses and provides detailed diagnostic information about the device's status.

## Features

- Real-time monitoring of Shelly Button1 status
- Display of button press events (single press, long press, double press)
- Detailed diagnostic information including battery status, WiFi connection, and more
- Event logging with individual and bulk acknowledgment functionality
- WebSocket-based real-time updates with animations
- Data persistence using SQLite database
- User authentication and admin panel
- Archived logs view for historical data
- Auto-refresh functionality for the main page
- Emergency reset feature
- Improved error handling for various MQTT message formats

## Directory Structure

```
mom-safety-monitor/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── mqtt_client.py
│   ├── routes.py
│   ├── schema.sql
│   └── websocket.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── diagnostics.js
│       └── main.js
├── templates/
│   ├── admin.html
│   ├── archived_logs.html
│   ├── base.html
│   ├── diagnostics.html
│   ├── index.html
│   ├── login.html
│   └── profile.html
├── .env
├── config.py
├── README.md
├── requirements.txt
└── run.py
```

## Setup and Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with the correct MQTT broker details and other configuration (a sample is provided)
4. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the application: `python run.py`

## Latest Developments

- Implemented user authentication and admin panel
- Added user profile management (password reset)
- Enhanced security with password hashing
- Improved database schema and initialization process
- Updated UI with responsive design improvements
- Implemented bulk acknowledgment functionality for event logs
- Created an archived logs page for viewing historical data
- Enhanced the main page to show the last 10 and unacknowledged messages
- Implemented auto-page refresh functionality for real-time updates
- Improved MQTT client to handle various message types and sensor data correctly
- Added emergency reset functionality

## Current Features

- User authentication with admin and regular user roles
- Admin panel for user management
- Real-time monitoring of Shelly Button1 status
- Display of button press events (single press, long press, double press)
- Detailed diagnostic information including battery status, WiFi connection, and more
- Event logging with individual and bulk acknowledgment functionality
- WebSocket-based real-time updates with animations
- Data persistence using SQLite database
- Archived logs view for historical data
- Auto-refresh functionality for the main page
- Emergency reset feature
- Improved error handling for various MQTT message formats

## Future Enhancements

- Implement Telegram/WhatsApp integration for notifications
- Enhance the mobile-friendly version of the web interface
- Set up automated testing for critical components
- Optimize performance for handling multiple concurrent connections
- Implement support for multiple Shelly Button1 devices
- Enhance the archived logs feature with filtering and sorting options
- Implement customizable alert thresholds (e.g., low battery warnings)
- Add support for other Shelly devices
- Create a mobile app for easier monitoring on-the-go

## Contributing

Contributions to the Mom's Safety Monitor project are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is open-source and available under the MIT License.
