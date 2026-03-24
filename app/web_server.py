"""Flask web server for AI News Aggregator - handles health checks and status endpoints"""
import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Service is healthy and ready",
        "version": "1.0.0"
    }), 200


@app.route('/status')
def status():
    """Status endpoint - shows service information"""
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Check Render logs for pipeline execution details",
        "port": os.environ.get('PORT', '10000')
    }), 200


@app.route('/logs')
def logs():
    """Logs endpoint"""
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Check Render dashboard for complete pipeline logs"
    }), 200


@app.route('/health')
def health():
    """Additional health check endpoint"""
    return jsonify({"healthy": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Flask web server on port {port}")
    logger.info("ℹ️  This service handles health checks and status endpoints")
    logger.info("ℹ️  Pipeline runs in the background worker service")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
