from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user, current_user
from app.mqtt_client import MQTTClient
from app.database import get_messages, acknowledge_message, get_archived_messages, acknowledge_multiple_messages
from datetime import datetime
import pytz
from app.models import User

bp = Blueprint('main', __name__)

@bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    users = User.get_all()
    return render_template('admin.html', users=users)

@bp.route('/admin/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('main.index'))
    username = request.form['username']
    password = request.form['password']
    is_admin = 'is_admin' in request.form
    User.create(username, password, is_admin)
    flash('User created successfully.')
    return redirect(url_for('main.admin'))

@bp.route('/admin/update_user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('main.index'))
    username = request.form['username']
    password = request.form['password'] if request.form['password'] else None
    is_admin = 'is_admin' in request.form
    User.update(user_id, username, password, is_admin)
    flash('User updated successfully.')
    return redirect(url_for('main.admin'))

@bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('main.index'))
    User.delete(user_id)
    flash('User deleted successfully.')
    return redirect(url_for('main.admin'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@bp.route('/profile/reset_password', methods=['POST'])
@login_required
def reset_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    if current_user.check_password(current_password):
        current_user.set_password(new_password)
        flash('Password updated successfully.')
    else:
        flash('Current password is incorrect.')
    return redirect(url_for('main.profile'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/')
@login_required
def index():
    messages = get_messages(limit=10, include_unacknowledged=True)
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    formatted_messages = []
    for message in messages:
        utc_time = datetime.fromisoformat(message[1])
        amsterdam_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(amsterdam_tz)
        formatted_time = amsterdam_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_messages.append([message[0], formatted_time] + list(message[2:]))
    return render_template('index.html', messages=formatted_messages)

@bp.route('/archived_logs')
def archived_logs():
    messages = get_archived_messages()
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    formatted_messages = []
    for message in messages:
        utc_time = datetime.fromisoformat(message[1])
        amsterdam_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(amsterdam_tz)
        formatted_time = amsterdam_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_messages.append([message[0], formatted_time] + list(message[2:]))
    return render_template('archived_logs.html', messages=formatted_messages)

@bp.route('/diagnostics')
def diagnostics():
    mqtt_client = MQTTClient._instance
    if mqtt_client:
        mqtt_status = mqtt_client._mqtt_status
        button_status = mqtt_client._button_status
        last_error = mqtt_client._last_error
        connection_details = mqtt_client._connection_details
    else:
        mqtt_status = "unknown"
        button_status = "unknown"
        last_error = "MQTT client not initialized"
        connection_details = {}
    return render_template('diagnostics.html', 
                           mqtt_status=mqtt_status, 
                           button_status=button_status, 
                           last_error=last_error, 
                           connection_details=connection_details)

@bp.route('/acknowledge_event', methods=['POST'])
def acknowledge_event():
    message_id = request.json.get('message_id')
    note = request.json.get('note', '')
    acknowledge_message(message_id, note)
    return jsonify({"status": "success", "message": "Event acknowledged"})

@bp.route('/acknowledge_bulk_events', methods=['POST'])
def acknowledge_bulk_events():
    message_ids = request.json.get('message_ids', [])
    note = request.json.get('note', '')
    acknowledge_multiple_messages(message_ids, note)
    return jsonify({"status": "success", "message": "Events acknowledged"})

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/get_latest_data')
def get_latest_data():
    mqtt_client = MQTTClient._instance
    messages = get_messages(limit=5)  # Get the 5 most recent messages
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    formatted_messages = []
    for message in messages:
        utc_time = datetime.fromisoformat(message[1])
        amsterdam_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(amsterdam_tz)
        formatted_time = amsterdam_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_messages.append({
            "id": message[0],
            "timestamp": formatted_time,
            "status": message[2],
            "action": message[3],
            "acknowledged": bool(message[4]),
            "note": message[5]
        })
    
    return jsonify({
        "button_status": {
            "status": mqtt_client._button_status if mqtt_client else "Unknown",
            "action": mqtt_client._last_action if mqtt_client and hasattr(mqtt_client, '_last_action') else None
        },
        "device_status": {
            "battery": mqtt_client._battery_status if mqtt_client else "Unknown",
            "charger": mqtt_client._charger_status if mqtt_client else "Unknown",
            "wifi": mqtt_client._wifi_status if mqtt_client else "Unknown",
            "last_seen": mqtt_client._last_seen if mqtt_client else "Unknown"
        },
        "events": formatted_messages
    })

def init_mqtt_client(broker, port, topic, username, password):
    mqtt_client = MQTTClient(broker, port, topic, username, password)
    mqtt_client.start()
