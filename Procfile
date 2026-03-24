web: python -c "from app.database.models import Base; from app.database.connection import engine; Base.metadata.create_all(engine); print('✓ Database initialized')"
worker: python main.py
