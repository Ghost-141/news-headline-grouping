from selenium.webdriver.common.by import By
from scrappers.chrome_driver import (
    get_chrome_driver,
    wait_for_elements,
    get_element_text,
    get_element_attribute,
)
from utils.db import save_to_db
from scrappers.detector import is_breaking_news
import time
import random


def extract_summary_from_item(item):
    """Extract summary from listing item"""
    summary_selectors = [
        "p.desktopSummary",
        "p.summary",
        "div.summary",
        "div[class*='summary']",
        "p[class*='desc']",
    ]
    for sel in summary_selectors:
        text = get_element_text(item, sel)
        if text and len(text) > 20:
            return text
    return ""


def scrape_jamuna():
    driver = get_chrome_driver(headless=True)

    try:
        driver.get("https://jamuna.tv/latest")
        time.sleep(random.uniform(3, 5))

        items = wait_for_elements(driver, "div.desktopSectionLead")

        for item in items:
            try:
                title = get_element_text(item, "h1", By.TAG_NAME)
                link = get_element_attribute(item, "a.linkOverlay", "href")
                publish_time = get_element_text(item, "p.desktopTime")

                summary = extract_summary_from_item(item)

                is_breaking = is_breaking_news(title, summary, publish_time)

                save_to_db(
                    source="Jamuna TV",
                    title=title,
                    summary=summary,
                    category="",
                    link=link,
                    publish_time=publish_time,
                    is_breaking=is_breaking,
                )

                print(f"Scraped: {title}")

            except Exception as e:
                print(f"Error: {e}")
                continue

    finally:
        driver.quit()

    print(f"\n✅ Saved news items to database")


if __name__ == "__main__":
    scrape_jamuna()
