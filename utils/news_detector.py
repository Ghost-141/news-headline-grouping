import logging
import re
from utils.db import cursor, conn
from is_break import is_breaking_news
from utils.news_filter import filter_international_news


logging.basicConfig(level=logging.INFO)


def process_pending_news():
    """Query pending news, check breaking status, and update database"""

    try:
        print("\n🔍 Fetching pending news...")
        sql = "SELECT id, title, publish_time FROM news WHERE pending = 0"
        cursor.execute(sql)
        pending_news = cursor.fetchall()
        print(f"📊 Found {len(pending_news)} pending news items")  # type: ignore

        breaking_count = 0
        for i, news in enumerate(pending_news, 1):  # type: ignore
            print(f"\n[{i}/{len(pending_news)}] Processing: {news['title'][:40]}...")  # type: ignore

            time = news["publish_time"]

            if not re.match(r"^\d+\s*মিনিট(ে| আগে)?", time):
                print(f"{i:2d}. ⏭️ SKIPPED | {news['title'[:30]]}... (Time: {news['publish_time']})")
                continue
            breaking_status = 0
            try:  
                breaking_status = is_breaking_news(news["title"], threshold=0.85)
                if breaking_status:
                    global_news = filter_international_news(news["title"])
                    if not global_news:
                        breaking_count += 1
                        print(f"🚨 BREAKING NEWS detected!")
                    else:
                        print(f"📰 Regular news")
                        breaking_status = 0    
            except Exception as e:
                print(f"{i:2d}. ⚠️ ERROR processing title: {news['title'[:40]]}... | {e}")   
                breaking_status = 0

            update_sql = "UPDATE news SET is_breaking = %s, pending = 1 WHERE id = %s"
            cursor.execute(update_sql, (breaking_status, news["id"]))

        conn.commit()
        print(f"\n✅ Processing complete: {breaking_count} breaking news out of {len(pending_news)} total")  # type: ignore

    except Exception as e:
        logging.error(f"Error processing pending news: {e}")
        conn.rollback()
        print(f"❌ Error occurred: {e}")
