import requests
import os
from dotenv import load_dotenv

# Load token from .env file in the same directory (optional but good practice)
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    # If .env fails, manually paste your token here
    BOT_TOKEN = "7632492614:AAGnWzosjBXfmBVkJtMhH8ywFtOXqVhq144" # <--- PASTE TOKEN HERE IF .env DOESN'T WORK

if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
     print("Error: Please replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token.")
else:
    # Construct the Telegram API URL to delete the webhook
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"

    try:
        response = requests.get(url)
        response_json = response.json()

        if response.status_code == 200 and response_json.get("ok"):
            print("Webhook successfully deleted!")
            print("Result:", response_json.get("description"))
        else:
            print("Failed to delete webhook.")
            print("Status Code:", response.status_code)
            print("Response:", response_json)

    except Exception as e:
        print(f"An error occurred: {e}")