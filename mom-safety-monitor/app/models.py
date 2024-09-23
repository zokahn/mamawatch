from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

class User(UserMixin):
    def __init__(self, id, username, password_hash, is_admin=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            return User(user['id'], user['username'], user['password_hash'], user['is_admin'])
        return None

    @staticmethod
    def get_all():
        db = get_db()
        users = db.execute('SELECT * FROM users').fetchall()
        return [User(user['id'], user['username'], user['password_hash'], user['is_admin']) for user in users]

    @staticmethod
    def create(username, password, is_admin=False):
        db = get_db()
        db.execute(
            'INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), is_admin)
        )
        db.commit()

    @staticmethod
    def update(user_id, username=None, password=None, is_admin=None):
        db = get_db()
        updates = []
        values = []
        if username is not None:
            updates.append('username = ?')
            values.append(username)
        if password is not None:
            updates.append('password_hash = ?')
            values.append(generate_password_hash(password))
        if is_admin is not None:
            updates.append('is_admin = ?')
            values.append(is_admin)
        
        if updates:
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            values.append(user_id)
            db.execute(query, tuple(values))
            db.commit()

    @staticmethod
    def delete(user_id):
        db = get_db()
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()

    @staticmethod
    def authenticate(username, password):
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            return User(user['id'], user['username'], user['password_hash'], user['is_admin'])
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db = get_db()
        db.execute('UPDATE users SET password_hash = ? WHERE id = ?', (self.password_hash, self.id))
        db.commit()
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
