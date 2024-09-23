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
        lastUpdate.textContent = new Date().toLocaleString();
    });

    socket.on('button_status', function(data) {
        console.log('Button status update:', data);
        updateStatus('button-status', data.status);
        lastUpdate.textContent = new Date().toLocaleString();
    });

    // Request initial status
    socket.emit('get_status');
});
