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
