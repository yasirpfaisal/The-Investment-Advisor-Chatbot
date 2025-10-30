

# 🏛️ Investment Philosopher Bot (Buffett & Dalio)

 Yasir Pulikkal
**Task:** AI Innovation Intern - Test Task 3: Investment Advisor Chatbot

This is my (optional) third submission for the Snoonu AI Innovation Intern task.

Instead of a "direct link" web app, I chose to build a **fully-operational Telegram Bot**. This demonstrates a different (and more robust) deployment pattern for an AI service, aligning with the "experimental, AI-powered projects" I am passionate about.

This is a **Retrieval-Augmented Generation (RAG) system** that treats the two investors as separate "experts" and synthesizes their views.

---

### 🚀 Live Demo

You can interact with the live, deployed bot on Telegram:

**Telegram Bot URL**: **[t.me/Invest_Phil_Bot](https://t.me/Invest_Phil_Bot)**

![1](https://github.com/user-attachments/assets/c9ed0cb5-515d-4d28-90d5-34ca3189c479)

🎬 Quick Video Walkthrough

https://www.loom.com/share/fdd98ae14ce74fbbb37938a67065d2d9
## 🤖 How to Use the Investment Philosopher Bot

Interacting with the bot is simple. Here are the main commands:

1.  **Start the Conversation:**
    * Click the link to open telegram or scan the QR code.
    * Press the **"Start"** button or type and send the command:
        ```
        /start
        ```
    * The bot will reply with a welcome message explaining its purpose.

    ---

2.  **Ask an Investment Question:**
    * To ask a question, use the `/ask` command followed by your question.
    * **Format:** `/ask [Your question here]`
    * **Example:**
        ```
        /ask What is your opinion on diversification?
        ```
        ```
        /ask How do Buffett and Dalio view market timing?
        ```
    * **Important:** You *must* include `/ask` before your question. If you just send the question text, the bot will remind you to use the command.

    ---

3.  **Wait for the Response:**
    * After you send an `/ask` command, the bot will reply with "Thinking...".
    * It takes a moment (usually 10-30 seconds) for the bot to retrieve information from its knowledge base (Buffett's letters & Dalio's principles) and for the AI to synthesize the 3-part answer.
    * The bot will then send the complete response, presenting Warren Buffett's view, Ray Dalio's view, and a final synthesized analysis.

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

--

### 3. How to Run Locally

**Prerequisites:**
* You have a `TELEGRAM_BOT_TOKEN`.
* You have an `OPENAI_API_KEY`.
* You have added PDF files to the `data/` folders.

**Step 1: Clone & Setup**
```bash
git clone [https://github.com/](https://github.com/)[yasirpfaisal]/investment-philosopher-telegram-bot.git
cd investment-philosopher-telegram-bot
```
```bash
python -m venv venv
```
```bash 
.\venv\Scripts\activate
pip install -r requirements.txt
 ```
