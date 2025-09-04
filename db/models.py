import sqlite3
import os

def create_table():
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        state TEXT DEFAULT get_services,
        user_id INTEGER UNIQUE,
        services_id INTEGER DEFAULT NULL,
        master_id INTEGER DEFAULT NULL,
        date TEXT DEFAULT NULL,
        time TEXT DEFAULT NULL);
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
