# Deploying AI News Aggregator to Render

This guide walks you through deploying the AI News Aggregator to Render.

## Prerequisites

- GitHub account (used by Render for deployment)
- Render account (free at render.com)
- OpenAI API key
- Gmail app password (optional, for email sending)

## Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: AI News Aggregator ready for Render deployment"
```

### 1.2 Push to GitHub

Create a new repository on GitHub, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-news-aggregator.git
git branch -M main
git push -u origin main
```

## Step 2: Create Render Account and Connect GitHub

1. Go to https://render.com
2. Sign up with GitHub (connect your GitHub account)
3. Click "New +" → "Blueprint"
4. Select your GitHub repository

## Step 3: Deploy Using render.yaml

Render will automatically detect `render.yaml` and deploy:

- **Web Service**: Initializes database
- **Background Worker**: Runs the daily pipeline
- **PostgreSQL Database**: Stores data (automatically created)

### What Happens During Deployment:

1. Render clones your repository
2. Installs Python dependencies from `requirements.txt`
3. Creates PostgreSQL database
4. Runs database initialization
5. Starts the background worker (runs `python main.py`)

## Step 4: Configure Environment Variables in Render Dashboard

After creating the services, configure these environment variables in Render:

### Web Service Variables:
- `OPENAI_API_KEY` = Your OpenAI API key
- `MY_EMAIL` = Your email address (optional)
- `APP_PASSWORD` = Gmail app-specific password (optional)

### Worker Service Variables:
(Same as Web Service - will inherit from dashboard)

**To set variables:**

1. Go to your service in Render dashboard
2. Click "Environment"
3. Add each variable from above
4. Render will automatically restart services

### Database Variables:
These are **automatically provided** by Render:
- `DATABASE_URL` - Full PostgreSQL connection string
- `POSTGRES_HOST` - Database host
- `POSTGRES_PASSWORD` - Database password
- etc.

(You don't need to set these - Render provides them)

## Step 5: Enable Background Worker

The background worker runs `python main.py` continuously:

1. Go to your service in Render
2. Set "Start Command" to: `python main.py`
3. Keep the service running

This ensures:
- Scrapes news articles from RSS feeds
- Generates AI digests
- Ranks articles by relevance
- (Optionally) Sends email digests

## Step 6: Monitor Your Deployment

**Check Status:**
- Go to Render dashboard
- View service logs in real-time
- Logs show if pipeline is running correctly

**Expected Log Output:**

```
2026-03-23 11:33:09 - INFO - ============================================================
2026-03-23 11:33:09 - INFO - Starting Daily AI News Aggregator Pipeline
2026-03-23 11:33:09 - INFO - ============================================================
2026-03-23 11:33:10 - INFO - ✓ Scraped 5 YouTube videos, 3 OpenAI articles, 2 Anthropic articles
2026-03-23 11:33:30 - INFO - ✓ Created 10 digests
2026-03-23 11:33:45 - INFO - ✓ Email sent successfully with 10 articles
```

## Step 7: Access Your Database (Optional)

You can connect to your PostgreSQL database:

1. Go to your PostgreSQL service in Render
2. Copy the connection string
3. Use tools like pgAdmin or DBeaver to browse data

## Troubleshooting

### Service Won't Start

**Check logs:**
- Go to service → "Logs"
- Look for error messages
- Common issues:
  - Missing `OPENAI_API_KEY`
  - Database connection failed
  - Missing dependencies

**Solution:**
```bash
# Make sure all dependencies are in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### PostgreSQL Connection Error

**Check:**
1. Verify `DATABASE_URL` is set in Render
2. Confirm PostgreSQL service is running
3. Check database credentials match

**Fix:**
- Redeploy service: Click "Deploy" in Render dashboard

### Python Version Issue

If deployment fails with Python version error:

1. Update `render.yaml` to specify your Python version:
```yaml
pythonVersion: '3.12'
```
2. Push to GitHub
3. Render will auto-redeploy

## Monitoring and Maintenance

### Set Up Email Notifications

In Render dashboard:
1. Go to "Settings" → "Notifications"
2. Enable email alerts for deployment failures

### Monitor Resource Usage

- Render shows CPU/memory usage for your services
- Free tier includes:
  - Up to 3 services
  - 0.5 GB RAM per service
  - Shared PostgreSQL database

### Update Your Code

To deploy new changes:

```bash
git add .
git commit -m "Your changes here"
git push origin main
```

Render will automatically redeploy on every push to `main`.

## Production Best Practices

### 1. Use Environment Variables

✅ **Good:**
```python
api_key = os.getenv("OPENAI_API_KEY")
```

❌ **Bad:**
```python
api_key = "sk-11111111111111"  # Never hardcode!
```

### 2. Monitor Logs

Set up log alerts in Render for errors.

### 3. Schedule Backups

Render PostgreSQL is automatically backed up, but you can:
- Export data periodically
- Use pg_dump to backup locally

### 4. Secure Credentials

- Store all secrets in Render environment variables
- Never commit .env file to GitHub
- Use `.env.example` for documentation

## Costs

**Render Free Tier:**
- 3000 hours/month of free service
- Free PostgreSQL (5 GB storage)
- No credit card required

**Paid Tiers (if needed):**
- Standard: $7/month per service
- Pro: $12/month per service
- PostgreSQL: $7/month onwards

## Performance Tips

1. **Limit article processing** - Process only recent articles:
```python
python main.py 24 10  # Last 24 hours, top 10 articles
```

2. **Schedule wisely** - Run during off-peak hours:
```python
schedule.every().day.at("02:00").do(run_daily_pipeline)  # 2 AM
```

3. **Monitor database** - Keep PostgreSQL usage low:
- Delete old articles periodically
- Archive digests

## Getting Help

- **Render Docs:** https://render.com/docs
- **OpenAI API Issues:** https://platform.openai.com/docs
- **Python Issues:** Check logs in Render dashboard

---

## Quick Reference

**One-time setup:**
```bash
# 1. Create GitHub repo
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-news-aggregator.git
git push -u origin main

# 2. Create Render account and deploy via dashboard
# 3. Set environment variables in Render
# 4. Done! Service starts automatically
```

**Files for Render deployment:**
- ✅ `Procfile` - Tells Render how to run services
- ✅ `render.yaml` - Full service definition
- ✅ `requirements.txt` - Python dependencies
- ✅ `.env.example` - Documentation for env vars
- ✅ `app/database/connection.py` - Handles Render DATABASE_URL

**Your secrets are safe:**
- `.env` is in `.gitignore` (not pushed to GitHub)
- Set secrets in Render dashboard (not in code)

---

Congratulations! Your AI News Aggregator is now deployed on Render! 🚀
