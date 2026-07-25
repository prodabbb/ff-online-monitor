from playwright.sync_api import sync_playwright, TimeoutError
from config import UID, URL


def check_player():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        )

        try:
            print("Opening website...")

            page.goto(URL, timeout=60000)

            page.wait_for_selector("#idsonline_input", timeout=30000)

            print("Entering UID...")

            page.fill("#idsonline_input", UID)

            page.click("#idsonline_submit")

            print("Waiting for result...")

            page.wait_for_selector(
                f'a[href*="{UID}"]',
                timeout=45000,
            )

            result = page.locator(
                f'a[href*="{UID}"]'
            ).first.evaluate(
                "el => el.parentElement.innerText"
            )

            print(result)

            text = result.lower()

            if "not online" in text:
                return False

            if "is online" in text:
                return True

            return None

        except TimeoutError:
            print("Timeout while loading page or waiting for result.")
            page.screenshot(path="error.png")
            print("Screenshot saved as error.png")
            return None

        finally:
            browser.close()