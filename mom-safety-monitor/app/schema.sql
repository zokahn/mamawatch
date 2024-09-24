CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    status TEXT,
    action TEXT,
    acknowledged INTEGER DEFAULT 0,
    note TEXT
);

-- Create initial admin user
INSERT OR IGNORE INTO users (username, password_hash, is_admin) 
VALUES ('admin', 'REPLACE_WITH_SECURE_HASH', 1);

-- IMPORTANT: Replace 'REPLACE_WITH_SECURE_HASH' above with a secure hash generated using the following Python code:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('your_secure_admin_password'))
-- Do not use the placeholder hash in production!
-- To generate a secure hash, use the following Python code:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('your_admin_password'))
