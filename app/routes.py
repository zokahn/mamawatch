from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user
from app.mqtt_client import MQTTClient
from app.database import get_messages

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    messages = get_messages(limit=10, include_unacknowledged=True)
    formatted_messages = [[str(m[0]), m[1], m[2], m[3], bool(m[4]), m[5]] for m in messages]
    return render_template('index.html', messages=formatted_messages)

@bp.route('/diagnostics')
@login_required
def diagnostics():
    mqtt_status = MQTTClient.get_status()
    button_status = MQTTClient.get_button_status()
    return render_template('diagnostics.html', mqtt_status=mqtt_status, button_status=button_status)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
