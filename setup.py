#!/usr/bin/env python3
"""
Complete setup and initialization script for AI News Aggregator
This script ensures all prerequisites are met and initializes the database
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check that environment variables are properly set"""
    logger.info("=" * 60)
    logger.info("Checking Environment Configuration")
    logger.info("=" * 60)
    
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or openai_key == "your-api-key-here":
        logger.warning("⚠️  OPENAI_API_KEY not properly configured")
        logger.warning("   Set a valid API key in .env to use AI features")
    else:
        logger.info("✓ OpenAI API key configured")
    
    my_email = os.getenv("MY_EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    if not my_email or my_email == "your-email@gmail.com":
        logger.warning("⚠️  Email configuration not set (email sending will be skipped)")
    else:
        logger.info("✓ Email configuration found")
    
    use_sqlite = os.getenv("USE_SQLITE", "true").lower() == "true"
    logger.info(f"✓ Database: {'SQLite (Local)' if use_sqlite else 'PostgreSQL'}")
    
    return True

def initialize_database():
    """Initialize the database with all tables"""
    logger.info("\n" + "=" * 60)
    logger.info("Initializing Database")
    logger.info("=" * 60)
    
    try:
        from app.database.models import Base
        from app.database.connection import engine, get_database_url
        
        logger.info(f"Database URL: {get_database_url()}")
        
        # Create tables
        Base.metadata.create_all(engine)
        logger.info("✓ Database tables created/verified")
        
        # Verify tables exist
        from app.database.models import YouTubeVideo, OpenAIArticle, AnthropicArticle, Digest
        logger.info("✓ All models imported successfully")
        
        return True
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False

def test_imports():
    """Test that all critical modules can be imported"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Module Imports")
    logger.info("=" * 60)
    
    try:
        logger.info("Importing scrapers...")
        from app.scrapers.youtube import YouTubeScraper
        from app.scrapers.openai import OpenAIScraper
        from app.scrapers.anthropic import AnthropicScraper
        logger.info("✓ Scrapers imported")
        
        logger.info("Importing agents...")
        from app.agent.digest_agent import DigestAgent
        from app.agent.curator_agent import CuratorAgent
        from app.agent.email_agent import EmailAgent
        logger.info("✓ AI agents imported")
        
        logger.info("Importing services...")
        from app.services.process_digest import process_digests
        from app.services.process_youtube import process_youtube_transcripts
        from app.services.process_anthropic import process_anthropic_markdown
        from app.services.process_curator import curate_digests
        from app.services.process_email import send_digest_email
        logger.info("✓ Services imported")
        
        logger.info("Importing database...")
        from app.database.repository import Repository
        logger.info("✓ Repository imported")
        
        return True
    except Exception as e:
        logger.error(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scrapers():
    """Test that scrapers can connect and fetch data"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Scrapers")
    logger.info("=" * 60)
    
    try:
        from app.scrapers.openai import OpenAIScraper
        from app.scrapers.anthropic import AnthropicScraper
        from app.config import YOUTUBE_CHANNELS
        from app.scrapers.youtube import YouTubeScraper
        
        logger.info("Testing OpenAI scraper...")
        openai_scraper = OpenAIScraper()
        openai_articles = openai_scraper.get_articles(hours=24)
        logger.info(f"✓ OpenAI scraper: found {len(openai_articles)} articles")
        
        logger.info("Testing Anthropic scraper...")
        anthropic_scraper = AnthropicScraper()
        anthropic_articles = anthropic_scraper.get_articles(hours=24)
        logger.info(f"✓ Anthropic scraper: found {len(anthropic_articles)} articles")
        
        logger.info("Testing YouTube scraper...")
        youtube_scraper = YouTubeScraper()
        if YOUTUBE_CHANNELS:
            for channel_id in YOUTUBE_CHANNELS[:1]:  # Test first channel only
                videos = youtube_scraper.get_latest_videos(channel_id, hours=24)
                logger.info(f"✓ YouTube scraper: found {len(videos)} videos from {channel_id}")
        
        return True
    except Exception as e:
        logger.error(f"✗ Scraper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all setup and initialization tasks"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 10 + "AI NEWS AGGREGATOR - SETUP & INITIALIZATION" + " " * 5 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    steps = [
        ("Environment Check", check_environment),
        ("Database Initialization", initialize_database),
        ("Module Imports", test_imports),
        ("Scraper Connectivity", test_scrapers),
    ]
    
    results = {}
    for step_name, step_func in steps:
        try:
            results[step_name] = step_func()
        except Exception as e:
            logger.error(f"✗ {step_name} failed with error: {e}")
            results[step_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Setup Summary")
    logger.info("=" * 60)
    
    for step_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status} - {step_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n✓ All checks passed! You can now run the application:")
        logger.info("\n  1. Initialize database (one-time):")
        logger.info("     venv\\Scripts\\python app/database/create_tables.py")
        logger.info("\n  2. Run the complete pipeline:")
        logger.info("     venv\\Scripts\\python main.py")
        logger.info("\n  3. Or run individual services:")
        logger.info("     venv\\Scripts\\python app/services/process_digest.py")
        logger.info("     venv\\Scripts\\python app/services/process_curator.py")
        logger.info("     venv\\Scripts\\python app/services/process_email.py")
    else:
        logger.error("\n✗ Some checks failed. Please review the errors above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
