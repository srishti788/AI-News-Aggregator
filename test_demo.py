#!/usr/bin/env python3
"""
Test/Demo Runner for AI News Aggregator
Demonstrates all functionality without sending emails
"""

import sys
import os
from pathlib import Path
from datetime import datetime

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

def test_scrapers(hours: int = 24):
    """Test all scrapers"""
    logger.info("\n" + "=" * 60)
    logger.info("[1/5] Testing Scrapers")
    logger.info("=" * 60)
    
    try:
        from app.scrapers.youtube import YouTubeScraper
        from app.scrapers.openai import OpenAIScraper
        from app.scrapers.anthropic import AnthropicScraper
        from app.config import YOUTUBE_CHANNELS
        
        logger.info("Starting scrape (this may take 10-30 seconds)...")
        
        # OpenAI
        logger.info("\n📰 Fetching OpenAI articles...")
        openai = OpenAIScraper()
        openai_articles = openai.get_articles(hours=hours)
        logger.info(f"  Found {len(openai_articles)} articles")
        if openai_articles:
            logger.info(f"  Example: {openai_articles[0].title[:60]}...")
        
        # Anthropic
        logger.info("\n📰 Fetching Anthropic research...")
        anthropic = AnthropicScraper()
        anthropic_articles = anthropic.get_articles(hours=hours)
        logger.info(f"  Found {len(anthropic_articles)} articles")
        if anthropic_articles:
            logger.info(f"  Example: {anthropic_articles[0].title[:60]}...")
        
        # YouTube
        logger.info("\n🎥 Fetching YouTube videos...")
        youtube = YouTubeScraper()
        total_videos = 0
        if YOUTUBE_CHANNELS:
            for channel_id in YOUTUBE_CHANNELS:
                videos = youtube.get_latest_videos(channel_id, hours=hours)
                total_videos += len(videos)
                logger.info(f"  Channel {channel_id}: {len(videos)} videos")
                if videos:
                    logger.info(f"    Example: {videos[0].title[:60]}...")
        else:
            logger.warning("  No YouTube channels configured in app/config.py")
        
        logger.info(f"\n✓ Scraping complete")
        logger.info(f"  Total: {len(openai_articles) + len(anthropic_articles) + total_videos} items")
        
        return {
            "openai": len(openai_articles),
            "anthropic": len(anthropic_articles),
            "youtube": total_videos
        }
    except Exception as e:
        logger.error(f"✗ Scraping failed: {e}")
        return None

def test_database():
    """Test database operations"""
    logger.info("\n" + "=" * 60)
    logger.info("[2/5] Testing Database")
    logger.info("=" * 60)
    
    try:
        from app.database.repository import Repository
        from app.database.models import YouTubeVideo, OpenAIArticle, AnthropicArticle, Digest
        
        repo = Repository()
        
        # Count existing items
        youtube_count = len(repo.session.query(YouTubeVideo).all())
        openai_count = len(repo.session.query(OpenAIArticle).all())
        anthropic_count = len(repo.session.query(AnthropicArticle).all())
        digest_count = len(repo.session.query(Digest).all())
        
        logger.info(f"Database Statistics:")
        logger.info(f"  YouTube Videos: {youtube_count}")
        logger.info(f"  OpenAI Articles: {openai_count}")
        logger.info(f"  Anthropic Articles: {anthropic_count}")
        logger.info(f"  Digests: {digest_count}")
        logger.info(f"  Total Items: {youtube_count + openai_count + anthropic_count}")
        
        if digest_count > 0:
            digests = repo.get_recent_digests(hours=24)
            logger.info(f"\n✓ Database is populated")
            logger.info(f"  Recent digests: {len(digests)}")
            if digests:
                logger.info(f"  Example digest: {digests[0]['title'][:60]}...")
        else:
            logger.info(f"\n⚠️  No digests yet. Run the pipeline to generate them.")
        
        return True
    except Exception as e:
        logger.error(f"✗ Database test failed: {e}")
        return False

def test_agents():
    """Test AI agents (without API calls)"""
    logger.info("\n" + "=" * 60)
    logger.info("[3/5] Testing AI Agents")
    logger.info("=" * 60)
    
    try:
        from app.agent.digest_agent import DigestAgent
        from app.agent.curator_agent import CuratorAgent
        from app.agent.email_agent import EmailAgent
        from app.profiles.user_profile import USER_PROFILE
        
        load_dotenv()
        
        logger.info(f"Initializing AI agents...")
        digest_agent = DigestAgent()
        curator_agent = CuratorAgent(USER_PROFILE)
        email_agent = EmailAgent(USER_PROFILE)
        
        logger.info(f"✓ DigestAgent initialized")
        logger.info(f"  Model: {digest_agent.model}")
        logger.info(f"✓ CuratorAgent initialized")
        logger.info(f"  Model: {curator_agent.model}")
        logger.info(f"✓ EmailAgent initialized")
        
        logger.info(f"\nUser Profile:")
        logger.info(f"  Name: {USER_PROFILE['name']}")
        logger.info(f"  Title: {USER_PROFILE['title']}")
        logger.info(f"  Expertise: {USER_PROFILE['expertise_level']}")
        logger.info(f"  Interests: {len(USER_PROFILE['interests'])} topics")
        
        logger.info(f"\n✓ All agents working")
        
        return True
    except Exception as e:
        logger.error(f"✗ Agent test failed: {e}")
        return False

def test_pipeline_simulation():
    """Simulate a complete pipeline run without emails"""
    logger.info("\n" + "=" * 60)
    logger.info("[4/5] Pipeline Simulation (Demo Mode)")
    logger.info("=" * 60)
    
    try:
        from app.database.repository import Repository
        
        repo = Repository()
        
        # Get articles for processing
        articles_for_digest = repo.get_articles_without_digest(limit=3)
        
        if articles_for_digest:
            logger.info(f"\nFound {len(articles_for_digest)} articles ready for processing")
            logger.info(f"\nExample articles that would be processed:")
            for i, article in enumerate(articles_for_digest[:3], 1):
                logger.info(f"\n  {i}. {article['type'].upper()}")
                logger.info(f"     Title: {article['title'][:60]}...")
                logger.info(f"     URL: {article['url'][:80]}...")
                logger.info(f"     Content Preview: {article['content'][:100]}...")
            
            logger.info(f"\n✓ Pipeline would process {len(articles_for_digest)} items")
        else:
            logger.info(f"⚠️  No articles ready for digest generation")
            logger.info(f"   Run scrapers and processors first")
        
        return True
    except Exception as e:
        logger.error(f"✗ Pipeline simulation failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 12 + "AI NEWS AGGREGATOR - TEST & DEMO" + " " * 14 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    results = {}
    
    # Test scrapers
    scrape_results = test_scrapers(hours=24)
    results["Scrapers"] = scrape_results is not None
    
    # Test database
    results["Database"] = test_database()
    
    # Test agents
    results["AI Agents"] = test_agents()
    
    # Pipeline simulation
    results["Pipeline"] = test_pipeline_simulation()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("[5/5] Test Summary")
    logger.info("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n✓ All tests passed!")
        logger.info("\nYou can now run the full pipeline:")
        logger.info("  python main.py")
        logger.info("\nOr individual services:")
        logger.info("  python app/services/process_digest.py")
        logger.info("  python app/services/process_curator.py")
        logger.info("  python app/services/process_email.py")
    else:
        logger.error("\n✗ Some tests failed. Check the output above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
