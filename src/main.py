import threading, time, json, urllib.request
from utils.db import init_db
from utils.telegram import send_message
from utils.transactions import add_deposit_request
from admin.panel import get_pending_deposits, approve_deposit

init_db()
ADMIN_ID = 5893363292 # আপনার টেলিগ্রাম আইডি এখানে দিন যাতে শুধু আপনিই অ্যাক্সেস পান

def bot_loop():
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4/getUpdates?offset={last_update_id + 1}"
            with urllib.request.urlopen(url, timeout=10) as res:
                data = json.loads(res.read().decode())
                for u in data.get('result', []):
                    last_update_id = u['update_id']
                    if 'message' in u and 'text' in u['message']:
                        text = u['message']['text']
                        chat_id = u['message']['chat']['id']
                        
                        # Admin commands
                        if text == '/admin' and chat_id == ADMIN_ID:
                            pendings = get_pending_deposits()
                            if not pendings: send_message(chat_id, "কোনো পেন্ডিং রিকোয়েস্ট নেই।")
                            else:
                                for p in pendings:
                                    msg = f"ID:{p[0]} | User:{p[1]} | Amount:{p[2]} | TRX:{p[3]}"
                                    send_message(chat_id, msg, [[{"text":"✅ Approve", "callback_data":f"app_{p[0]}"}]])
                        
                        # User commands
                        elif text.startswith('/deposit'):
                            parts = text.split()
                            if len(parts) == 3:
                                if add_deposit_request(chat_id, parts[1], parts[2]):
                                    send_message(chat_id, "রিকোয়েস্ট সফল হয়েছে!")
                                else:
                                    send_message(chat_id, "ত্রুটি: TRX ID ইতিমধ্যে ব্যবহৃত!")
                    
                    elif 'callback_query' in u:
                        chat_id = u['callback_query']['message']['chat']['id']
                        cb = u['callback_query']['data']
                        if cb.startswith('app_') and chat_id == ADMIN_ID:
                            tx_id = cb.split('_')[1]
                            approve_deposit(tx_id)
                            send_message(chat_id, f"ট্রানজ্যাকশন {tx_id} অনুমোদিত!")
            time.sleep(2)
        except Exception: time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler).serve_forever()
