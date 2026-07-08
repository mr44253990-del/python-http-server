import urllib.request, urllib.parse, json
TOKEN = "8262466024:AAG4yoZE5ynR0spQ39iWrAlcOq3fX7trtj4"

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if keyboard: payload["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    urllib.request.urlopen(url, data=urllib.parse.urlencode(payload).encode())
