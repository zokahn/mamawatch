document.addEventListener('DOMContentLoaded', () => {
    const buttonStatus = document.getElementById('button-status');
    const ledStatus = document.getElementById('led-status');
    const helpMessage = document.getElementById('help-message');
    const ledToggle = document.getElementById('led-toggle');

    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to WebSocket');
    });

    socket.on('button_status', (data) => {
        if (data.status === 'pressed') {
            buttonStatus.textContent = 'Pressed';
            buttonStatus.style.color = '#FF6B6B';
            helpMessage.classList.remove('hidden');
        } else {
            buttonStatus.textContent = 'Not Pressed';
            buttonStatus.style.color = '#4CAF50';
            helpMessage.classList.add('hidden');
        }
    });

    socket.on('led_status', (data) => {
        ledStatus.textContent = data.status === 'on' ? 'On' : 'Off';
        ledStatus.style.color = data.status === 'on' ? '#4CAF50' : '#FF6B6B';
    });

    ledToggle.addEventListener('click', () => {
        const currentStatus = ledStatus.textContent.toLowerCase();
        const newStatus = currentStatus === 'on' ? 'led_off' : 'led_on';
        socket.emit('led_control', newStatus);
    });

    socket.on('disconnect', () => {
        console.log('WebSocket connection closed');
        buttonStatus.textContent = 'Disconnected';
        buttonStatus.style.color = '#FFA500';
    });
});
