import json, sqlite3, time, urllib.request, urllib.parse, os

def init():
    conn = sqlite3.connect('app.db', check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, balance REAL DEFAULT 0)')
    conn.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, amount REAL, trx_id TEXT UNIQUE, status TEXT)')
    conn.commit()
    conn.close()

def run_bot():
    token = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    ADMIN_ID = 5893363292
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset + 1}"
            with urllib.request.urlopen(url, timeout=15) as res:
                data = json.loads(res.read().decode())
                for u in data.get('result', []):
                    offset = u['update_id']
                    chat_id = u['message']['chat']['id']
                    text = u['message'].get('text', '')
                    
                    # Logic for users: /deposit amount trx_id
                    if text.startswith('/deposit'):
                        parts = text.split()
                        if len(parts) == 3:
                            try:
                                amt, tid = float(parts[1]), parts[2]
                                conn = sqlite3.connect('app.db')
                                conn.execute("INSERT INTO transactions (telegram_id, amount, trx_id, status) VALUES (?, ?, ?, ?)", (chat_id, amt, tid, 'Pending'))
                                conn.commit()
                                conn.close()
                                reply = "Deposit request submitted! Wait for admin approval."
                            except: reply = "Error: TRX ID must be unique or data invalid."
                        else: reply = "Usage: /deposit [amount] [trx_id]"
                    # Admin logic
                    elif chat_id == ADMIN_ID:
                        if text == '/admin': reply = "Admin Menu: /pending, /stats"
                        elif text == '/pending':
                            conn = sqlite3.connect('app.db')
                            rows = conn.execute("SELECT id, telegram_id, amount, trx_id FROM transactions WHERE status='Pending'").fetchall()
                            reply = "Pending Deposits:\n" + str(rows) if rows else "No pending deposits."
                            conn.close()
                        else: reply = "Admin mode active."
                    else: reply = "Welcome! Use /deposit [amount] [trxid] to add funds."
                    
                    send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                    urllib.request.urlopen(f"{send_url}?chat_id={chat_id}&text={urllib.parse.quote(reply)}")
        except: time.sleep(10)

if __name__ == "__main__":
    init()
    run_bot()
