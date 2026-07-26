from checker import check_player
from notifier import send_message
from config import UID
from firebase import get_player, save_player, add_history
from datetime import datetime, timezone, timedelta


def now():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")


print("=" * 50)
print(f"Time   : {now()}")
print(f"UID    : {UID}")
print("Checking player...")
print("=" * 50)


status = check_player(UID)

print("DEBUG STATUS:", status)

# Get previous status from Firebase
player_data = get_player(UID)

if player_data:
    previous = player_data.get("status")
else:
    previous = "offline"


# PLAYER ONLINE
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

        add_history(UID, "online")

    save_player(UID, {
        "uid": UID,
        "status": "online",
        "last_seen": now()
    })


# PLAYER OFFLINE
elif status is False:

    print("Status : OFFLINE")

    if previous == "online":

        print("Sending offline notification...")

        send_message(
            f"""🔴 FREE FIRE ALERT

Player: {UID}

Status: OFFLINE ❌

Time: {now()}
"""
        )

        add_history(UID, "offline")


    save_player(UID, {
        "uid": UID,
        "status": "offline",
        "last_seen": now()
    })


# UNKNOWN
else:
    print("Status : UNKNOWN")


print("=" * 50)