document.addEventListener('DOMContentLoaded', function() {
    var socket = io();
    var mqttStatus = document.getElementById('mqtt-status');
    var buttonStatus = document.getElementById('button-status');
    var lastUpdate = document.getElementById('last-update');

    function updateStatus(elementId, status) {
        var element = document.getElementById(elementId);
        element.textContent = status;
        element.className = status.toLowerCase();
    }

    function updateDeviceStatus(data) {
        document.getElementById('battery-status').textContent = data.battery ? data.battery + '%' : 'Unknown';
        document.getElementById('charger-status').textContent = data.charger ? 'Charging' : 'Not charging';
        if (data.wifi) {
            document.getElementById('wifi-ssid').textContent = data.wifi.ssid || 'Unknown';
            document.getElementById('wifi-ip').textContent = data.wifi.ip || 'Unknown';
            document.getElementById('wifi-signal').textContent = data.wifi.rssi ? data.wifi.rssi + ' dBm' : 'Unknown';
        }
        document.getElementById('last-seen').textContent = data.last_seen ? new Date(data.last_seen).toLocaleString() : 'Unknown';
        
        // Update debug information
        document.getElementById('debug-info').textContent = JSON.stringify(data, null, 2);
    }

    socket.on('connect', function() {
        console.log('Connected to server');
        updateStatus('server-status', 'Connected');
    });

    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        updateStatus('server-status', 'Disconnected');
        updateStatus('mqtt-status', 'Unknown');
    });

    socket.on('mqtt_status', function(data) {
        console.log('MQTT status update:', data);
        updateStatus('mqtt-status', data.status);
        if (data.last_error) {
            document.getElementById('last-error').textContent = data.last_error;
        }
        lastUpdate.textContent = new Date().toLocaleString();
    });

    socket.on('button_status', function(data) {
        console.log('Button status update:', data);
        updateStatus('button-status', data.status);
        lastUpdate.textContent = new Date().toLocaleString();
    });

    socket.on('device_status', function(data) {
        console.log('Device status update:', data);
        updateDeviceStatus(data);
        lastUpdate.textContent = new Date().toLocaleString();
    });

    socket.on('connection_details', function(data) {
        console.log('Connection details update:', data);
        for (let key in data) {
            let element = document.getElementById(key + '-detail');
            if (element) {
                element.textContent = data[key];
            }
        }
    });

    // Request initial status
    socket.emit('get_status');
});
document.addEventListener('DOMContentLoaded', function() {
    var socket = io();
    var mqttStatus = document.getElementById('mqtt-status');
    var buttonStatus = document.getElementById('button-status');
    var lastUpdate = document.getElementById('last-update');

    function updateStatus(elementId, status) {
        var element = document.getElementById(elementId);
        element.textContent = status;
        element.className = status.toLowerCase();
    }

    socket.on('connect', function() {
        console.log('Connected to server');
        updateStatus('server-status', 'Connected');
    });

    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        updateStatus('server-status', 'Disconnected');
        updateStatus('mqtt-status', 'Unknown');
    });

    socket.on('mqtt_status', function(data) {
        console.log('MQTT status update:', data);
        updateStatus('mqtt-status', data.status);
        if (data.last_error) {
            document.getElementById('last-error').textContent = data.last_error;
        }
        lastUpdate.textContent = new Date().toLocaleString();
    });

    socket.on('button_status', function(data) {
        console.log('Button status update:', data);
        updateStatus('button-status', data.status);
        lastUpdate.textContent = new Date().toLocaleString();
    });

    socket.on('connection_details', function(data) {
        console.log('Connection details update:', data);
        for (let key in data) {
            let element = document.getElementById(key + '-detail');
            if (element) {
                element.textContent = data[key];
            }
        }
    });

    // Request initial status
    socket.emit('get_status');
});
