import sqlite3
from datetime import datetime

DB_NAME = "elara_users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            created_at TEXT,
            birthdate TEXT,
            tariff TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE id=?", (user_id,))
    if not c.fetchone():
        c.execute("INSERT INTO users (id, username, first_name, created_at) VALUES (?, ?, ?, ?)",
                  (user_id, username, first_name, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
