from scrappers.scrape_jamuna import scrape_jamuna
from scrappers.scrape_somoy import scrape_somoy
from scrappers.scrape_independent import scrape_independent
from utils.send_breaking_news import send_breaking_news
from utils.news_detector import process_pending_news
import time


def scrape_all_news():
    """Run all news scrapers and save to database"""
    print("=" * 50)
    print("Starting news scraping...")
    print("=" * 50)

    try:
        print("\n[1/3] Scraping Jamuna TV...")
        scrape_jamuna()
        time.sleep(2)
    except Exception as e:
        print(f"Jamuna News scraping failed: {e}")

    try:
        print("\n[2/3] Scraping Somoy TV...")
        scrape_somoy()
        time.sleep(2)
    except Exception as e:
        print(f"Somoy TV scraping failed: {e}")

    try:
        print("\n[3/3] Scraping Indepentdent TV...")
        scrape_independent()
        time.sleep(2)
    except Exception as e:
        print(f"Independent TV scraping failed: {e}")

    print("\n" + "=" * 50)
    print("✅ All scraping completed!")
    print("=" * 50)


if __name__ == "__main__":
    scrape_all_news()
    process_pending_news()  # Check and update breaking news status
    send_breaking_news()  # Send breaking news to WhatsApp
