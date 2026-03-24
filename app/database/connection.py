import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_database_url() -> str:
    # Render provides DATABASE_URL for PostgreSQL
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Render PostgreSQL connection
        return database_url
    
    # Local development: try to use PostgreSQL if configured
    use_sqlite = os.getenv("USE_SQLITE", "true").lower() == "true"
    
    if use_sqlite:
        # Use SQLite for development/testing
        db_path = Path(__file__).parent.parent.parent / "ai_news_aggregator.db"
        return f"sqlite:///{db_path}"
    else:
        # Use PostgreSQL for production
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "ai_news_aggregator")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(get_database_url(), echo=False)

# Enable foreign key support for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    return SessionLocal()
