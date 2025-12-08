from selenium.webdriver.common.by import By
from scrappers.chrome_driver import get_chrome_driver
from scrappers.utils import save_to_db
from detector import is_breaking_news
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
import json

BASE_URL = "https://www.channel24bd.tv/"


def extract_article_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Extract title from meta tag or h1
    title_meta = soup.find("meta", property="og:title")
    title = title_meta["content"] if title_meta else ""
    if not title:
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

    # Extract description from meta tag
    desc_meta = soup.find("meta", property="og:description")
    description = desc_meta["content"] if desc_meta else ""

    # Extract publish time from JSON-LD
    publish_time = ""
    json_ld_scripts = soup.find_all("script", type="application/ld+json")
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                publish_time = data.get("dateCreated") or data.get("datePublished", "")
                if publish_time:
                    break
        except:
            pass

    return {
        "title": title or "",
        "description": description or "",
        "publish_time": publish_time or "",
    }


def scrape_channel24():
    driver = get_chrome_driver(headless=True)

    try:
        driver.get(BASE_URL)
        time.sleep(2)

        scroll_floating_tab(driver)
        links = scrape_latest_tab(driver)
        print(f"Found {len(links)} articles")

        for link in links:
            scrape_article(driver, link["url"], link["title"])
            time.sleep(0.5)

    finally:
        driver.quit()

    print(f"\n✅ Saved news items to database")


def scroll_floating_tab(driver, max_scrolls=10):
    for _ in range(max_scrolls):
        driver.execute_script(
            "const tab = document.querySelector('#tabs-1'); if (tab) tab.scrollBy(0, tab.scrollHeight);"
        )
        time.sleep(0.5)


def scrape_latest_tab(driver):
    results = []
    elements = driver.find_elements(By.CSS_SELECTOR, "#tabs-1 a")

    for el in elements:
        try:
            title = el.text.strip()
            href = el.get_attribute("href")

            if not href or len(title) < 10:
                continue

            if href.startswith("/"):
                href = BASE_URL.rstrip("/") + href
            href = unquote(href)

            results.append({"title": title, "url": href})
        except:
            continue

    return results


def scrape_article(driver, url):
    try:
        driver.get(url)
        time.sleep(1)

        html = driver.page_source
        data = extract_article_data(html)

        print(f"Processing: {data['title']}")

        is_breaking = is_breaking_news(
            data["title"], data["description"], data["publish_time"]
        )

        save_to_db(
            source="Channel 24",
            title=data["title"],
            summary=data["description"],
            category="",
            link=url,
            publish_time=data["publish_time"],
            is_breaking=is_breaking,
        )

        driver.back()
        time.sleep(1)

    except Exception as e:
        print(f"Failed: {e}")
        driver.get(BASE_URL)
        time.sleep(1)


if __name__ == "__main__":
    scrape_channel24()
