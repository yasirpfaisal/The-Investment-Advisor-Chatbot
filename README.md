# investment-philosopher-telegram-bot

# 🏛️ Investment Philosopher Bot (Buffett & Dalio)

**Candidate:** Yasir Pulikkal
**Task:** AI Innovation Intern - Test Task 3: Investment Advisor Chatbot

This is my (optional) third submission for the Snoonu AI Innovation Intern task.

Instead of a "direct link" web app, I chose to build a **fully-operational Telegram Bot**. This demonstrates a different (and more robust) deployment pattern for an AI service, aligning with the "experimental, AI-powered projects" I am passionate about.

This is a **Retrieval-Augmented Generation (RAG) system** that treats the two investors as separate "experts" and synthesizes their views.

---

### 🚀 Live Demo

You can interact with the live, deployed bot on Telegram:

**Telegram Bot URL:** **[Link to your t.me/YourBotName]**

---

### 1. Solution: RAG Bot as a Telegram Service

My solution is a RAG pipeline deployed as a 24/7 background worker on Render. This is a production-ready architecture.

1.  **Ingestion:** The system ingests two separate knowledge bases (Buffett's letters, Dalio's "Principles") and stores them in an in-memory ChromaDB vector store.
2.  **Telegram Interface:** The bot is built with `python-telegram-bot`. It listens for a `/ask` command.
3.  **Synthesis (MoE):** The user's question is sent to an advanced RAG chain. A "Moderator" LLM (using an advanced prompt) synthesizes the answer in three parts:
    * **Warren Buffett's Perspective** (based *only* on his data)
    * **Ray Dalio's Perspective** (based *only* on his data)
    * **Synthesized Analyst Take** (a final analysis)

This provides a nuanced, accurate, and truly innovative answer, fulfilling the spirit of the "AI Innovation" role.

### 2. Technology Stack

* **Language:** Python
* **Bot Framework:** `python-telegram-bot`
* **RAG:** LangChain
* **LLM:** OpenAI `gpt-4o` (for high-quality synthesis)
* **Vector Store:** ChromaDB (In-memory, persistent as long as the worker is running)
* **Deployment:** **Render** (as a "Background Worker")

---

### 3. ⚠️ CRITICAL: How to Set Up the Bot

#### Part 1: Get Your Telegram Bot Token

1.  Open the Telegram app and search for the **`@BotFather`** (it's the official bot with a checkmark).
2.  Send the command `/newbot`.
3.  Follow the instructions to name your bot (e.g., "Investment Philosopher") and choose a username (e.g., `InvestoPhilBot`).
4.  BotFather will give you a **token**. This is your `TELEGRAM_BOT_TOKEN`.

#### Part 2: Knowledge Base Setup

The `data/` directory is where the bot's "knowledge" lives. For the app to work, you **must** find and add high-quality PDF files to these two folders:

* **`data/buffett/`**: Add Warren Buffett's Shareholder Letters.
* **`data/dalio/`**: Add Ray Dalio's "Principles".

The application will *not* run without these files.

---

### 4. How to Run Locally

**Prerequisites:**
* You have a `TELEGRAM_BOT_TOKEN`.
* You have an `OPENAI_API_KEY`.
* You have added PDF files to the `data/` folders.

**Step 1: Clone & Setup**
```bash
git clone [https://github.com/](https://github.com/)[yasirpfaisal]/investment-philosopher-telegram-bot.git
cd investment-philosopher-telegram-bot
python -m venv venv
# On macOS/Linux: source venv/bin/activate
# On Windows: .\venv\Scripts\activate
pip install -r requirements.txt