document.addEventListener('DOMContentLoaded', () => {
    const buttonStatus = document.getElementById('button-status');
    const helpMessage = document.getElementById('help-message');

    const socket = new WebSocket('ws://' + location.host + '/ws');

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.status === 'pressed') {
            buttonStatus.textContent = 'Pressed';
            buttonStatus.style.color = '#FF6B6B';
            helpMessage.classList.remove('hidden');
        } else {
            buttonStatus.textContent = 'Not Pressed';
            buttonStatus.style.color = '#4CAF50';
            helpMessage.classList.add('hidden');
        }
    };

    socket.onclose = function(event) {
        console.log('WebSocket connection closed:', event);
        buttonStatus.textContent = 'Disconnected';
        buttonStatus.style.color = '#FFA500';
    };
});
