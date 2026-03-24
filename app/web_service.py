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
    "run_count": 0,
    "db_initialized": False
}


def ensure_database_initialized():
    """Lazy initialization of database on first request"""
    if pipeline_state["db_initialized"]:
        return True
    
    try:
        from app.database.models import Base
        from app.database.connection import engine
        
        logger.info("📊 Initializing database tables...")
        Base.metadata.create_all(engine)
        pipeline_state["db_initialized"] = True
        logger.info("✓ Database initialized")
        return True
    except Exception as e:
        logger.error(f"✗ Database init failed: {e}")
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


def pipeline_scheduler(initial_delay: int = 120, interval_minutes: int = 60):
    """Run pipeline on schedule - waits for Flask server to start first"""
    logger.info(f"⏱️  Pipeline scheduler: waiting {initial_delay}s before first run")
    time.sleep(initial_delay)
    
    while True:
        try:
            run_pipeline_safe()
        except Exception as e:
            logger.error(f"✗ Scheduler error: {e}")
        
        time.sleep(interval_minutes * 60)


# Flask Routes
@app.route('/')
def health_check():
    """Health check endpoint"""
    ensure_database_initialized()
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Service is healthy and ready"
    }), 200


@app.route('/health')
def health():
    """Quick health check - no database call"""
    return jsonify({"healthy": True}), 200


@app.route('/status')
def status():
    """Pipeline status endpoint"""
    ensure_database_initialized()
    return jsonify({
        "service": "running",
        "pipeline": {
            "last_run": pipeline_state["last_run"],
            "last_success": pipeline_state["last_success"],
            "running": pipeline_state["running"],
            "total_runs": pipeline_state["run_count"],
            "error": pipeline_state["error"]
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
    
    # Start pipeline scheduler in background thread with 2-minute initial delay
    scheduler_thread = threading.Thread(
        target=pipeline_scheduler, 
        args=(120, 60),
        daemon=True
    )
    scheduler_thread.start()
    logger.info("✓ Pipeline scheduler started (first run in 2 minutes)")
    
    # Start Flask web server IMMEDIATELY (don't wait for anything)
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Flask web server on port {port}")
    logger.info("ℹ️  Pipeline will run in 2 minutes, then every 60 minutes")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
