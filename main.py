import json, sqlite3, time, urllib.request, urllib.parse, os

# --- Database Setup ---
def init():
    try:
        conn = sqlite3.connect('app.db', check_same_thread=False)
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE, balance REAL DEFAULT 0)')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

# --- Bot Engine ---
def run_bot():
    token = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    offset = 0
    print("Bot engine initialized...")
    
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
                            
                            # Reply
                            reply = f"Hello! Your ID is {chat_id}. Bot is active and running."
                            send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                            params = urllib.parse.urlencode({'chat_id': chat_id, 'text': reply})
                            urllib.request.urlopen(f"{send_url}?{params}", timeout=15)
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    init()
    run_bot()
