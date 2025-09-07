import sqlite3
import os

def create_table():
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        state TEXT DEFAULT idle,
        user_id INTEGER UNIQUE,
        services_id INTEGER DEFAULT NULL,
        master_id INTEGER DEFAULT NULL,
        date TEXT DEFAULT NULL,
        time TEXT DEFAULT NULL,
        end_cooldown_time DEFAULT NULL,
        tryon_state TEXT DEFAULT idle,
        tryon_prompt TEXT DEFAULT NULL,
        price_question_state TEXT DEFAULT idle);
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
        user_id INTEGER,
        role TEXT,
        content TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id));
    ''')

    conn.commit()
    conn.close()

def run_table():
    if os.path.exists('users.sqlite'):
        print('Users table already exists')
        return
    print('Table creation')
    create_table()
