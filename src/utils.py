import json
import os
import sqlite3
def load_mental_health_data(file_path):
    """Safely loads the JSON database."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def format_hospital_info(hospital_list):
    """Converts JSON objects into clean strings for the Vector DB."""
    documents = []
    for h in hospital_list:
        entry = f"Hospital: {h['name']}, City: {h['city']}, Contact: {h['contact']}"
        documents.append(entry)
    return documents


DB_PATH = "chat_history.db"

def init_db():
    """Initializes the database and creates the 'chats' table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Adding 'IF NOT EXISTS' is crucial to prevent errors on repeat runs
    c.execute('''CREATE TABLE IF NOT EXISTS chats 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                  role TEXT, 
                  content TEXT)''')
    conn.commit()
    conn.close()

def save_message(role, content):
    # Ensure the database exists before saving
    init_db() 
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chats (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def clear_chat_history():
    """Deletes all messages from the database to allow for a fresh start."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM chats")
    conn.commit()
    conn.close()

def get_all_messages():
    """Fetches all stored messages from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, role, content FROM chats ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data