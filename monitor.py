from checker import check_player
from notifier import send_message
from config import UID
from datetime import datetime

STATUS_FILE = "status.txt"


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_last_status():
    try:
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "offline"


def save_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)


print("=" * 50)
print(f"Time   : {now()}")
print(f"UID    : {UID}")
print("Checking player...")
print("=" * 50)

status = check_player()
print(f"Returned status: {status}")
previous = get_last_status()

if status is True:
    print("Status : ONLINE")

    if previous != "online":
        print("Sending Telegram notification...")

        send_message(
            f"""🟢 FREE FIRE ALERT

Player: {UID}

Status: ONLINE ✅

Time: {now()}
"""
        )

        save_status("online")
        print("Done!")

elif status is False:
    print("Status : OFFLINE")
    save_status("offline")

else:
    print("Status : UNKNOWN")

print("=" * 50)