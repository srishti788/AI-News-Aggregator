from app.daily_runner import run_daily_pipeline
import os
import threading
from flask import Flask, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store pipeline status
pipeline_status = {
    "running": False,
    "last_run": None,
    "last_success": False,
    "error": None
}

def run_pipeline_background():
    """Run pipeline in background thread"""
    try:
        logger.info("Starting pipeline in background...")
        pipeline_status["running"] = True
        result = run_daily_pipeline(hours=24, top_n=10)
        pipeline_status["last_run"] = result
        pipeline_status["last_success"] = result.get("success", False)
        pipeline_status["error"] = result.get("error") if not result.get("success") else None
        logger.info(f"Pipeline completed: {result}")
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        pipeline_status["error"] = str(e)
        pipeline_status["last_success"] = False
    finally:
        pipeline_status["running"] = False

@app.route('/')
def health_check():
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Service is healthy and ready",
        "pipeline_running": pipeline_status["running"]
    }), 200

@app.route('/status')
def status():
    return jsonify({
        "pipeline": pipeline_status
    }), 200

@app.route('/logs')
def logs():
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Check Render logs for pipeline execution details"
    }), 200


if __name__ == "__main__":
    # Start pipeline in background thread immediately
    logger.info("Starting AI News Aggregator Service")
    pipeline_thread = threading.Thread(target=run_pipeline_background, daemon=True)
    pipeline_thread.start()
    
    # Start Flask web server immediately on PORT
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
