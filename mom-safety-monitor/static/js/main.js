document.addEventListener('DOMContentLoaded', () => {
    const buttonStatus = document.getElementById('button-status');
    const lastAction = document.getElementById('last-action');
    const messageText = document.getElementById('message-text');
    const messageContainer = document.getElementById('message');
    const eventLog = document.getElementById('event-log').querySelector('tbody');
    const ackForm = document.getElementById('ack-form');
    const ackNote = document.getElementById('ack-note');
    const ackMessageId = document.getElementById('ack-message-id');
    const acknowledgeFormContainer = document.getElementById('acknowledge-form');

    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to WebSocket');
        buttonStatus.textContent = 'Connected';
        buttonStatus.classList.remove('disconnected');
        buttonStatus.classList.add('connected');
    });

    socket.on('button_status', (data) => {
        updateButtonStatus(data);
        addEventToLog(data);
    });

    socket.on('device_status', (data) => {
        updateDeviceStatus(data);
    });

    socket.on('emergency_reset', (data) => {
        console.log('Emergency reset:', data.message);
        messageContainer.classList.add('hidden');
        messageContainer.classList.remove('animated', 'pulse');
        buttonStatus.textContent = 'Normal';
        lastAction.textContent = 'Emergency Reset';
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

        acknowledgeEvent(messageId, note);
    });

    const bulkAcknowledgeForm = document.getElementById('bulk-acknowledge-form');
    bulkAcknowledgeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const selectedMessages = Array.from(document.querySelectorAll('input[name="selected_messages"]:checked')).map(checkbox => checkbox.value);
        const note = prompt("Enter a note for the selected messages:");
        if (note !== null) {
            acknowledgeBulkEvents(selectedMessages, note);
        }
    });

    function acknowledgeBulkEvents(messageIds, note) {
        fetch('/acknowledge_bulk_events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message_ids: messageIds, note: note }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                messageIds.forEach(id => {
                    const row = document.querySelector(`tr[data-message-id="${id}"]`);
                    row.cells[4].textContent = 'Yes';
                    row.cells[5].textContent = note;
                    row.cells[6].textContent = '';
                    row.classList.add('animated', 'flash');
                    row.querySelector('input[type="checkbox"]').disabled = true;
                });
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    socket.on('disconnect', () => {
        console.log('WebSocket connection closed');
        buttonStatus.textContent = 'Disconnected';
        buttonStatus.classList.remove('connected');
        buttonStatus.classList.add('disconnected');
    });

    function updateButtonStatus(data) {
        buttonStatus.textContent = data.status;
        lastAction.textContent = data.action;

        if (data.status === 'call_request' || data.status === 'emergency') {
            messageText.textContent = data.status === 'call_request' ? 'Help requested by Mom' : 'Emergency! Mom needs immediate assistance!';
            messageContainer.classList.remove('hidden');
            messageContainer.classList.add('animated', 'pulse');
        } else if (data.status === 'normal') {
            messageContainer.classList.add('hidden');
            messageContainer.classList.remove('animated', 'pulse');
        }
    }

    function addEventToLog(data) {
        const newRow = eventLog.insertRow(0);
        newRow.dataset.messageId = data.id;
        newRow.innerHTML = `
            <td>${new Date(data.timestamp).toLocaleString()}</td>
            <td>${data.status}</td>
            <td>${data.action}</td>
            <td>No</td>
            <td></td>
            <td><button class="ack-button" data-message-id="${data.id}">Acknowledge</button></td>
        `;
        newRow.classList.add('animated', 'fadeIn');
    }

    function updateDeviceStatus(data) {
        const deviceStatus = document.getElementById('device-status');
        deviceStatus.innerHTML = `
            <p>Battery: ${data.battery}%</p>
            <p>Charger: ${data.charger ? 'Connected' : 'Disconnected'}</p>
            <p>WiFi: ${data.wifi.connected ? 'Connected' : 'Disconnected'}</p>
            <p>Last Seen: ${new Date(data.last_seen).toLocaleString()}</p>
        `;
    }

    function acknowledgeEvent(messageId, note) {
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
                const acknowledgedRow = document.querySelector(`tr[data-message-id="${messageId}"]`);
                acknowledgedRow.cells[3].textContent = 'Yes';
                acknowledgedRow.cells[4].textContent = note;
                acknowledgedRow.cells[5].textContent = '';
                acknowledgeFormContainer.classList.add('hidden');
                ackNote.value = '';
                acknowledgedRow.classList.add('animated', 'flash');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function refreshData() {
        fetch('/get_latest_data')
        .then(response => response.json())
        .then(data => {
            updateButtonStatus(data.button_status);
            updateDeviceStatus(data.device_status);
            data.events.forEach(event => addEventToLog(event));
        })
        .catch(error => console.error('Error refreshing data:', error));
    }

    // Refresh data every 30 seconds
    setInterval(refreshData, 30000);
});
