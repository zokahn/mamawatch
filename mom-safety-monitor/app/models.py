from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        # This is a mock implementation. In a real application, you would fetch the user from a database.
        users = {
            1: User(1, 'admin', generate_password_hash('admin')),
            2: User(2, 'user', generate_password_hash('user'))
        }
        return users.get(int(user_id))

    @staticmethod
    def authenticate(username, password):
        users = {
            'admin': User(1, 'admin', generate_password_hash('admin')),
            'user': User(2, 'user', generate_password_hash('user'))
        }
        user = users.get(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        # This is a mock implementation. In a real application, you would fetch the user from a database.
        users = {
            1: User(1, 'admin', generate_password_hash('admin_password'))
        }
        return users.get(int(user_id))

    @staticmethod
    def authenticate(username, password):
        user = User.get(1)  # In a real app, you would search for the user by username
        if user and user.username == username and check_password_hash(user.password_hash, password):
            return user
        return None
