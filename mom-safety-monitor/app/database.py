import sqlite3
from datetime import datetime
from flask import current_app, g

DATABASE = 'app.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def add_message(status, action):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (timestamp, status, action, acknowledged) VALUES (?, ?, ?, ?)",
              (datetime.now().isoformat(), status, action, 0))
    message_id = c.lastrowid
    conn.commit()
    conn.close()
    return message_id

def get_messages(limit=None, include_unacknowledged=False):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if include_unacknowledged:
        c.execute("SELECT * FROM messages WHERE acknowledged = 0 OR id IN (SELECT id FROM messages ORDER BY timestamp DESC LIMIT ?) ORDER BY timestamp DESC", (limit,))
    else:
        c.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))
    messages = [list(row) for row in c.fetchall()]
    conn.close()
    return messages

def get_archived_messages():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE acknowledged = 1 ORDER BY timestamp DESC")
    messages = [list(row) for row in c.fetchall()]
    conn.close()
    return messages

def acknowledge_message(message_id, note):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE messages SET acknowledged = 1, note = ? WHERE id = ?", (note, message_id))
    conn.commit()
    conn.close()

def acknowledge_multiple_messages(message_ids, note):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.executemany("UPDATE messages SET acknowledged = 1, note = ? WHERE id = ?", [(note, id) for id in message_ids])
    conn.commit()
    conn.close()
