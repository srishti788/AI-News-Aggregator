# Deploying AI News Aggregator to Render

This guide walks you through deploying the AI News Aggregator to Render with proper error handling and reliability.

## Architecture

The deployment uses three Render services:

1. **Web Service** (`ai-news-aggregator`) - Flask app for health checks and status endpoints
2. **Background Worker** (`ai-news-worker`) - Runs the daily pipeline continuously  
3. **PostgreSQL Database** (`ai-news-db`) - Stores all data

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

Render will automatically detect `render.yaml` and deploy three services:

- **Web Service** (ai-news-aggregator): Initializes database and provides health checks
- **Background Worker** (ai-news-worker): Runs the daily pipeline continuously
- **PostgreSQL Database**: Stores all news articles and digests

### How Deployment Works

1. Render clones your repository
2. Creates PostgreSQL database (takes ~30 seconds)
3. Web service installs Python dependencies
4. Web service initializes database tables
5. Background worker starts and begins pipeline execution every hour
6. Both services stay running continuously

### Important Notes

- **Database Initialization**: The web service automatically creates all database tables on startup
- **Database Readiness**: The worker waits up to 60 seconds for the database to be ready
- **Pipeline Interval**: The background worker runs the full pipeline every 60 minutes
- **Health Checks**: Visit the web service URL to see health check status

## Step 4: Configure Environment Variables in Render Dashboard

After services are created, add these environment variables in Render:

### Required for All Services:

- `OPENAI_API_KEY` = Your OpenAI API key (from https://platform.openai.com/api-keys)

### Optional (for email digest features):

- `MY_EMAIL` = Your email address  
- `APP_PASSWORD` = Gmail app-specific password

### Database Variables (automatically set by Render):

Render automatically provides these - **do not set them manually**:
- `DATABASE_URL` - PostgreSQL connection string
- `POSTGRES_HOST` - Database host
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_USER` - Database user
- `POSTGRES_DB` - Database name
- `POSTGRES_PORT` - Database port

### To Set Variables in Render Dashboard:

1. Go to each service in Render (web and worker)
2. Click "Environment" 
3. Add:
   - `OPENAI_API_KEY` = your-api-key
   - (Optional) `MY_EMAIL` and `APP_PASSWORD`
4. Click "Save changes"
5. Services will automatically restart with new variables

## Step 5: Verify Deployment

### Check Service Status

1. Go to https://dashboard.render.com
2. You should see three services:
   - ✓ ai-news-aggregator (Web) - Status: "Live"
   - ✓ ai-news-worker (Background Worker) - Status: "Live"  
   - ✓ ai-news-db (PostgreSQL) - Status: "Available"

### Check if Services are Working

1. Click the web service link to open the health check URL
2. You should see JSON response confirming the service is running
3. Go to the `/status` endpoint to see more details

### View Pipeline Logs

1. Click on "ai-news-worker" service
2. Click the "Logs" tab
3. You should see pipeline execution logs:
   ```
   ✓ Database connection successful
   ✓ Database tables initialized successfully
   🔄 Pipeline Run #1 - 2024-03-24 14:30:00
   ...starting Daily AI News Aggregator Pipeline...
   ✓ Scraped 15 YouTube videos...
   ✓ Processed 12 Anthropic articles...
   ✓ Created 10 digests...
   ✓ Pipeline run #1 completed successfully
   Next run in 60 minutes...
   ```

## Troubleshooting Deployment Failures

### Issue: Build Failure or "Database Connection Error"

**Cause**: Database not ready when web service initializes tables

**Fix**: This is automatically handled now with database connectivity checks

**Check logs**: Go to web service → Logs tab

### Issue: Worker Service Shows Error

**Cause**: Usually missing `OPENAI_API_KEY` environment variable

**Fix**:
1. Check "Environment" tab for both services
2. Verify `OPENAI_API_KEY` is set correctly
3. Redeploy: Click "Manual Deploy" → "Deploy Latest Commit"

**Check logs**: Go to worker service → Logs tab

### Issue: Services Keep Restarting

**Cause**: Often a Python import error or missing dependency

**Fix**:
1. Check the logs for the error message
2. If it's an import error, add the package to `requirements.txt`
3. Commit and push to GitHub
4. Render will auto-redeploy

### Issue: Database Shows "Available" but Worker Fails

**Cause**: PostgreSQL is ready but credentials not set correctly

**Fix**:
1. Verify environment variables are set for BOTH services
2. Check that `USE_SQLITE=false` is NOT set (it should use DATABASE_URL)
3. Wait 1-2 minutes for all services to start
4. Manually restart the worker service

## Monitoring & Maintenance

### Daily Monitoring

- Check Render dashboard once daily
- All three services should show "Live" or "Available"
- Pipeline should run every hour automatically

### View Recent Logs

Worker service logs show:
- When pipeline runs start and complete
- How many articles were scraped and processed
- Any errors or failed operations
- Email digest status

### Restart Services (if needed)

If a service appears stuck:
1. Go to that service in Render
2. Click the "..." menu (top right)
3. Select "Restart Service"

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "ModuleNotFoundError" | Missing Python dependency | Add package to requirements.txt and redeploy |
| "OPENAI_API_KEY not found" | Missing environment variable | Set in Render dashboard for both services |
| "Connection refused" | Database not ready | Wait 2-3 minutes for all services to initialize |
| Worker keeps restarting | Python error in code | Check logs for specific error, fix, and redeploy |
| Pipeline doesn't run | Worker service stopped | Check logs, restart service, or redeploy |

## Deployment Checklist

```
✓ Repository pushed to GitHub
✓ render.yaml present in repository root
✓ requirements.txt includes all dependencies
✓ app/web_server.py exists (Flask web service)
✓ app/worker.py exists (background worker)
✓ app/daily_runner.py properly configured
✓ All three services showing "Live" in Render
✓ OPENAI_API_KEY environment variable set
✓ Worker logs show successful pipeline runs
✓ Web service health check returning 200 OK
```

## Getting Help

- **Render Support**: https://render.com/docs
- **Check Logs**: Always start by checking the detailed logs for each service
- **Test Locally**: Run `python app/worker.py` locally to test pipeline logic
- **Git Logs**: If deployment fails, check git commit history to see what changed
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
