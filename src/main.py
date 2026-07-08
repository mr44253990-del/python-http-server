import os
import json
import sqlite3
import threading
import time
import urllib.request
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# ডাটাবেস সেটআপ
def init_db():
    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

init_db()

# লাইব্রেরি ছাড়া টেলিগ্রাম বট লজিক
def run_simple_bot(token):
    last_update_id = 0
    base_url = f"https://api.telegram.org/bot{token}/"
    while True:
        try:
            url = f"{base_url}getUpdates?offset={last_update_id + 1}"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                if data.get('ok') and data.get('result'):
                    for update in data['result']:
                        last_update_id = update['update_id']
                        if 'message' in update:
                            chat_id = update['message']['chat']['id']
                            text = update['message'].get('text', '')
                            reply_text = f"Hello Rakibul! I am live. You said: {text}"
                            encoded_reply = urllib.parse.quote(reply_text)
                            send_url = f"{base_url}sendMessage?chat_id={chat_id}&text={encoded_reply}"
                            urllib.request.urlopen(send_url, timeout=10)
            time.sleep(2)
        except Exception:
            time.sleep(5)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # রুট পাথের জন্য রেসপন্স
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Server is Running!</h1><p>Check <a href='/status'>/status</a> for API info.</p>")
        
        # /status পাথের জন্য রেসপন্স
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "running", "bot_method": "native_urllib"}).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    TOKEN = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    threading.Thread(target=run_simple_bot, args=(TOKEN,), daemon=True).start()
    
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    print(f"Server starting on {host}:{port}")
    server = HTTPServer((host, port), CustomHandler)
    server.serve_forever()
