import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/chat_history.db")

def init_db():
    """Initialize the SQLite database and create the chat_history table if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Ensure data/ folder exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            session_id TEXT,
            timestamp DATETIME,
            role TEXT,        -- 'user' or 'assistant'
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(session_id: str, role: str, message: str):
    """Save a single message to chat history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (session_id, timestamp, role, message) VALUES (?, ?, ?, ?)",
        (session_id, datetime.utcnow(), role, message)
    )
    conn.commit()
    conn.close()

def get_history(session_id: str, limit: int = 10):
    """
    Retrieve the last `limit` messages for a session, ordered oldest first.
    
    Returns:
        List[dict]: List of messages in the form [{"role": role, "content": message}, ...]
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, message FROM chat_history WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
        (session_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    # Reverse to return oldest first (chat order)
    return [{"role": role, "content": message} for role, message in reversed(rows)]
