from utils.db import get_db

def get_pending_deposits():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, user_id, amount, trx_id FROM transactions WHERE status = "Pending"')
    rows = cursor.fetchall()
    conn.close()
    return rows

def approve_deposit(tx_id):
    conn = get_db()
    cursor = conn.cursor()
    # Transaction আপডেট করা
    cursor.execute('UPDATE transactions SET status = "Approved" WHERE id = ?', (tx_id,))
    # User ব্যালেন্স যোগ করা
    cursor.execute('SELECT user_id, amount FROM transactions WHERE id = ?', (tx_id,))
    data = cursor.fetchone()
    if data:
        cursor.execute('UPDATE users SET balance = balance + ? WHERE telegram_id = ?', (data[1], data[0]))
    conn.commit()
    conn.close()
