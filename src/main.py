import os
import json
import sqlite3
import threading
import sys

# Try to import telebot, handle if not present
try:
    import telebot
    TELEBOT_AVAILABLE = True
except ImportError:
    TELEBOT_AVAILABLE = False

# Database setup
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

def start_bot(token):
    if not TELEBOT_AVAILABLE:
        print("Error: pyTelegramBotAPI not installed.")
        return
    try:
        bot = telebot.TeleBot(token)
        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            bot.reply_to(message, f"Hello Rakibul! I am live. You said: {message.text}")
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

class CustomHandler(SimpleHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/status':
            self._set_headers()
            self.wfile.write(json.dumps({"status": "running", "bot_ready": TELEBOT_AVAILABLE}).encode('utf-8'))
        else:
            self._set_headers(404)

if __name__ == "__main__":
    TOKEN = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    if TELEBOT_AVAILABLE:
        threading.Thread(target=start_bot, args=(TOKEN,), daemon=True).start()
    
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    print(f"Server starting on {host}:{port}")
    server = HTTPServer((host, port), CustomHandler)
    server.serve_forever()
