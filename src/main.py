import os
import json
import sqlite3
import threading
import time
import urllib.request
import urllib.parse
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer

# ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, content TEXT, timestamp TEXT)')
    conn.commit()
    conn.close()

init_db()

# বট লজিক (নিরাপদ ও স্থিতিশীল সংস্করণ)
def run_bot(token):
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
                        if 'message' in update and 'text' in update['message']:
                            text = update['message']['text']
                            chat_id = update['message']['chat']['id']
                            
                            # লগিং
                            conn = sqlite3.connect('app.db')
                            conn.execute('INSERT INTO logs (content, timestamp) VALUES (?, ?)', (text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                            conn.commit()
                            conn.close()
                            
                            # QR কোড লিংকের জন্য Google Chart API ব্যবহার
                            qr_link = f"https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl={urllib.parse.quote(text)}"
                            reply_text = f"QR Code Generated:\n{qr_link}\n\nDetails:\nName: Rakibul\nDate: {datetime.now().strftime('%Y-%m-%d')}\nID: {chat_id}"
                            
                            send_url = f"{base_url}sendMessage?chat_id={chat_id}&text={urllib.parse.quote(reply_text)}"
                            urllib.request.urlopen(send_url, timeout=10)
            time.sleep(2)
        except Exception:
            time.sleep(5)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # রুট এবং অন্যান্য পাথের জন্য রেসপন্স
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "running", "message": "Server is healthy and bot is active"}).encode('utf-8'))

if __name__ == "__main__":
    TOKEN = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    # বট থ্রেড চালু করা
    threading.Thread(target=run_bot, args=(TOKEN,), daemon=True).start()
    
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer((host, port), CustomHandler)
    print(f"Starting server on {host}:{port}")
    server.serve_forever()
