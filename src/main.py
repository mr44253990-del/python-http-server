import threading, time, json, urllib.request
from utils.db import init_db
from utils.telegram import send_message
from utils.transactions import add_deposit_request

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
                    
                    if 'callback_query' in u:
                        chat_id = u['callback_query']['message']['chat']['id']
                        cb_data = u['callback_query']['data']
                        if cb_data == 'balance':
                            send_message(chat_id, "আপনার ব্যালেন্স: 0.00 BDT")
                        elif cb_data == 'deposit':
                            send_message(chat_id, "বিকাশ করুন: 01755070708\nএরপর TRX ID পাঠান এভাবে: /deposit [amount] [trxid]")
                    
                    elif 'message' in u and 'text' in u['message']:
                        text = u['message']['text']
                        chat_id = u['message']['chat']['id']
                        if text == '/start':
                            send_message(chat_id, "স্বাগতম! মেনু সিলেক্ট করুন:", [[{"text":"💰 ব্যালেন্স", "callback_data":"balance"}, {"text":"➕ Deposit", "callback_data":"deposit"}]])
                        elif text.startswith('/deposit'):
                            parts = text.split()
                            if len(parts) == 3:
                                _, amount, trx = parts
                                if add_deposit_request(chat_id, amount, trx):
                                    send_message(chat_id, f"আপনার ডিপোজিট রিকোয়েস্ট জমা হয়েছে! TRX: {trx}. এডমিন চেক করছেন।")
                                else:
                                    send_message(chat_id, "এরর: TRX ID টি সম্ভবত আগেই ব্যবহৃত হয়েছে।")
            time.sleep(2)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler).serve_forever()
