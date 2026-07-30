import time
from datetime import datetime, timezone, timedelta

from checker import check_player
from notifier import send_message
from config import UID
from firebase import get_player, save_player, add_history


def now():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")


def time_diff(start, end):
    if not start:
        return 0

    fmt = "%Y-%m-%d %H:%M:%S"

    try:
        start_time = datetime.strptime(start, fmt)
        end_time = datetime.strptime(end, fmt)
        return int((end_time - start_time).total_seconds())
    except Exception as e:
        print("Time calculation error:", e)
        return 0


while True:

    try:

        print("=" * 50)
        print(f"Time : {now()}")
        print(f"UID  : {UID}")
        print("Checking player...")
        print("=" * 50)

        status = check_player(UID)

        print("DEBUG STATUS:", status)

        player = get_player(UID)

        if player:
            previous = player.get("status", "offline")
        else:
            previous = "offline"

        # ==========================
        # ONLINE
        # ==========================

        if status is True:

            print("Status : ONLINE")

            if previous != "online":

                old_sessions = 0

                if player:
                    old_sessions = player.get("total_sessions", 0)

                new_session = old_sessions + 1

                send_message(
f"""🟢 FREE FIRE ALERT

Player: {UID}

Status: ONLINE ✅

Time:
{now()}

Session:
{new_session}
"""
                )

                add_history(UID, "online")

                save_player(
                    UID,
                    {
                        "uid": UID,
                        "status": "online",
                        "online_since": now(),
                        "offline_since": "",
                        "last_checked": now(),
                        "total_sessions": new_session,
                        "total_online_seconds": player.get("total_online_seconds", 0) if player else 0
                    }
                )

            else:

                save_player(
                    UID,
                    {
                        "last_checked": now()
                    }
                )

        # ==========================
        # OFFLINE
        # ==========================

        elif status is False:

            print("Status : OFFLINE")

            sessions = 0
            old_total = 0
            played_seconds = 0

            if player:

                sessions = player.get("total_sessions", 0)
                old_total = player.get("total_online_seconds", 0)

                if previous == "online":

                    played_seconds = time_diff(
                        player.get("online_since"),
                        now()
                    )

            new_total = old_total + played_seconds

            if previous == "online":

                minutes = played_seconds // 60
                seconds = played_seconds % 60

                send_message(
f"""🔴 FREE FIRE ALERT

Player: {UID}

Status: OFFLINE ❌

Played this session:
{minutes}m {seconds}s

Total Play Time:
{new_total // 3600}h {(new_total % 3600) // 60}m

Time:
{now()}
"""
                )

                add_history(UID, "offline")

            save_player(
                UID,
                {
                    "uid": UID,
                    "status": "offline",
                    "offline_since": now(),
                    "last_checked": now(),
                    "total_sessions": sessions,
                    "total_online_seconds": new_total
                }
            )

        else:

            print("Status : UNKNOWN")

    except Exception as e:

        print("ERROR:", e)

    print("=" * 50)
    print("Sleeping for 2 minutes...")
    print("=" * 50)

    time.sleep(120)