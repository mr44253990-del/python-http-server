import threading, time, json, urllib.request
from utils.db import init_db, get_db
from utils.telegram import send_message

init_db()

def bot_loop():
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4/getUpdates?offset={last_update_id + 1}"
            with urllib.request.urlopen(url, timeout=10) as res:
                data = json.loads(res.read().decode())
                for u in data.get('result', []):
                    last_update_id = u['update_id']
                    # Callback logic
                    if 'callback_query' in u:
                        chat_id = u['callback_query']['message']['chat']['id']
                        if u['callback_query']['data'] == 'balance':
                            send_message(chat_id, "আপনার ব্যালেন্স: 0.00 BDT")
                    # Command logic
                    elif 'message' in u and u['message'].get('text') == '/start':
                        send_message(u['message']['chat']['id'], "স্বাগতম! মেনু সিলেক্ট করুন:", [[{"text":"💰 ব্যালেন্স", "callback_data":"balance"}]])
            time.sleep(2)
        except: time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler).serve_forever()
