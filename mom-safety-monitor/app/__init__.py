from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
import os

socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a real secret key
    
    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(int(user_id))

    return app
