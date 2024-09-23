document.addEventListener('DOMContentLoaded', function() {
    var socket = io();
    var buttonStatus = document.getElementById('button-status');
    var message = document.getElementById('message');
    var messageText = document.getElementById('message-text');

    socket.on('mqtt_status', function(data) {
        document.getElementById('mqtt-status').textContent = data.status;
    });

    socket.on('button_status', function(data) {
        buttonStatus.textContent = data.status;
        message.classList.remove('hidden');
        
        switch(data.status) {
            case 'call_request':
                messageText.textContent = 'Mom requests a call';
                break;
            case 'emergency':
                messageText.textContent = 'EMERGENCY: Mom needs immediate assistance!';
                break;
            case 'reset':
                messageText.textContent = 'Action reset';
                break;
            default:
                message.classList.add('hidden');
        }
    });
});
