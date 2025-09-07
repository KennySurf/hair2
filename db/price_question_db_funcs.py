import sqlite3

def update_price_question_state(user_id, state):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET price_question_state = ? WHERE user_id = ?', (state, user_id))
        conn.commit()

def get_price_question_state(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT price_question_state FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()[0]

def reset_price_question_state(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET price_question_state = ? WHERE user_id = ?', (None, user_id))
        conn.commit()
