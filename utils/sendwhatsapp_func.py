import requests
import time
import difflib
import re

# WhatsApp API Config
ULTRA_INSTANCE = "instance151894"
ULTRA_TOKEN = "d8uil7mglabcla3m"
GROUP_ID = "120363423977994258@g.us"

# ---------------------------------------------------------
# FUNCTION: SEND WHATSAPP MESSAGE
# ---------------------------------------------------------
def send_whatsapp(news):
   

    message = f"""
    {news}
    """

    url = f"https://api.ultramsg.com/{ULTRA_INSTANCE}/messages/chat"

    payload = {
        "token": ULTRA_TOKEN,
        "to": GROUP_ID,
        "body": message
    }

    try:
        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print("WhatsApp Sent Successfully!")
            return True
        else:
            print("WhatsApp API Error:", res.text)
            return False
    except Exception as e:
        print("Exception while sending WhatsApp:", e)
        return False
    
   