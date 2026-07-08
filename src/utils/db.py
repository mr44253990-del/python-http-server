import sqlite3
def get_db():
    conn = sqlite3.connect('app.db', check_same_thread=False)
    return conn

def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, name TEXT, balance REAL DEFAULT 0.0, status TEXT DEFAULT "Active")')
    conn.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount REAL, trx_id TEXT, status TEXT)')
    conn.commit()
    conn.close()
