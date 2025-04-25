import sqlite3

def create_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def save_message(user_id: int, message: str, response: str):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO messages (user_id, message, response)
        VALUES (?, ?, ?)
    ''', (user_id, message, response))

    conn.commit()
    conn.close()
