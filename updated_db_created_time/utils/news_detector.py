import logging
import re
from datetime import datetime
from utils.db import cursor, conn
from is_break import is_breaking_news

logging.basicConfig(level=logging.INFO)


BREAKING_KEYWORDS = [
    "হত্যা",
    "দুর্ঘটনা",
    "প্রাণ",
    "মৃত্যু",
    "মৃতদেহ",
    "ধর্ষণ",
    "আগুন",
    "বিস্ফোরণ",
    "ভূমিকম্প",
    "রাজনৈতিক সহিংসতা",
    "নির্বাচন",
    "ভোট",
    "রাষ্ট্রপতি",
    "গ্রেফতার",
    "মোতায়েন",
    "অবরোধ",
    "বিক্ষোভ",
    "ধাওয়া–পাল্টাধাওয়া",
    "নিরাপত্তা",
    "রিমান্ড",
    "প্রদর্শন",
    "ঘোষণা",
    "বন্যা",
    "ঝড়",
    "জরুরি",
    "বিল পাস",
    "রায়",
    "গুরুতর আহত",
    "খুন",
    "অপহরণ",
    "সংঘর্ষ",
    "মৃত",
    "মহাসড়ক",
]


def process_pending_news():
    """Query pending news, check breaking status, and update database"""

    try:
        print("\n🔍 Fetching pending news...")
        sql = "SELECT id, title, publish_time FROM news WHERE pending = 0 AND DATE(created_at) = CURDATE()"
        cursor.execute(sql)
        pending_news = cursor.fetchall()
        print(f"📊 Found {len(pending_news)} pending news items for today")  # type: ignore

        breaking_count = 0
        for i, news in enumerate(pending_news, 1):  # type: ignore
            print(f"\n[{i}/{len(pending_news)}] Processing: {news['title'][:20]}...")  # type: ignore

            time = news["publish_time"]

            if not re.match(r"^\d+\s*মিনিট(ে| আগে)?", time):
                print(f"{i:2d}. ⏭️ SKIPPED | {news['title'[:10]]}... (Time: {news['publish_time']})")
                continue
            try:  
                breaking_status = is_breaking_news(news["title"], threshold=0.85)
                if breaking_status:
                    breaking_count += 1
                    print(f"🚨 BREAKING NEWS detected!")
                else:
                    print(f"📰 Regular news")    
            except Exception as e:
                print(f"{i:2d}. ⚠️ ERROR processing title: {news['title'[:30]]}... | {e}")   

            update_sql = "UPDATE news SET is_breaking = %s, pending = 1 WHERE id = %s"
            cursor.execute(update_sql, (breaking_status, news["id"]))

        conn.commit()
        print(f"\n✅ Processing complete: {breaking_count} breaking news out of {len(pending_news)} total")  # type: ignore

    except Exception as e:
        logging.error(f"Error processing pending news: {e}")
        conn.rollback()
        print(f"❌ Error occurred: {e}")
