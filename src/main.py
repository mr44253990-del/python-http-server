import os
import json
import sqlite3
import threading
import telebot
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

init_db()

# টেলিগ্রাম বট লজিক
def start_bot(token):
    try:
        bot = telebot.TeleBot(token)
        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            bot.reply_to(message, f"Hello Rakibul! I am live. You said: {message.text}")
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")

class CustomHandler(SimpleHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/status':
            self._set_headers()
            self.wfile.write(json.dumps({"status": "running", "message": "Python app with Telegram Bot is active"}).encode('utf-8'))
        else:
            self._set_headers(404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/set-bot':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            token = data.get('token')
            
            # বট থ্রেড চালু করা
            threading.Thread(target=start_bot, args=(token,), daemon=True).start()
            
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "Bot initialization started!"}).encode('utf-8'))

if __name__ == "__main__":
    # সরাসরি আপনার দেওয়া টোকেনটি দিয়ে বট অটোমেটিক চালু করে দিচ্ছি
    TOKEN = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    threading.Thread(target=start_bot, args=(TOKEN,), daemon=True).start()
    
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer((host, port), CustomHandler)
    print(f"Server running at http://{host}:{port}")
    server.serve_forever()
