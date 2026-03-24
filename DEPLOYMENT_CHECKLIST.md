# Render Deployment Checklist

## ✅ Pre-Deployment Tasks (Local)

### Code Preparation
- [ ] All code committed and tested locally
- [ ] No hardcoded API keys or credentials in code
- [ ] `.env` file is in `.gitignore` (confirmed via `.gitignore` file)
- [ ] `.env.example` created with template variables
- [ ] `requirements.txt` updated with all dependencies
- [ ] Database connection supports both SQLite and PostgreSQL

### Files Created for Deployment
- [ ] `Procfile` created (defines how to run services)
- [ ] `render.yaml` created (defines all services and databases)
- [ ] `.gitignore` updated (excludes `.env` and other sensitive files)
- [ ] `RENDER_DEPLOYMENT.md` documentation created

### Code Verified
- [ ] `app/database/connection.py` handles `DATABASE_URL` (for Render)
- [ ] `python main.py` runs without errors locally
- [ ] Works with `USE_SQLITE=true` (local dev) and `USE_SQLITE=false` (production)
- [ ] All imports work correctly
- [ ] Database models defined properly

---

## 📝 GitHub Setup

- [ ] GitHub account created
- [ ] New repository created (ai-news-aggregator)
- [ ] Local repository initialized:
  ```bash
  git init
  git add .
  git commit -m "Initial commit: AI News Aggregator ready for Render"
  ```
- [ ] Remote added:
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/ai-news-aggregator.git
  git branch -M main
  git push -u origin main
  ```
- [ ] All files pushed to GitHub
- [ ] Can view repository on github.com

---

## 🚀 Render Setup

### Account & Connection
- [ ] Render account created (render.com)
- [ ] Logged in with GitHub
- [ ] GitHub repository connected to Render

### Service Creation
- [ ] Clicked "New +" → "Blueprint"
- [ ] Selected your GitHub repository
- [ ] Render detected `render.yaml` automatically
- [ ] Services to be created:
  - [ ] Web service (ai-news-aggregator)
  - [ ] Background worker (ai-news-worker)
  - [ ] PostgreSQL database (ai-news-db)

### Environment Variables
In Render Dashboard, set these for **all services**:

**Essential:**
- [ ] `OPENAI_API_KEY` = `sk-...your-key...`

**Optional (for email sending):**
- [ ] `MY_EMAIL` = your email address
- [ ] `APP_PASSWORD` = Gmail app-specific password

**Database (automatically set by Render):**
- [ ] `DATABASE_URL` - Provided automatically
- [ ] `POSTGRES_HOST` - Provided automatically
- [ ] `POSTGRES_PASSWORD` - Provided automatically
- [ ] `POSTGRES_DB` = `ai_news_aggregator`
- [ ] `USE_SQLITE` = `false`

---

## ✨ Post-Deployment

### Verify Deployment
- [ ] All services showing "Live" status in Render dashboard
- [ ] PostgreSQL database is running
- [ ] Background worker is running
- [ ] Can view logs without errors

### Monitor Logs
- [ ] Go to ai-news-worker service → "Logs"
- [ ] Look for successful pipeline runs:
  ```
  Starting Daily AI News Aggregator Pipeline
  ✓ Scraped N articles
  ✓ Created N digests
  ```

### Test Functionality
- [ ] Worker logs show pipeline running
- [ ] Check database has data:
  - Service → "Database" tab
  - Connect with database client or Render's data browser
  - Verify tables: youtube_videos, openai_articles, digests, etc.

### Email Testing (Optional)
- [ ] If configured, verify email digest sent
- [ ] Check inbox for "Daily AI News Digest"

---

## 🔧 Troubleshooting

### If services won't start:
- [ ] Check all environment variables are set
- [ ] Verify `OPENAI_API_KEY` is valid
- [ ] Look at service logs for error messages
- [ ] Try manual redeploy: Click "Deploy" in Render

### If database connection fails:
- [ ] Verify PostgreSQL service is running
- [ ] Check `DATABASE_URL` environment variable is set
- [ ] Confirm connection string format is correct

### If code changes don't deploy:
- [ ] Verify changes are pushed to `main` branch on GitHub
- [ ] Render auto-deploys on every push (watch for this)
- [ ] Can manually trigger redeploy in Render dashboard

---

## 📊 Expected Behavior

### Startup (First 2-3 minutes)
1. Render builds Python environment
2. Installs dependencies from requirements.txt
3. Creates PostgreSQL database
4. Runs database initialization
5. Starts background worker
6. Worker begins first pipeline run

### Every Run (First run)
- Scrapes articles from YouTube, OpenAI, Anthropic
- Takes 1-2 minutes (depends on article count)
- Stores data in PostgreSQL
- Generates AI digests using OpenAI API

### Subsequent Runs
- Process only new articles
- Takes 30-60 seconds
- Continues indefinitely (worker never stops)

### Logs Show
```
2026-03-23 ... Starting Daily AI News Aggregator Pipeline
2026-03-23 ... ✓ Scraped X videos, Y articles, Z articles
2026-03-23 ... ✓ Created N digests
2026-03-23 ... ✓ Ranked articles by relevance
2026-03-23 ... Pipeline completed successfully
```

---

## 💰 Costs

**Render Free Tier:**
- ✅ Free services (up to 3)
- ✅ Free PostgreSQL database (5 GB)
- ✅ 0.5 GB RAM per service
- ⚠️ Services may spin down after 15 minutes of inactivity
  - (Not an issue with continuous running worker)

**Estimated Monthly Cost:** $0 (Free tier)

---

## 🎯 Quick Verification Commands

**Before deploying, verify locally:**

```bash
# 1. Test with SQLite (local dev)
venv\Scripts\python test_demo.py

# 2. Verify all services work
venv\Scripts\python main.py

# 3. Check requirements
pip freeze | grep -E "(openai|sqlalchemy|pydantic)"
```

**After deploying, check Render:**

1. Go to Render dashboard
2. Click your workspace → ai-news-worker
3. View "Logs" tab
4. Should see pipeline activity

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs
- **Procfile Reference:** https://render.com/docs/procfile
- **PostgreSQL Guide:** https://render.com/docs/managed-postgres
- **Environment Variables:** https://render.com/docs/environment-variables
- **Scheduled Jobs:** https://render.com/docs/cron-jobs

---

## ✅ Final Checklist Before Clicking Deploy

- [ ] GitHub repository is public and accessible
- [ ] All files committed and pushed to `main` branch
- [ ] `.env` is in `.gitignore` (not in repository)
- [ ] `Procfile` exists and is correct
- [ ] `render.yaml` exists and is correct
- [ ] `requirements.txt` has all dependencies
- [ ] `OPENAI_API_KEY` is ready to set in Render
- [ ] You understand this will:
  - Create a PostgreSQL database
  - Run Python continuously
  - Call OpenAI API (costs money)
  - Send emails (if configured)

**Status: Ready to Deploy** ✅

---

If all items are checked, you're ready to deploy on Render!

**Next Step:** Go to render.com → Click "New Blueprint" → Select your GitHub repo → Deploy
