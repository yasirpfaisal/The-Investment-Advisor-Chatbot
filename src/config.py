import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

#OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Validation ---
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is not set in the environment.")
if not TELEGRAM_BOT_TOKEN:
    print("Warning: TELEGRAM_BOT_TOKEN is not set in the environment.")