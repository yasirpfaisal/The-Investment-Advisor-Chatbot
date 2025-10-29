import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.config import OPENAI_API_KEY, TELEGRAM_BOT_TOKEN
from src.rag_chain import create_rag_chain
import threading # Added for threading
import http.server # Added for the dummy web server
import socketserver # Added for the dummy web server
import time # Added for sleep

# --- 1. App Setup & Validation ---
print("Bot application starting...")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Check for API Keys
if not OPENAI_API_KEY:
    logger.error("FATAL: OPENAI_API_KEY not found.")
    raise ValueError("OPENAI_API_KEY is not set.")
if not TELEGRAM_BOT_TOKEN:
    logger.error("FATAL: TELEGRAM_BOT_TOKEN not found.")
    raise ValueError("TELEGRAM_BOT_TOKEN is not set.")

# --- Start Dummy Server Immediately ---
def run_dummy_server():
    """Runs a simple HTTP server on the port Render expects."""
    PORT = int(os.getenv("PORT", 10000)) # Render sets the PORT env var
    Handler = http.server.SimpleHTTPRequestHandler
    # Use 0.0.0.0 to bind to all available interfaces
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        logger.info(f"Dummy HTTP server starting on port {PORT}")
        httpd.serve_forever()

logger.info("Starting dummy HTTP server in a background thread...")
server_thread = threading.Thread(target=run_dummy_server)
server_thread.daemon = True # Allows the main program to exit even if this thread is running
server_thread.start()
time.sleep(2) # Give the server a couple of seconds to start and bind the port
# --- END NEW SECTION ---

# --- 2. Build the RAG Chain (Now happens *after* server starts) ---
logger.info("Building RAG chain... This may take a few minutes as knowledge is loaded.")
try:
    rag_chain = create_rag_chain()
    logger.info("RAG chain successfully built and in memory.")
except Exception as e:
    logger.error(f"Error building RAG chain: {e}")
    raise

# --- 3. Define Telegram Bot Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    logger.info(f"User {update.effective_user.username} started chat.")
    await update.message.reply_text(
        "Welcome! I am the Investment Philosopher Bot.\n\n"
        "I have studied the works of Warren Buffett and Ray Dalio. "
        "Ask me an investment question, and I will provide you with a synthesized "
        "analysis from both of their perspectives.\n\n"
        "Example: /ask What is your opinion on diversification?"
    )

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /ask command and processes the question."""
    if not context.args:
        # Fixed parse_mode issue here as well
        await update.message.reply_text("Please provide a question after the /ask command. \n\nExample: /ask What is market timing?", parse_mode=None)
        return

    question = ' '.join(context.args)
    logger.info(f"Received question from {update.effective_user.username}: {question}")
    await update.message.reply_text("Thinking... Retrieving and synthesizing a response. This may take a moment.")

    try:
        response = rag_chain.invoke(
            {"question": question},
            config={"configurable": {"session_id": str(update.effective_user.id)}}
        )

        # Fixed parse_mode issue for long messages
        if len(response) > 4096:
            logger.warning("Response is too long, splitting into multiple messages.")
            for i in range(0, len(response), 4096):
                await update.message.reply_text(response[i:i + 4096], parse_mode=None)
        # Fixed parse_mode issue for regular messages
        else:
            await update.message.reply_text(response, parse_mode=None)

    except Exception as e:
        logger.error(f"Error during chain invocation for user {update.effective_user.username}: {e}")
        await update.message.reply_text(f"An error occurred while processing your request: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles any non-command message."""
    logger.info(f"Received non-command message from {update.effective_user.username}")
    # Fixed parse_mode issue here
    await update.message.reply_text(
        "I only respond to the /ask command.\n\n"
        "Please format your question as: /ask [your question here]",
        parse_mode=None
    )

# --- 4. Main Function to Run the Bot ---
def main():
    """Starts the Telegram bot polling."""
    # The server is already started in the main scope
    logger.info("Setting up Telegram application...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ask", ask_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is polling for messages...")
    application.run_polling()

if __name__ == "__main__":
    main()