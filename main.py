import os, json, sqlite3, threading, time, urllib.request, urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

# --- Simple Database ---
def init():
    conn = sqlite3.connect('app.db', check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE, balance REAL DEFAULT 0)')
    conn.commit()
    conn.close()

# --- Telegram Bot Engine ---
def run_bot():
    token = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset + 1}"
            with urllib.request.urlopen(url, timeout=10) as res:
                data = json.loads(res.read().decode())
                if data.get('result'):
                    for u in data['result']:
                        offset = u['update_id']
                        if 'message' in u and 'chat' in u['message']:
                            chat_id = u['message']['chat']['id']
                            reply_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=Bot is active and running!"
                            urllib.request.urlopen(reply_url)
        except: time.sleep(5)

# --- Server to keep alive ---
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is active")

if __name__ == "__main__":
    init()
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 8000))
    HTTPServer(('', port), Handler).serve_forever()
