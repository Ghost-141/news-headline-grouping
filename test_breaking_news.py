import json
from datetime import datetime
from breaking_news_detector import is_breaking_news


def test_breaking_news():
    """Test is_breaking_news function against latest_news.json"""

    try:
        with open("somoy_news.json", "r", encoding="utf-8") as f:
            news_data = json.load(f)
    except FileNotFoundError:
        print("❌ latest_news.json not found!")
        return
    except json.JSONDecodeError:
        print("❌ Invalid JSON format in latest_news.json!")
        return

    print("🔍 Testing Breaking News Detection")
    print("=" * 50)

    breaking_count = 0
    total_count = len(news_data)
    breaking_news = []

    for i, news in enumerate(news_data, 1):
        title = news.get("title", "")
        summary = news.get("summarized_description", "")
        publish_time = news.get("published_time", "")

        is_breaking = is_breaking_news(title, summary, publish_time)

        status = "🚨 BREAKING" if is_breaking else "📰 Regular"
        print(f"{i:2d}. {status} | {title[:60]}...")

        if is_breaking:
            breaking_count += 1
            breaking_news.append(news)

    # Save breaking news to file
    with open("detected_breaking_news.txt", "w", encoding="utf-8") as f:
        f.write(f"Breaking News Detection Results\n")
        f.write(
            f"Generated: {json.dumps(news_data[0].get('created_at', 'Unknown'), ensure_ascii=False) if news_data else 'Unknown'}\n"
        )
        f.write(f"Total: {breaking_count}/{total_count} breaking news\n\n")

        for i, news in enumerate(breaking_news, 1):
            f.write(f"{i}. {news.get('title', '')}\n")
            f.write(f"   Source: {news.get('source', '')}\n")
            f.write(f"   Link: {news.get('link', '')}\n")
            f.write(f"   Time: {news.get('publish_time', '')}\n\n")

    print("=" * 50)
    print(f"📊 Results: {breaking_count}/{total_count} breaking news detected")
    print(f"📈 Breaking news ratio: {(breaking_count/total_count)*100:.1f}%")
    print(f"💾 Breaking news saved to: detected_breaking_news.txt")


if __name__ == "__main__":
    test_breaking_news()
