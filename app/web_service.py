"""
Unified Flask Web Service with Background Pipeline Scheduler
For Render Free Plan (which doesn't support separate worker services)
"""
import os
import sys
import time
import logging
import threading
from datetime import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Global state for pipeline
pipeline_state = {
    "last_run": None,
    "last_success": False,
    "running": False,
    "error": None,
    "run_count": 0
}


def wait_for_database(max_retries: int = 30, delay: int = 2) -> bool:
    """Wait for database to be ready"""
    logger.info("⏳ Waiting for database to be ready...")
    
    try:
        from app.database.connection import engine
        
        for attempt in range(max_retries):
            try:
                with engine.connect() as connection:
                    logger.info(f"✓ Database connection successful")
                    return True
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️  Database not ready (attempt {attempt + 1}/{max_retries}), "
                                   f"retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    logger.error(f"✗ Database connection failed: {e}")
                    return False
    except Exception as e:
        logger.error(f"✗ Failed to import database module: {e}")
        return False
    
    return False


def run_pipeline_safe():
    """Run pipeline with error handling"""
    try:
        from app.daily_runner import run_daily_pipeline
        
        pipeline_state["running"] = True
        pipeline_state["run_count"] += 1
        run_num = pipeline_state["run_count"]
        
        logger.info("=" * 80)
        logger.info(f"🔄 Pipeline Run #{run_num} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        result = run_daily_pipeline(hours=24, top_n=10)
        
        pipeline_state["last_run"] = datetime.now().isoformat()
        pipeline_state["last_success"] = result.get("success", False)
        pipeline_state["error"] = result.get("error") if not result.get("success") else None
        
        if result.get("success"):
            logger.info(f"✓ Pipeline run #{run_num} completed successfully")
        else:
            logger.warning(f"⚠️  Pipeline run #{run_num} completed with issues: "
                          f"{result.get('error', 'Unknown error')}")
        
    except Exception as e:
        logger.error(f"✗ Pipeline error: {e}", exc_info=True)
        pipeline_state["last_success"] = False
        pipeline_state["error"] = str(e)
    finally:
        pipeline_state["running"] = False


def pipeline_scheduler(interval_minutes: int = 60):
    """Run pipeline on a schedule in background thread"""
    logger.info(f"🕐 Pipeline scheduler started (every {interval_minutes} minutes)")
    
    # Run pipeline immediately on startup
    logger.info("🚀 Running initial pipeline...")
    run_pipeline_safe()
    
    # Then schedule for future runs
    while True:
        logger.info(f"⏱️  Next pipeline run in {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)
        run_pipeline_safe()


# Flask Routes
@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Service is healthy and ready",
        "version": "1.0.0"
    }), 200


@app.route('/health')
def health():
    """Quick health check"""
    return jsonify({"healthy": True}), 200


@app.route('/status')
def status():
    """Pipeline status endpoint"""
    return jsonify({
        "service": "running",
        "database": "connected",
        "pipeline": {
            "last_run": pipeline_state["last_run"],
            "last_success": pipeline_state["last_success"],
            "currently_running": pipeline_state["running"],
            "total_runs": pipeline_state["run_count"],
            "last_error": pipeline_state["error"]
        }
    }), 200


@app.route('/logs')
def logs():
    """Logs endpoint"""
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Check Render logs for complete pipeline execution details",
        "logs_location": "Render Dashboard > Logs tab"
    }), 200


def main():
    """Main entry point"""
    
    # Validate environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"✗ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your Render environment")
        sys.exit(1)
    
    logger.info("✓ All required environment variables are set")
    
    # Wait for database
    if not wait_for_database():
        logger.error("✗ Could not connect to database")
        sys.exit(1)
    
    # Start pipeline scheduler in background thread
    scheduler_thread = threading.Thread(target=pipeline_scheduler, args=(60,), daemon=True)
    scheduler_thread.start()
    logger.info("✓ Pipeline scheduler thread started")
    
    # Start Flask web server
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Flask web server on port {port}")
    logger.info("ℹ️  Pipeline runs automatically in the background every 60 minutes")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
