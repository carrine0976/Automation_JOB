import sqlite3
from datetime import datetime

DB_NAME = "invite.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS invited_users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            invited_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def is_invited(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM invited_users WHERE user_id = ?",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row is not None

def mark_invited(user_id, username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO invited_users (user_id, username, invited_at) VALUES (?, ?, ?)",
        (user_id, username, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def init_group_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS group_id (
            group_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()
    


    
