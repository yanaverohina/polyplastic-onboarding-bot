import sqlite3
import os
from typing import Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "hr_ai.db")

def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT DEFAULT 'employee',
        tone TEXT DEFAULT 'formal',
        current_stage TEXT DEFAULT 'day_minus_3',
        department TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS steps (
        id TEXT PRIMARY KEY,
        name TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS progress (
        user_id INTEGER,
        step_id TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(step_id) REFERENCES steps(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        status TEXT DEFAULT 'open',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    from scenario import ONBOARDING_STAGES
    for stage in ONBOARDING_STAGES:
        c.execute("INSERT OR IGNORE INTO steps (id, name) VALUES (?, ?)", (stage["id"], stage["name"]))

    conn.commit()
    conn.close()

def get_or_create_user(user_id: int, name: str) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users (id, name, role) VALUES (?, ?, 'employee')", (user_id, name))
        conn.commit()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = c.fetchone()
    conn.close()
    return dict(user) if user else {}

def update_user_tone(user_id: int, tone: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET tone=? WHERE id=?", (tone, user_id))
    conn.commit()
    conn.close()