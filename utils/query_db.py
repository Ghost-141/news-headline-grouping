import mysql.connector
import json
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="news_automation"
)
cursor = conn.cursor(dictionary=True)


def get_all_news():
    """Get all news with id, title, publish time, and source"""
    try:
        sql = "SELECT id, title, publish_time, source FROM news ORDER BY id DESC"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []


def display_news():
    """Display all news in a formatted table"""
    news = get_all_news()

    if not news:
        print("No news found in database")
        return

    # print(f"\n{'ID':<5} {'Title':<60} {'Published Time':<20} {'Source':<15}")
    # print("=" * 100)

    # for item in news:
    #     title = item["title"][:57] + "..." if len(item["title"]) > 60 else item["title"]
    #     print(
    #         f"{item['id']:<5} {title:<60} {item['publish_time']:<20} {item['source']:<15}"
    #     )

    print(f"\nTotal: {len(news)} news items")


def save_to_json():
    """Save all news to a JSON file"""
    news = get_all_news()

    if not news:
        print("No news found to save")
        return

    filename = f"news_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(news)} news items to {filename}")


if __name__ == "__main__":
    display_news()
    save_to_json()
