import json, sqlite3, time, urllib.request, urllib.parse, os

def init():
    conn = sqlite3.connect('app.db', check_same_thread=False)
    conn.execute('CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, balance REAL DEFAULT 0, name TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, amount REAL, trx_id TEXT UNIQUE, status TEXT)')
    conn.commit()
    conn.close()

def send_msg(token, chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {'chat_id': chat_id, 'text': text}
    if keyboard: params['reply_markup'] = json.dumps({"inline_keyboard": keyboard})
    urllib.request.urlopen(f"{url}?{urllib.parse.urlencode(params)}")

def run_bot():
    token = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset + 1}"
            with urllib.request.urlopen(url, timeout=15) as res:
                data = json.loads(res.read().decode())
                for u in data.get('result', []):
                    offset = u['update_id']
                    if 'callback_query' in u:
                        cb = u['callback_query']
                        chat_id = cb['message']['chat']['id']
                        data = cb['data']
                        if data == 'balance': send_msg(token, chat_id, "আপনার ব্যালেন্স: 0.00 BDT")
                        elif data == 'deposit_info': send_msg(token, chat_id, "বিকাশ: 01755070708. টাকা পাঠিয়ে TRX ID জানান /deposit [amount] [trx]")
                    elif 'message' in u and u['message'].get('text') == '/start':
                        menu = [[{"text":"💰 ব্যালেন্স", "callback_data":"balance"}, {"text":"📥 ডিপোজিট", "callback_data":"deposit_info"}]]
                        send_msg(token, u['message']['chat']['id'], "স্বাগতম রাকিবুল! মেইন মেনু:", menu)
        except: time.sleep(10)

if __name__ == "__main__":
    init()
    run_bot()
