document.addEventListener('DOMContentLoaded', function() {
    var socket = io();

    socket.on('mqtt_status', function(data) {
        document.getElementById('mqtt-status').textContent = data.status;
    });

    socket.on('button_status', function(data) {
        document.getElementById('button-status').textContent = data.status;
    });
});
