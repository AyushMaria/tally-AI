# 🧾 Tally-AI

> An AI-powered bridge between Tally ERP and intelligent business automation — transforming raw accounting data into actionable insights.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active%20development-green.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)]()

---

## 📖 Overview

**Tally-AI** is a smart integration layer that connects [Tally ERP](https://tallysolutions.com/) with AI-driven workflows. It parses Tally's XML data exports, normalizes ledger and voucher information, and feeds it into an AI pipeline for analysis, reporting, and automation — making accounting intelligence accessible without leaving your workflow.

Whether you're a retailer tracking inventory costs, an accountant reconciling ledgers, or a developer building financial tooling, Tally-AI bridges the gap between raw ERP data and modern AI capabilities.

---

## ✨ Features

- **XML Parsing** — Reads and parses Tally's native XML export format with full schema support
- **Ledger Normalization** — Converts raw voucher entries into structured, queryable data
- **AI Integration** — Connects with LLM APIs (Gemini, Claude, OpenRouter) for natural language Q&A over financial data
- **Retailer Insights** — Pre-built prompts and pipelines tailored for retail accounting use cases
- **Automated Reporting** — Generate summaries, anomaly detection, and trend analysis from Tally data
- **REST API** — Exposes a clean API so other tools and frontends can query processed accounting data

---

## 🗂️ Project Structure

```
tally-AI/
├── src/
│   ├── parser/         # Tally XML parsing and normalization
│   ├── ai/             # LLM integration and prompt management
│   ├── api/            # REST API layer
│   └── utils/          # Shared utilities and helpers
├── data/               # Sample Tally XML exports (gitignored)
├── tests/              # Unit and integration tests
├── .env.example        # Environment variable template
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Tally ERP 9 / TallyPrime (for XML export)
- An API key for your chosen LLM provider (Gemini, Claude, or OpenRouter)

### Installation

```bash
# Clone the repository
git clone https://github.com/AyushMaria/tally-AI.git
cd tally-AI

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy the example env file
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# LLM Provider (choose one)
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
CLAUDE_API_KEY=your_claude_api_key

# Tally XML Data Path
TALLY_DATA_DIR=./data/

# API Server
PORT=8000
```

### Running the App

```bash
python src/main.py
```

The API will be available at `http://localhost:8000`.

---

## 🔌 Tally XML Export

To export data from Tally ERP for use with Tally-AI:

1. Open Tally ERP / TallyPrime
2. Go to **Gateway of Tally → Display → Account Books → Ledger**
3. Press **Alt+E** to export
4. Select **XML** format and save to the `data/` directory

Tally-AI will automatically detect and process new files placed in the configured data directory.

---

## 🤖 AI Capabilities

Tally-AI uses a structured prompt architecture to answer questions like:

- *"What were total sales in March compared to February?"*
- *"Which ledger has the highest outstanding balance?"*
- *"Summarize this month's expense breakdown by category."*
- *"Flag any unusual transactions above ₹50,000."*

LLM calls are made via the [OpenRouter](https://openrouter.ai/) or Google Gemini API, making it easy to swap models without changing application logic.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| XML Parsing | `xml.etree.ElementTree`, `lxml` |
| AI Integration | Google Gemini API / OpenRouter |
| API Server | FastAPI |
| Data Handling | Pandas |
| Environment | `python-dotenv` |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [Apache 2.0 License](LICENSE).

---

<p align="center">Built with ❤️ by <a href="https://github.com/AyushMaria">Ayush Maria</a></p>
