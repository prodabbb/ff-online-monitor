import requests
from bs4 import BeautifulSoup
import time


URL = "https://freefirejornal.com/freefire/online/checar.php"


def check_player(uid):

    print(text[:200])

    data = {
        "id": uid
    }

    print("Checking player...")

    for attempt in range(10):

        print(f"Attempt {attempt + 1}/10")

        try:
            response = requests.post(URL, data=data, timeout=15)

            # Convert HTML to readable text
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(" ").lower()

            print(text[:200])

            # Website is still processing
            if "aguarde" in text:
                print("Waiting for result...")
                time.sleep(3)
                continue


            # ONLINE detection
            if (
                "has been online" in text
                or "is online" in text
                or ("jogador" in text and "online" in text)
                or "esteve online" in text
                or "tem estado online" in text
            ):
                print("Player is ONLINE")
                return True


            # OFFLINE detection
            if (
                "is not online" in text
                or "não está online" in text
                or "nao esta online" in text
                or "not online" in text
            ):
                print("Player is OFFLINE")
                return False


            print("Unknown response")

        except Exception as e:
            print("Error:", e)

        time.sleep(3)


    print("No final result received")
    return None


if __name__ == "__main__":

    uid = "3178435469"

    status = check_player(uid)

    print("Status:", status)