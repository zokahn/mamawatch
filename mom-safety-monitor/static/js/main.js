document.addEventListener('DOMContentLoaded', () => {
    const buttonStatus = document.getElementById('button-status');
    const lastAction = document.getElementById('last-action');
    const messageText = document.getElementById('message-text');
    const messageContainer = document.getElementById('message');
    const eventLog = document.getElementById('event-log');
    const ackForm = document.getElementById('ack-form');
    const ackNote = document.getElementById('ack-note');

    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to WebSocket');
    });

    socket.on('button_status', (data) => {
        buttonStatus.textContent = data.status;
        lastAction.textContent = data.action;

        if (data.status === 'call_request' || data.status === 'emergency') {
            messageText.textContent = data.status === 'call_request' ? 'Help requested by Mom' : 'Emergency! Mom needs immediate assistance!';
            messageContainer.classList.remove('hidden');
        } else {
            messageContainer.classList.add('hidden');
        }

        // Add event to log
        const logEntry = document.createElement('li');
        logEntry.innerHTML = `
            <strong>Button:</strong> ${data.button_name}<br>
            <strong>Action:</strong> ${data.action}<br>
            <strong>Time:</strong> ${new Date(data.timestamp).toLocaleString()}<br>
            <strong>Acknowledged:</strong> <span class="ack-status">No</span><br>
            <strong>Note:</strong> <span class="ack-note"></span>
        `;
        eventLog.insertBefore(logEntry, eventLog.firstChild);
    });

    ackForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const latestEvent = eventLog.firstChild;
        if (latestEvent) {
            latestEvent.querySelector('.ack-status').textContent = 'Yes';
            latestEvent.querySelector('.ack-note').textContent = ackNote.value;
            socket.emit('acknowledge_event', { note: ackNote.value });
            ackNote.value = '';
        }
    });

    socket.on('disconnect', () => {
        console.log('WebSocket connection closed');
        buttonStatus.textContent = 'Disconnected';
    });
});
