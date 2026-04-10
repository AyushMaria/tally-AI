# Tally-AI

> Connects Tally ERP to an AI agent — ask questions about your accounts receivable in plain English via Discord.

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-under%20construction-orange.svg)

> [!WARNING]
> **This project is currently under active construction.** Features are being actively developed and things may change or break. More updates are coming soon — check back regularly for progress.

---

## What it does

Tally-AI is a lightweight AI agent that sits on top of your Tally ERP data stored in Supabase. It exposes a Discord bot interface where you (or your team) can ask natural language questions about outstanding receivables, overdue invoices, and defaulting retailers — and get instant, structured answers.

Under the hood it uses **LangGraph's ReAct agent** with **Gemini 2.5 Flash** as the reasoning model, pulling live data from a Supabase `receivables` table that you sync from Tally.

---

## Features

- **Discord Bot Interface** — ask questions directly in a `#collections-bot` channel
- **Natural Language Queries** — powered by Gemini 2.5 Flash via LangChain
- **Live Supabase Data** — fetches real-time receivables data on every query
- **ReAct Agent Architecture** — uses LangGraph for reliable tool-calling loops
- **Overdue Account Summaries** — total outstanding, top defaulters, aging days
- **Authorized User Access** — restrict bot responses to specific Discord user IDs

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Agent | LangGraph (ReAct) + LangChain |
| LLM | Google Gemini 2.5 Flash |
| Database | Supabase (PostgreSQL) |
| Bot Interface | Discord.py |
| Runtime | Python 3.10+ |

---

## Project Structure

```
tally-AI/
├── agent.py           # LangGraph ReAct agent + tool definitions
├── main.py            # Discord bot setup and message handler
├── supabase_client.py # Supabase REST API client
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template (copy to .env)
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Supabase](https://supabase.com) project with a `receivables` table
- A [Google AI Studio](https://aistudio.google.com) API key (Gemini)
- A [Discord Bot](https://discord.com/developers/applications) token

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/AyushMaria/tally-AI.git
cd tally-AI

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env     # Windows
# cp .env.example .env     # macOS/Linux
# Then edit .env with your actual keys
```

### Environment Variables

Create a `.env` file in the project root (never commit this file):

```env
GEMINI_API_KEY=your_google_gemini_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_or_service_key
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_AUTHORIZED_USER_IDS=123456789,987654321
```

### Running the Bot

```bash
python main.py
```

Once running, the bot will come online in your Discord server and respond to messages in the `#collections-bot` channel.

---

## Supabase Table Schema

The `receivables` table should have at least these columns:

| Column | Type | Description |
|---|---|---|
| `retailer_name` | text | Name of the retailer / party |
| `invoice_number` | text | Tally invoice reference |
| `closing_balance` | numeric | Outstanding amount (₹) |
| `aging_days` | integer | Days since invoice date |

---

## Example Queries

Once the bot is running in Discord, you can ask things like:

- *"Who are the top defaulters this month?"*
- *"What is the total outstanding amount?"*
- *"List all retailers overdue by more than 60 days"*
- *"How many overdue accounts do we have?"*

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## License

[Apache 2.0](LICENSE)
