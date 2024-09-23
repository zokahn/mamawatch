from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, login_user, current_user
from app.mqtt_client import MQTTClient
from app.database import get_messages
from app.models import User

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

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(1) if username == 'admin' else User.get(2)  # Simplified user retrieval
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
