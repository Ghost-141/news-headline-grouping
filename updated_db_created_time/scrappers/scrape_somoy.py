from selenium.webdriver.common.by import By
from scrappers.chrome_driver import (
    get_chrome_driver,
    wait_for_elements,
    get_element_text,
    get_element_attribute,
)
from utils.db import save_to_db
from utils.news_detector import is_breaking_news
import time


def get_full_content(driver, url):
    try:
        driver.get(url)
        time.sleep(2)

        selectors = [
            "div.news-paragraph",
            "div.body-content",
            "div.news-details",
            "div.details",
            "article",
            "div.row.ma-0",
        ]

        paragraphs = []
        for selector in selectors:
            try:
                if selector == "div.news-paragraph":
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for el in elements:
                        text = el.text.strip()
                        if text:
                            paragraphs.append(text)
                else:
                    container = driver.find_element(By.CSS_SELECTOR, selector)
                    p_tags = container.find_elements(By.TAG_NAME, "p")
                    for p in p_tags:
                        text = p.text.strip()
                        if text:
                            paragraphs.append(text)
            except:
                continue

        return "\n\n".join(paragraphs)
    except Exception as e:
        print("FULL CONTENT ERROR:", e)
        return ""


def scrape_somoy():
    driver = get_chrome_driver(headless=True)
    seen_titles = set()

    try:
        driver.get("https://www.somoynews.tv/read/recent")
        time.sleep(3)

        items = wait_for_elements(driver, "div.row", timeout=30)
        print(f"Found {len(items)} potential news items")

        for item in items:
            try:
                title = get_element_text(item, "h2, h3")
                if not title or title in seen_titles:
                    continue

                category = get_element_text(item, "h4")
                publish_time = get_element_text(item, "span.text-caption")

                if not category or not publish_time:
                    continue

                seen_titles.add(title)
                subtitle = get_element_text(item, "h3.simple-card-3-subtitle")

                link = get_element_attribute(item, "a", "href")
                if link and not link.startswith("http"):
                    link = "https://www.somoynews.tv" + link

                print(f"\nProcessing: {title}")

                save_to_db(
                    source="Somoy TV",
                    title=title,
                    summary=subtitle,
                    category=category,
                    link=link,
                    publish_time=publish_time
                )

                time.sleep(1)
            except Exception as e:
                print("Item Error:", e)

    finally:
        driver.quit()

    print(f"\n✅ Saved Somoy TV news to database")


if __name__ == "__main__":
    scrape_somoy()
