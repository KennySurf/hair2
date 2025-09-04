import sqlite3
from services.gpt.gpt_config import GPT_SYSTEM_PROMPT

def add_message(user_id, role, content, system_prompt=GPT_SYSTEM_PROMPT):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        user = cursor.execute('SELECT user_id FROM Users WHERE user_id = ?', (user_id,)).fetchone()

        if user is None:
            cursor.execute('INSERT INTO Users (user_id) VALUES (?)', (user_id,))
            cursor.execute('INSERT INTO Messages (user_id, role, content) VALUES (?, ?, ?)',
                           (user_id, role, system_prompt))

        cursor.execute('INSERT INTO Messages (user_id, role, content) VALUES (?, ?, ?)',
                       (user_id, role, content))

        conn.commit()

def get_user_messages(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT user_id FROM Messages WHERE user_id = ?', (user_id,))
        messages = cursor.fetchone()

        if messages is None:
            return None

        messages = cursor.execute('SELECT role, content FROM Messages WHERE user_id = ?', (user_id,)).fetchall()
        messages_list = [{'role': message[0], 'content': message[1]} for message in messages]
        return messages_list

def update_state(user_id, state):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Users SET state = ? WHERE user_id = ?',(state, user_id))
        conn.commit()

def get_state(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT state FROM Users WHERE user_id = ?', (user_id,))
        state = cursor.fetchone()
        return state

def update_services_id(user_id, service_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Users SET service_id = ? WHERE user_id = ?', (service_id, user_id))

        conn.commit()

def get_services_id(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT service_id FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def update_master_id(user_id, master_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Users SET master_id = ? WHERE user_id = ?', (master_id, user_id))
        conn.commit()

def get_master_id(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT master_id FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def get_date(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def update_date(user_id, date):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Users SET date = ? WHERE user_id = ?', (date, user_id))
        conn.commit()

def update_time(user_id, time):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Users SET time = ? WHERE user_id = ?', (time, user_id))
        conn.commit()

def get_time(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT time FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
