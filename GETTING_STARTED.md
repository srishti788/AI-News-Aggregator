# AI News Aggregator - Getting Started Guide

This is a complete AI-powered news aggregator that scrapes AI news from multiple sources, processes them with AI, creates digests, ranks them by relevance, and sends them via email.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (venv)
- OpenAI API key (for digest generation)

### 1. Setup Environment

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit `.env` and set:

```env
# Required: OpenAI API key for digest generation
OPENAI_API_KEY=sk-...your-key...

# Optional: Gmail credentials for email sending
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-gmail-app-password

# Database (SQLite by default - no setup needed)
USE_SQLITE=true
```

### 3. Initialize Database

```bash
python app/database/create_tables.py
```

This creates the SQLite database with all required tables.

### 4. Run Setup Verification

```bash
python setup.py
```

This script verifies:
- ✓ Environment configuration
- ✓ Database connectivity
- ✓ Module imports
- ✓ Scraper connectivity

### 5. Run the Application

**Complete Pipeline:**
```bash
python main.py
```

**By Hours (default 24):**
```bash
python main.py 24 10
```
(Scrapes last 24 hours, ranks top 10 articles)

---

## 📊 Project Structure

```
app/
├── agent/                    # AI agents for processing
│   ├── digest_agent.py       # Creates article summaries
│   ├── curator_agent.py      # Ranks articles by relevance
│   └── email_agent.py        # Generates email content
│
├── scrapers/                 # News scrapers
│   ├── youtube.py            # YouTube channel videos
│   ├── openai.py             # OpenAI news RSS feed
│   └── anthropic.py          # Anthropic research feeds
│
├── services/                 # Data processing services
│   ├── process_digest.py     # Generate digests
│   ├── process_youtube.py    # Extract transcripts
│   ├── process_anthropic.py  # Convert to markdown
│   ├── process_curator.py    # Rank by relevance
│   ├── process_email.py      # Generate email digest
│   └── email.py              # Send emails
│
├── database/                 # Data storage
│   ├── models.py             # SQLAlchemy models
│   ├── connection.py         # Database setup
│   ├── repository.py         # Data access layer
│   └── create_tables.py      # Initialize DB
│
├── profiles/                 # User profiles
│   └── user_profile.py       # User interests for ranking
│
└── config.py                 # YouTube channels to monitor
```

---

## 🔄 How It Works

### 1. Scraping (5-10 seconds)
- Fetches latest videos from YouTube channels (configured in `config.py`)
- Fetches latest articles from OpenAI RSS feed
- Fetches latest research from Anthropic feeds

### 2. Processing (20-60 seconds)
- **YouTube**: Extracts transcripts from videos
- **Anthropic**: Converts articles to markdown
- Both are cached to avoid reprocessing

### 3. Digest Generation (10-30 seconds)
- Uses OpenAI API to summarize each article
- Creates title + 2-3 sentence summary
- Stores in database

### 4. Ranking (5-10 seconds)
- Uses `CuratorAgent` to rank articles by relevance
- Compares against user profile (interests, expertise)
- Scores each article 0-10 based on relevance

### 5. Email Generation (5-10 seconds)
- Generates personalized greeting
- Previews top 10 ranked articles
- Sends via Gmail (if configured)

---

## 🎯 Run Individual Services

### Scrape Sources Only
```bash
python app/runner.py
```

### Process YouTube Transcripts
```bash
python app/services/process_youtube.py
```

### Process Anthropic Markdown
```bash
python app/services/process_anthropic.py
```

### Create Digests
```bash
python app/services/process_digest.py
```

### Rank Articles
```bash
python app/services/process_curator.py
```

### Generate Email
```bash
python app/services/process_email.py
```

---

## ⚙️ Configuration

### YouTube Channels
Edit `app/config.py` to add/remove channels:

```python
YOUTUBE_CHANNELS = [
    "UCawZsQWqfGSbCI5yjkdVkTA",  # Matthew Berman
    # Add more channel IDs...
]
```

### User Profile
Edit `app/profiles/user_profile.py` to customize ranking:

```python
USER_PROFILE = {
    "name": "Dave",
    "interests": [
        "Large Language Models (LLMs)",
        "AI safety research",
        # Add your interests...
    ],
    "expertise_level": "Advanced"
}
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'pydantic'"
```bash
pip install pydantic
```

### "OPENAI_API_KEY not set"
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Database errors
```bash
# Recreate database
rm ai_news_aggregator.db
python app/database/create_tables.py
```

### Email not sending
1. Enable 2-factor authentication in Gmail
2. Generate app-specific password at https://myaccount.google.com/apppasswords
3. Set in `.env`:
   ```
   MY_EMAIL=your-email@gmail.com
   APP_PASSWORD=your-16-char-password
   ```

---

## 📈 What to Expect

**First Run:**
- Scrapes recent articles/videos from all sources
- Takes 1-2 minutes (faster on subsequent runs)
- May have some articles with unavailable transcripts

**Subsequent Runs:**
- Only processes new articles
- Takes 30-60 seconds
- Incrementally builds knowledge base

**Database Grows Over Time:**
- Stores articles, videos, digests, rankings
- SQLite file: ~5-50MB depending on content
- Can be reset by deleting `ai_news_aggregator.db`

---

## 📝 API Keys Needed

### OpenAI (Required for AI Features)
1. Sign up: https://openai.com/signup
2. Create API key: https://platform.openai.com/api-keys
3. Add to `.env`

### Gmail (Optional, for email sending)
1. Enable 2-factor authentication
2. Generate app password: https://myaccount.google.com/apppasswords
3. Add to `.env`

---

## 🚨 Important Notes

- **API Costs**: OpenAI charges per API call (~$0.001-0.005 per digest)
- **Rate Limits**: OpenAI has rate limits - start with small batches
- **Transcripts**: Some YouTube videos don't have transcripts
- **Privacy**: Store sensitive data in `.env` - never commit to git

---

## 📚 Learn More

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## ✅ Success Checklist

- [ ] Python 3.12+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` configured with API keys
- [ ] Database initialized
- [ ] `setup.py` passes all checks
- [ ] `main.py` runs without errors
- [ ] Check `ai_news_aggregator.db` exists
- [ ] View sample digests in database

Once all checked, you're ready to use the AI News Aggregator!
