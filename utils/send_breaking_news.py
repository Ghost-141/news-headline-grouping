from utils.db import get_pending_breaking_news, update_sent_status
from utils.send_message import send_whatsapp
import datetime


def send_breaking_news():
    """Send pending breaking news to WhatsApp and update sent status"""
    breaking_news_list = get_pending_breaking_news()

    if not breaking_news_list:
        print("No unsent breaking news found.")
        return

    print(f"Found {len(breaking_news_list)} unsent breaking news.")

    for news in breaking_news_list:
        # Format news data for WhatsApp
        news_data = {
            "title": news["title"],
            "source": news["source"],
            "link": news["link"],
            "publish_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Send to WhatsApp
        if send_whatsapp(news_data):
            # Update sent status if successful
            if update_sent_status(news["id"]):
                print(f"✅ Sent and updated: {news['title'][:20]}...")
            else:
                print(f"❌ Sent but failed to update status: {news['title'][:20]}...")
        else:
            print(f"❌ Failed to send: {news['title'][:50]}...")


# if __name__ == "__main__":
#     send_breaking_news()
