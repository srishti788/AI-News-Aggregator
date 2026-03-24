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
- [x] `render.yaml` created (defines all services and databases)
- [x] `app/web_server.py` created (Flask web service)
- [x] `app/worker.py` created (background worker with retries)
- [x] `.gitignore` updated (excludes `.env` and other sensitive files)
- [x] `RENDER_DEPLOYMENT.md` documentation created

### Code Verified
- [x] `app/database/connection.py` handles `DATABASE_URL` (for Render)
- [x] `app/daily_runner.py` runs the full pipeline
- [x] Works with `USE_SQLITE=true` (local dev) and PostgreSQL (production)
- [ ] All imports work correctly
- [ ] Database models defined properly
- [ ] Web server starts on PORT environment variable
- [ ] Worker properly waits for database and initializes tables

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
- [ ] `.gitignore` properly excludes `.env` and `__pycache__`

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
- [ ] `OPENAI_API_KEY` = `sk-...your-key...` (from https://platform.openai.com/api-keys)

**Optional (for email sending):**
- [ ] `MY_EMAIL` = your email address
- [ ] `APP_PASSWORD` = Gmail app-specific password

**Database (automatically set by Render - DO NOT set manually):**
- [ ] `DATABASE_URL` - Provided automatically by Render
- [ ] `POSTGRES_HOST` - Provided automatically
- [ ] `POSTGRES_PASSWORD` - Provided automatically
- [ ] `POSTGRES_USER` - Provided automatically (usually "postgres_user")
- [ ] `POSTGRES_DB` - Provided automatically (should be "ai_news_aggregator")
- [ ] `POSTGRES_PORT` - Provided automatically (usually 5432)

**How to Check What Variables Render Set:**
1. Go to each service in Render dashboard
2. Click "Settings"
3. Scroll to "Environment" section
4. You'll see all variables that have been set

---

## ✨ Post-Deployment Verification

### Check Service Status
- [ ] Go to https://dashboard.render.com
- [ ] All three services show status:
  - [ ] ai-news-aggregator (Web) - "Live"
  - [ ] ai-news-worker (Background Worker) - "Live"
  - [ ] ai-news-db (PostgreSQL) - "Available"

### Test Web Service
- [ ] Click the web service URL link
- [ ] You should see JSON response: `{"status": "running", ...}`
- [ ] Visit `/status` endpoint to see more info
- [ ] Visit `/health` endpoint for quick health check

### Monitor Worker Service
- [ ] Click "ai-news-worker" service
- [ ] Click "Logs" tab
- [ ] Look for logs showing:
  ```
  ✓ All required environment variables are set
  ⏳ Waiting for database to be ready...
  ✓ Database connection successful
  📊 Initializing database tables...
  ✓ Database tables initialized successfully
  🔄 Pipeline Run #1
  ...starting Daily AI News Aggregator Pipeline...
  ✓ Scraped X YouTube videos
  ✓ Processed Y articles
  ✓ Created Z digests
  ✓ Email sent successfully
  ```

### Verify Pipeline Execution
- [ ] Worker logs show "Pipeline Run #1" completed
- [ ] Logs show articles scraped and processed
- [ ] Next pipeline run scheduled correctly
- [ ] No errors in logs (warnings are okay)

### Database Status
- [ ] ai-news-db service shows "Available"
- [ ] Web service logs show successful table creation
- [ ] Worker can connect to database (no connection errors)

---

## 🔍 Troubleshooting During Deployment

| Error | Cause | Solution |
|-------|-------|----------|
| "Build failed" | Missing dependency or syntax error | Check logs, fix issue, push to GitHub |
| "ModuleNotFoundError" | Package not in requirements.txt | Add to requirements.txt, commit, push |
| "OPENAI_API_KEY not found" | Environment variable not set | Add to Render environment, wait for restart |
| "Database connection refused" | Database not ready yet | Wait 2-3 minutes for all services to start |
| Worker keeps restarting | Python error in code | Check logs for stacktrace, fix, commit, push |
| Services not starting | Syntax errors or missing files | Check that all .py files have correct syntax |

---

## 📋 Pre-Deployment Validation (Run Locally)

Before deploying, verify everything works locally:

```bash
# Test 1: Check Python syntax
python check_syntax.py

# Test 2: Test database connection  
python -c "from app.database.connection import engine; print('✓ Database connection works')"

# Test 3: Create tables
python app/database/create_tables.py

# Test 4: Test web server (local)
python app/web_server.py

# Test 5: Test pipeline (in another terminal)
python app/worker.py  # (Press Ctrl+C to stop)
```

---

## ✅ Final Verification Checklist

- [ ] All services showing "Live"/"Available" in Render dashboard
- [ ] Web service responds to health checks
- [ ] Worker starting up without errors
- [ ] Database tables created successfully
- [ ] Pipeline running at least once (check logs)
- [ ] No Python errors in any logs
- [ ] Environment variables set correctly
- [ ] Ready for continuous operation

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
