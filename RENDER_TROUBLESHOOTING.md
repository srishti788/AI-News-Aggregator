# Render Deployment Troubleshooting Guide

This guide explains the common deployment failures and how to fix them.

## Why Deployments Were Failing

Your previous deployments failed due to several architectural issues:

### Issue 1: Race Condition Between Services
**Problem**: The old `render.yaml` had only one service trying to both initialize the database AND run the pipeline. When PostgreSQL was being created, the build command would fail trying to connect.

**Solution**: Split into separate services:
- **Web Service**: Initializes tables, provides health checks
- **Worker Service**: Runs pipeline continuously with retry logic

### Issue 2: Missing Database Readiness Check
**Problem**: The build command tried to create tables immediately, but PostgreSQL might not be ready yet.

**Solution**: Added explicit database readiness checks in `app/worker.py`:
- Waits up to 60 seconds for database to be ready
- Retries connection with exponential backoff
- Clear error messages if database doesn't connect

### Issue 3: No Separate Entry Points
**Problem**: `main.py` was used for everything - Flask server, pipeline, database init
This caused confusion about which command should run where.

**Solution**: Created separate entry points:
- `app/web_server.py` - Pure Flask web server
- `app/worker.py` - Pure background pipeline execution
- Clear separation of concerns

### Issue 4: No Error Handling for Missing Variables
**Problem**: If `OPENAI_API_KEY` wasn't set, the service would fail silently or with cryptic errors.

**Solution**: Added validation in `app/worker.py`:
```python
# Validates required environment variables on startup
required_vars = ["OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)
```

### Issue 5: No Pipeline Scheduling
**Problem**: Pipeline might run once and then never again, or crash and not retry.

**Solution**: `app/worker.py` runs pipeline continuously:
- Runs every 60 minutes on a schedule
- Catches exceptions and retries
- Logs every pipeline run with status

---

## The New Architecture

```
┌─── Render ───────────────────────────────────────┐
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ Web Service (ai-news-aggregator)             │ │
│  │ - Flask app for health checks                │ │
│  │ - Initializes database tables                │ │
│  │ - Runs on PORT (usually 10000)               │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ Background Worker (ai-news-worker)           │ │
│  │ - Waits for database readiness               │ │
│  │ - Runs pipeline every 60 minutes             │ │
│  │ - Handles errors and retries                 │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │ PostgreSQL Database (ai-news-db)             │ │
│  │ - Stores articles, digests, data             │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## Deployment Flow (Fixed)

```
1. Push code to GitHub
2. Render detects update
3. Services install dependencies in parallel
4. PostgreSQL database starts (takes ~30s)
5. Web service initializes:
   - Waits for PostgreSQL to be ready
   - Creates database tables
   - Starts Flask web server
6. Worker service initializes:
   - Waits for PostgreSQL to be ready
   - Verifies OPENAI_API_KEY is set
   - Starts pipeline loop
7. Pipeline runs immediately, then every 60 minutes
```

---

## Common Deployment Errors & Fixes

### Error: "Build Failed"

**What you see in logs**:
```
Build failed with status code 1
...
ModuleNotFoundError: No module named 'xxx'
```

**Cause**: A Python package is missing from `requirements.txt`

**Fix**:
1. Open your `requirements.txt`
2. Add the missing package: `echo "package-name>=1.0.0" >> requirements.txt`
3. Commit and push: `git add requirements.txt && git commit -m "Add missing dependency" && git push`
4. Render will auto-redeploy

---

### Error: "Worker keeps restarting"

**What you see**: Worker service in "Restarting..." status, logs show Python errors

**Likely causes**:
1. Missing `OPENAI_API_KEY` environment variable
2. Syntax error in Python code
3. Import error from missing dependency

**Fix**:
1. Go to Render dashboard → ai-news-worker
2. Click "Logs" tab
3. Look for the error message (usually at the bottom)
4. If it's a code error: Fix it locally, commit, push (auto-redeploy)
5. If it's OPENAI_API_KEY: Set the variable in Environment, service will restart
6. If it's a missing package: Add to requirements.txt, commit, push

---

### Error: "PostgreSQL connection refused"

**What you see in logs**:
```
⏳ Waiting for database to be ready...
ConnectionRefusedError: connection refused
✗ Database connection failed after 30 attempts
```

**Cause**: Database took too long to start

**Fix**:
1. This usually resolves itself within 2-3 minutes
2. If it persists:
   - Click on ai-news-db service
   - Check status (should be "Available")
   - If not available: Wait a bit longer
   - If still not available: Restart the database service

---

### Error: "OPENAI_API_KEY not found"

**What you see in logs**:
```
✗ Missing required environment variables: OPENAI_API_KEY
Please set these variables in your Render environment
```

**Cause**: Environment variable not set in Render dashboard

**Fix**:
1. Go to Render dashboard
2. Click on ai-news-worker service
3. Click "Environment" tab
4. Add new variable:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key from https://platform.openai.com/api-keys
5. Click "Save"
6. Service will restart with the new variable

---

### Error: "all services running but no logs from worker"

**What you see**: 
- Web service shows "Live"
- Worker service shows "Live"
- But no logs appear in worker logs

**Cause**: Logs might be delayed by 30-60 seconds to appear

**Fix**:
1. Wait 2-3 minutes and refresh
2. If still no logs: Click "..." menu → "Restart Service"
3. If logs still don't appear:
   - Check web service logs (might have error during startup)
   - Check database service (click ai-news-db to see it's running)

---

### Error: "Pipeline runs but never creates articles"

**What you see in logs**:
```
✓ Scraped 0 YouTube videos, 0 OpenAI articles, 0 Anthropic articles
✓ Processed 0 digests
```

**Cause**: 
1. YouTube channel IDs not configured
2. APIs not returning results
3. No recent articles within 24-hour window

**Fix**:
1. Check `app/config.py` - verify YOUTUBE_CHANNELS list has valid channels
2. Verify OPENAI_API_KEY by testing locally: `python -c "import openai; print('OK')"`
3. Check if there are actually new articles
4. Monitor several pipeline runs (they run at ~65-minute intervals)

---

## How to Monitor Your Deployment

### Daily Checks

1. Go to https://dashboard.render.com
2. Check that all three services show:
   - ai-news-aggregator: "Live"
   - ai-news-worker: "Live"  
   - ai-news-db: "Available"

### Check Pipeline is Running

1. Click on ai-news-worker
2. Click "Logs" tab
3. You should see logs from the last hour:
   ```
   🔄 Pipeline Run #1 - 2024-03-24 14:30:00
   ...starting Daily AI News Aggregator Pipeline...
   ✓ Scraping articles from sources...
   ✓ Scraped X YouTube videos
   ...
   ✓ Pipeline run #1 completed successfully
   Next run in 60 minutes...
   ```

### Check Web Service is Responsive

1. Click on ai-news-aggregator (web service)
2. Copy the service URL
3. Open in browser (or curl):
   - `https://your-service-url.onrender.com/` - Health check
   - `https://your-service-url.onrender.com/status` - Status details
   - `https://your-service-url.onrender.com/health` - Quick health

### Check Database Status

1. Click on ai-news-db
2. Should show "Available" and "Healthy"
3. You can see database URL and connection info

---

## Rollback & Recovery

### If Deployment Breaks

1. **Immediate**: Identify the problem from logs
2. **Fix locally**: Make the necessary changes to your code
3. **Test**: Run the failing command locally to verify fix
4. **Deploy**: `git add . && git commit -m "Fix: description" && git push`
5. **Render auto-deploys**: Watch logs for success

### If You Need to Revert

If the latest commit broke something:

```bash
# Revert to previous working commit
git revert HEAD
git push

# Render will auto-deploy the previous working version
```

### If a Service Won't Start

1. Click the service
2. Click "..." menu (top right)
3. Click "Restart service"
4. Watch logs to see if it starts

---

## Testing Before Deployment

### Test database initialization locally

```bash
# Use SQLite for testing
export USE_SQLITE=true
python app/database/create_tables.py
# Output: Tables created successfully
```

### Test the worker script locally

```bash
# Run for 1 iteration (will timeout after default interval)
# Press Ctrl+C to stop
python app/worker.py
```

### Test the web server locally

```bash
# In one terminal:
python app/web_server.py

# In another terminal:
curl http://localhost:10000/
# Should return: {"status": "running", ...}
```

---

## Getting Help

1. **Check logs first** - Always the best source of truth
2. **Review this guide** - Most common issues are documented
3. **Test locally** - Run failing code locally to understand the error
4. **Check Render status** - https://status.render.com
5. **Review code** - Ensure all required files exist:
   - `render.yaml`
   - `app/web_server.py`
   - `app/worker.py`
   - `app/daily_runner.py`
   - `requirements.txt` 

---

## Success Signs

After deployment, you should see:

✅ All three services showing "Live"/"Available"  
✅ Web service responds to health checks  
✅ Worker service logs show database initialization  
✅ Pipeline starting immediately  
✅ Pipeline completing with articles found/processed  
✅ Next pipeline run scheduled  
✅ No error messages in logs (warnings are okay)  

If you see all these, your deployment is successful! 🎉
