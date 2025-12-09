import requests
from dotenv import load_dotenv
import os

load_dotenv()

# WhatsApp API Config
ULTRA_INSTANCE = os.getenv("INSTANCE")
ULTRA_TOKEN = os.getenv("TOKEN")
GROUP_ID = os.getenv("ID")


def send_whatsapp(news: dict):

    message = f"""📰 *Breaking News*
    🏷️ *Title:* {news['title']}
    📺 *Source:* {news['source']}
    ⏰ *Published:* {news['publish_time']}
    🔗 *Read more:* {news['link']}
    """

    url = f"https://api.ultramsg.com/{ULTRA_INSTANCE}/messages/chat"

    payload = {"token": ULTRA_TOKEN, "to": GROUP_ID, "body": message}

    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print("Message Sent Successfully!")
            return True
        else:
            print("WhatsApp API Error:", res.text)
            return False
    except Exception as e:
        print("Error while sending WhatsApp Message:", e)
        return False
