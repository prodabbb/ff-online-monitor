import requests
from config import BOT_TOKEN, CHAT_ID


def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    print(response.text)

    return response.json()


if __name__ == "__main__":
    send_message("🟢 TEST MESSAGE FROM FREE FIRE MONITOR")