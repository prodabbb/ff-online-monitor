from playwright.sync_api import sync_playwright
from config import UID, URL


def check_player():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, wait_until="networkidle")

        page.fill("#idsonline_input", UID)

        page.click("#idsonline_submit")

        page.wait_for_selector(
            f'a[href*="{UID}"]',
            timeout=30000
        )

        result = page.locator(
            f'a[href*="{UID}"]'
        ).first.evaluate(
            "el => el.parentElement.innerText"
        )

        browser.close()

        text = result.lower()

        if "not online" in text:
            return False

        if "is online" in text:
            return True

        return None