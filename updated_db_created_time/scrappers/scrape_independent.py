from selenium.webdriver.common.by import By
from scrappers.chrome_driver import get_chrome_driver
from utils.db import save_to_db
from utils.news_detector import is_breaking_news
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time


def scrape_independent():
    driver = get_chrome_driver(headless=True)

    try:
        MAIN_URL = "https://www.itvbd.com/country"
        driver.get(MAIN_URL)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "lxml")
        article_blocks = soup.select("div.each.col_in")
        articles_data = []

        for block in article_blocks:
            try:
                a_tag = block.select_one("h2.title a")
                if not a_tag:
                    continue

                title = a_tag.get_text(strip=True)
                href = a_tag.get("href")

                if href.startswith("//"):  # type: ignore
                    href = "https:" + href  # type: ignore
                elif href.startswith("/"):  # type: ignore
                    href = "https://www.itvbd.com" + href  # type: ignore

                href = unquote(href)  # type: ignore

                time_span = block.select_one(".additional .time")
                publish_time = time_span.get_text(strip=True) if time_span else ""

                articles_data.append(
                    {
                        "title": title,
                        "publish_time": publish_time,
                        "link": href,
                    }
                )
            except:
                continue

        print(f"Found {len(articles_data)} articles")

        for item in articles_data:
            print(f"\nProcessing: {item['title']}")
            try:
                link_element = driver.find_element(By.LINK_TEXT, item["title"])
                driver.execute_script("arguments[0].click();", link_element)
                time.sleep(1)

                soup_article = BeautifulSoup(driver.page_source, "lxml")
                paragraphs = soup_article.select(".content_details p")
                summary = "\n".join([p.get_text(strip=True) for p in paragraphs])

                save_to_db(
                    source="Independent TV",
                    title=item["title"],
                    summary=summary,
                    category="",
                    link=item["link"],
                    publish_time=item["publish_time"]
                )

                # print(f"Saved: {item['title']}")
                driver.back()
                time.sleep(1)

            except Exception as e:
                print(f"Failed: {e}")
                driver.get(MAIN_URL)
                time.sleep(1)
                continue

    finally:
        driver.quit()

    print(f"\n✅ Saved Independent TV news to database")


if __name__ == "__main__":
    scrape_independent()
