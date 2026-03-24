"""Background worker for AI News Aggregator - runs the daily pipeline"""
import os
import sys
import time
import logging
from datetime import datetime
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


def wait_for_database(max_retries: int = 30, delay: int = 2) -> bool:
    """Wait for database to be ready before connecting
    
    Args:
        max_retries: Maximum number of connection attempts
        delay: Delay between retries in seconds
    
    Returns:
        True if database is ready, False if timeout
    """
    logger.info("⏳ Waiting for database to be ready...")
    
    try:
        from app.database.connection import engine
        
        for attempt in range(max_retries):
            try:
                with engine.connect() as connection:
                    logger.info(f"✓ Database connection successful (attempt {attempt + 1})")
                    return True
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️  Database not ready (attempt {attempt + 1}/{max_retries}), "
                                   f"retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    logger.error(f"✗ Database connection failed after {max_retries} attempts: {e}")
                    return False
    except Exception as e:
        logger.error(f"✗ Failed to import database module: {e}")
        return False
    
    return False


def initialize_database() -> bool:
    """Initialize database tables
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("📊 Initializing database tables...")
        from app.database.models import Base
        from app.database.connection import engine
        
        Base.metadata.create_all(engine)
        logger.info("✓ Database tables initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize database: {e}", exc_info=True)
        return False


def run_pipeline_continuous(interval_minutes: int = 60) -> None:
    """Run the daily pipeline continuously at specified intervals
    
    Args:
        interval_minutes: Interval between pipeline runs in minutes
    """
    from app.daily_runner import run_daily_pipeline
    
    logger.info("=" * 80)
    logger.info("🤖 AI News Aggregator Background Worker Started")
    logger.info("=" * 80)
    logger.info(f"Pipeline will run every {interval_minutes} minutes")
    logger.info("=" * 80)
    
    # Keep track of run count
    run_count = 0
    
    while True:
        try:
            run_count += 1
            logger.info(f"\n🔄 Pipeline Run #{run_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("─" * 80)
            
            # Run the pipeline
            result = run_daily_pipeline(hours=24, top_n=10)
            
            # Log result
            if result.get("success"):
                logger.info(f"✓ Pipeline run #{run_count} completed successfully")
            else:
                logger.warning(f"⚠️  Pipeline run #{run_count} completed with issues: "
                              f"{result.get('error', 'Unknown error')}")
            
            logger.info("─" * 80)
            logger.info(f"Next run in {interval_minutes} minutes... "
                       f"({datetime.now().strftime('%H:%M:%S')})")
            
            # Wait for next run
            time.sleep(interval_minutes * 60)
            
        except KeyboardInterrupt:
            logger.info("\n⏹️  Shutting down background worker...")
            sys.exit(0)
        except Exception as e:
            logger.error(f"✗ Unexpected error in pipeline loop: {e}", exc_info=True)
            logger.info(f"Retrying in {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)


def main():
    """Main entry point for background worker"""
    
    # Validate environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"✗ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your Render environment")
        sys.exit(1)
    
    logger.info("✓ All required environment variables are set")
    
    # Wait for database to be ready
    if not wait_for_database():
        logger.error("✗ Could not connect to database after multiple attempts")
        sys.exit(1)
    
    # Initialize database tables
    if not initialize_database():
        logger.error("✗ Failed to initialize database")
        sys.exit(1)
    
    # Run pipeline continuously
    run_pipeline_continuous(interval_minutes=60)


if __name__ == "__main__":
    main()
