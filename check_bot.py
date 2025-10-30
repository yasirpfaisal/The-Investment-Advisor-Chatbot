import requests
import os
from dotenv import load_dotenv

# Load token from .env file in the same directory
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("ERROR: Could not find TELEGRAM_BOT_TOKEN in your .env file.")
else:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    print(f"Checking bot token ending in: ...{BOT_TOKEN[-5:]}")

    try:
        response = requests.get(url)
        data = response.json()

        if not data.get("ok"):
            print("\n--- 🔴 ERROR ---")
            print("Your TELEGRAM_BOT_TOKEN is INVALID. Telegram rejected it.")
            print(f"Error {data.get('error_code')}: {data.get('description')}")

        else:
            print("\n--- ✅ SUCCESS ---")
            print("Your TELEGRAM_BOT_TOKEN is VALID.")

            if data['result'].get('url'):
                print("\n--- ⚠️ WARNING: WEBHOOK IS SET! ---")
                print(f"A webhook is active and pointing to: {data['result']['url']}")
                print("This is the problem. Run your `clear_webhook.py` script again.")
            else:
                print("\n--- ✅ GOOD NEWS: NO WEBHOOK IS SET ---")
                print("Your bot is correctly configured for polling.")

    except Exception as e:
        print(f"An error occurred: {e}")