document.addEventListener('DOMContentLoaded', () => {
    const buttonStatus = document.getElementById('button-status');
    const lastAction = document.getElementById('last-action');
    const messageText = document.getElementById('message-text');
    const messageContainer = document.getElementById('message');
    const eventLog = document.getElementById('event-log');
    const ackForm = document.getElementById('ack-form');
    const ackNote = document.getElementById('ack-note');
    const ackMessageId = document.getElementById('ack-message-id');
    const acknowledgeFormContainer = document.getElementById('acknowledge-form');

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
            <strong>Status:</strong> ${data.status}<br>
            <strong>Action:</strong> ${data.action}<br>
            <strong>Time:</strong> ${new Date(data.timestamp).toLocaleString()}<br>
            <strong>Acknowledged:</strong> No<br>
            <button class="ack-button" data-message-id="${data.id}">Acknowledge</button>
        `;
        eventLog.insertBefore(logEntry, eventLog.firstChild);
    });

    eventLog.addEventListener('click', (e) => {
        if (e.target.classList.contains('ack-button')) {
            const messageId = e.target.getAttribute('data-message-id');
            ackMessageId.value = messageId;
            acknowledgeFormContainer.classList.remove('hidden');
        }
    });

    ackForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const messageId = ackMessageId.value;
        const note = ackNote.value;

        fetch('/acknowledge_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message_id: messageId, note: note }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const acknowledgedEvent = document.querySelector(`[data-message-id="${messageId}"]`).closest('li');
                acknowledgedEvent.querySelector('.ack-button').remove();
                acknowledgedEvent.innerHTML = acknowledgedEvent.innerHTML.replace('Acknowledged: No', `Acknowledged: Yes<br><strong>Note:</strong> ${note}`);
                acknowledgeFormContainer.classList.add('hidden');
                ackNote.value = '';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    socket.on('disconnect', () => {
        console.log('WebSocket connection closed');
        buttonStatus.textContent = 'Disconnected';
    });
});
