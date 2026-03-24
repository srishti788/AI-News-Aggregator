# AI News Aggregator

A production-ready AI-powered news aggregation pipeline that automatically collects articles from multiple sources, processes them with AI, and delivers personalized digests to users.

## 🎯 Features

- **Multi-Source Scraping** - Collects articles from YouTube, OpenAI blog, and Anthropic blog via RSS feeds
- **AI-Powered Article Processing** - Uses OpenAI API to generate summaries and analyze content
- **Personalized Curation** - Ranks articles based on user profiles and interests
- **Automated Digests** - Creates formatted email digests with personalized content
- **Production-Ready Deployment** - Configured for Render with PostgreSQL and scheduled execution
- **Comprehensive Database Layer** - SQLAlchemy ORM with full data persistence
- **Email Integration** - Automated digest delivery via Gmail SMTP

## 🏗️ Project Structure

```
ai-news-aggregator/
├── app/
│   ├── agent/                # AI agents for processing
│   │   ├── curator_agent.py  # Ranks articles by relevance
│   │   ├── digest_agent.py   # Generates article summaries
│   │   └── email_agent.py    # Creates email content
│   ├── database/             # Data persistence layer
│   │   ├── connection.py     # SQLite/PostgreSQL connection
│   │   ├── models.py         # SQLAlchemy ORM models
│   │   ├── repository.py     # Data access layer
│   │   └── create_tables.py  # Database initialization
│   ├── scrapers/             # Content sources
│   │   ├── youtube.py        # YouTube transcript scraper
│   │   ├── openai.py         # OpenAI blog scraper
│   │   └── anthropic.py      # Anthropic blog scraper
│   ├── services/             # Business logic and orchestration
│   │   ├── process_curator.py
│   │   ├── process_digest.py
│   │   ├── process_email.py
│   │   └── process_*.py      # Service processors
│   ├── config.py             # Configuration management
│   ├── runner.py             # One-time execution script
│   └── daily_runner.py       # Daily pipeline orchestration
├── docker/                   # Docker configuration
├── main.py                   # Entry point
├── pyproject.toml            # Project metadata
├── requirements.txt          # Python dependencies
├── Procfile                  # Render service definitions
├── render.yaml               # Render deployment blueprint
├── .env.example              # Environment variable template
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- OpenAI API key
- Gmail account (for email features, optional)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-news-aggregator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or: source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys:
   # OPENAI_API_KEY=sk-...
   # MY_EMAIL=your-email@gmail.com
   # APP_PASSWORD=your-app-password
   ```

5. **Initialize database**
   ```bash
   python main.py
   ```

6. **Run the pipeline**
   ```bash
   python -m app.runner
   ```

## 🧪 Testing

Verify everything works locally:

```bash
python test_demo.py
```

Expected output:
```
✓ PASS - Scrapers
✓ PASS - Database
✓ PASS - AI Agents
✓ PASS - Pipeline
✓ PASS - Summary
```

## 🤖 How It Works

### Pipeline Flow

1. **Scraping** - Collects articles from three sources:
   - YouTube: Extracts transcripts from specified channels
   - OpenAI Blog: RSS feed parsing
   - Anthropic Blog: RSS feed parsing with markdown conversion

2. **Processing** - Anthropic articles converted to markdown using Docling library

3. **Digest Generation** - Each article gets:
   - AI-generated summary (using `gpt-4o-mini`)
   - Relevance ranking against user profile (using `gpt-4o`)

4. **Curation** - Articles ranked by relevance to user interests

5. **Email Creation** - Formatted digest with:
   - Personalized introduction
   - Top-ranked articles
   - Summary and source links
   - HTML/Markdown export

6. **Delivery** - Sent via Gmail SMTP (if configured)

### AI Models Used

- **gpt-4o-mini** - Fast summaries and email generation
- **gpt-4o** - Intelligent article ranking and curation

## 🗄️ Database

### Tables

- **youtube_videos** - Transcript data from YouTube
- **openai_articles** - Articles from OpenAI blog
- **anthropic_articles** - Articles from Anthropic blog
- **digests** - Generated article summaries and rankings

### Local Development

Uses SQLite for simplicity (auto-created as `ai_news_aggregator.db`)

### Production (Render)

Uses PostgreSQL - connection automatically detected via `DATABASE_URL` environment variable

## 🌐 Environment Variables

### Required
- `OPENAI_API_KEY` - Your OpenAI API key (required for AI features)

### Optional
- `MY_EMAIL` - Gmail address for digest delivery
- `APP_PASSWORD` - Gmail app-specific password
- `USE_SQLITE` - Set to `false` in production (auto-detected on Render)

### Auto-Set (Render)
- `DATABASE_URL` - PostgreSQL connection string (provided by Render)

## 📦 Technology Stack

**Backend**
- Python 3.12
- FastAPI (future expansion)
- SQLAlchemy 2.0 (ORM)
- Pydantic 2.0 (validation)

**AI/LLM**
- OpenAI API (GPT-4o, GPT-4o-mini)
- Structured outputs with Pydantic integration

**Database**
- PostgreSQL (production on Render)
- SQLite (local development)

**Content Processing**
- feedparser - RSS feed parsing
- youtube-transcript-api - YouTube transcript extraction
- docling - Document to markdown conversion
- BeautifulSoup4 - HTML/XML parsing

**Email**
- smtplib - Gmail integration
- email.mime - Message formatting

**Utilities**
- python-dotenv - Environment configuration
- requests - HTTP requests

## 🚢 Deployment

### Render Setup (Production)

The project is fully configured for Render deployment:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Render automatically detects `render.yaml`
   - Services created automatically:
     - **Web Service** - Initializes database
     - **Background Worker** - Runs daily pipeline
     - **PostgreSQL Database** - Data persistence

3. **Configure Environment Variables**
   - Set `OPENAI_API_KEY` in Render dashboard
   - Optionally set `MY_EMAIL` and `APP_PASSWORD`

### Deployment Details

- **Web Service** - Runs once on startup to initialize database
- **Background Worker** - Repeats pipeline daily, runs continuously
- **Database** - PostgreSQL managed by Render (5 GB free tier)

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) and [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for detailed instructions.

## 📋 API Documentation

### Core Classes

**Scrapers**
- `YouTubeScraper` - Extracts transcripts from YouTube videos
- `OpenAIScraper` - Parses OpenAI blog RSS feed
- `AnthropicScraper` - Parses Anthropic blog RSS feed

**Agents**
- `DigestAgent` - Generates summaries using OpenAI
- `CuratorAgent` - Ranks articles by relevance
- `EmailAgent` - Creates formatted email content

**Database**
- `Repository` - Centralized data access with methods:
  - `create_youtube_video()` - Store YouTube data
  - `bulk_create_openai_articles()` - Batch save OpenAI articles
  - `get_articles_without_digest()` - Query unprocessed articles
  - `create_digest()` - Store article summary
  - `get_recent_digests()` - Retrieve latest digests

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `OpenAI API Error` | Verify `OPENAI_API_KEY` in `.env` |
| Database won't connect | Check `DATABASE_URL` (Render) or `USE_SQLITE` (local) |
| Scrapers return 0 articles | Check RSS feed URLs and network connectivity |
| Email not sending | Verify Gmail app-specific password and `MY_EMAIL` |

## 📚 Additional Documentation

- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Detailed Render deployment guide
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Pre-deployment verification checklist
- [GETTING_STARTED.md](GETTING_STARTED.md) - Initial setup guide
- [.env.example](.env.example) - Environment variable template

## 📝 License

This project is provided as-is for reference and learning purposes.

## 🤝 Contributing

This is a personal project. For questions or issues, refer to the deployment documentation or troubleshooting section above.

---

**Status:** ✅ Production-ready | 🚀 Render deployment configured | ✨ All tests passing