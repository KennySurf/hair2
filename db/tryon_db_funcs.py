import sqlite3

def get_end_cooldown_time(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cooldown = cursor.execute('SELECT end_cooldown_time FROM Users WHERE user_id = ?', (user_id,)).fetchone()
        if cooldown is None:
            return None

        cursor.execute('SELECT end_cooldown_time FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()[0]

def update_end_cooldown_time(user_id, time):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET end_cooldown_time = ? WHERE user_id = ?', (time, user_id))
        conn.commit()

def get_tryon_state(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT tryon_state FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()[0]

def update_tryon_state(user_id, state):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Users SET tryon_state = ? WHERE user_id = ?', (state, user_id))
        conn.commit()

def reset_tryon_state(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET tryon_state = ? WHERE user_id = ?', ('idle', user_id))
        conn.commit()

def get_tryon_prompt(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT tryon_prompt FROM Users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()[0]

def update_tryon_prompt(user_id, prompt):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET tryon_prompt = ? WHERE user_id = ?', (prompt, user_id))
        conn.commit()

def reset_tryon_prompt(user_id):
    with sqlite3.connect('users.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('UPDATE Users SET tryon_prompt = ? WHERE user_id = ?', (None, user_id))
        conn.commit()
