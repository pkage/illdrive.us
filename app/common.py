from .db import get_db
import random

def resolve_user(user_id):
    db = get_db()
    db.execute('SELECT * FROM Users WHERE id=?', (user_id,))
    return db.fetchone()

def get_random_str(length):
    # simplicity!
    out = ''
    for i in range(length):
        out += random.choice('abcdefghijklmnopqrstuvwxyz0123456789')

    return out
