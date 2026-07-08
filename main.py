import json, sqlite3, time, urllib.request, urllib.parse, os

def init():
    conn = sqlite3.connect('app.db', check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE, balance REAL DEFAULT 0)')
    conn.commit()
    conn.close()

def run_bot():
    token = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    offset = 0
    ADMIN_ID = 5893363292
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset + 1}"
            with urllib.request.urlopen(url, timeout=15) as res:
                data = json.loads(res.read().decode())
                if data.get('result'):
                    for u in data['result']:
                        offset = u['update_id']
                        if 'message' in u and 'chat' in u['message']:
                            chat_id = u['message']['chat']['id']
                            text = u['message'].get('text', '')
                            
                            # Admin Panel Logic
                            if text == '/admin' and chat_id == ADMIN_ID:
                                reply = "🛠️ Admin Panel Active:\n/pending - পেন্ডিং ডিপোজিট\n/stats - স্ট্যাটাস"
                            else:
                                reply = f"Hello! Your ID is {chat_id}. Bot is active."
                            
                            send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                            params = urllib.parse.urlencode({'chat_id': chat_id, 'text': reply})
                            urllib.request.urlopen(f"{send_url}?{params}", timeout=15)
        except: time.sleep(10)

if __name__ == "__main__":
    init()
    run_bot()
