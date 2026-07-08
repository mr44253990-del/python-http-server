from utils.db import get_db

def add_deposit_request(user_id, amount, trx_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO transactions (user_id, amount, trx_id, status) VALUES (?, ?, ?, ?)', 
                       (user_id, amount, trx_id, 'Pending'))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()
