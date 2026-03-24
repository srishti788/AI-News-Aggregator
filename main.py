from app.daily_runner import run_daily_pipeline
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Service is healthy"
    }), 200

@app.route('/logs')
def logs():
    return jsonify({
        "status": "running",
        "app": "AI News Aggregator",
        "message": "Check Render logs for pipeline execution details"
    }), 200

def main(hours: int = 24, top_n: int = 10):
    return run_daily_pipeline(hours=hours, top_n=top_n)


if __name__ == "__main__":
    import sys
    
    # Run pipeline once on startup
    hours = 24
    top_n = 10
    
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    if len(sys.argv) > 2:
        top_n = int(sys.argv[2])
    
    print("=" * 60)
    print("Starting AI News Aggregator...")
    print("=" * 60)
    
    result = main(hours=hours, top_n=top_n)
    
    print("=" * 60)
    print("Pipeline completed. Starting web server...")
    print("=" * 60)
    
    # Start Flask web server to keep service alive
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
