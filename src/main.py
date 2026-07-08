import os, json, sqlite3, threading, time, urllib.request, urllib.parse
from datetime import datetime

# DB Connection
def db_query(query, params=()):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    res = cursor.fetchall()
    conn.commit()
    conn.close()
    return res

# Initialize DB
db_query('CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, username TEXT, full_name TEXT, balance REAL DEFAULT 0.00, status TEXT DEFAULT "Active", reg_date TEXT)')
db_query('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, type TEXT, amount REAL, trx_id TEXT, status TEXT, timestamp TEXT)')

def send_telegram(token, chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    if reply_markup: data["reply_markup"] = json.dumps(reply_markup)
    urllib.request.urlopen(url, data=urllib.parse.urlencode(data).encode())

def run_bot(token):
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}"
            with urllib.request.urlopen(url, timeout=10) as response:
                updates = json.loads(response.read().decode())
                for u in updates.get('result', []):
                    last_update_id = u['update_id']
                    msg = u.get('message', {})
                    chat_id = msg.get('chat', {}).get('id')
                    text = msg.get('text', '')
                    
                    if text == '/start':
                        # Register User
                        user = db_query('SELECT * FROM users WHERE telegram_id=?', (chat_id,))
                        if not user:
                            db_query('INSERT INTO users (telegram_id, username, full_name, reg_date) VALUES (?,?,?,?)', 
                                     (chat_id, msg.get('from',{}).get('username'), msg.get('from',{}).get('first_name'), datetime.now().strftime('%Y-%m-%d')))
                        
                        user = db_query('SELECT * FROM users WHERE telegram_id=?', (chat_id,))[0]
                        reply = f"স্বাগতম {user[2]}!\n\nID: {user[0]}\nBalance: {user[3]:.2f} BDT\nStatus: {user[4]}"
                        send_telegram(token, chat_id, reply, {"inline_keyboard": [[{"text":"💰 Balance", "callback_data":"balance"},{"text":"➕ Deposit", "callback_data":"deposit"}]]})
            time.sleep(2)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot, args=("8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4",), daemon=True).start()
    # Web server to keep it alive
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    HTTPServer((os.environ.get('HOST', '127.0.0.1'), int(os.environ.get('PORT', 8000))), SimpleHTTPRequestHandler).serve_forever()
