import sys, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

try:
    from app.core.config import settings   # local
except ModuleNotFoundError:
    from backend.app.core.config import settings  # render

database_url = os.getenv("DATABASE_URL", settings.database_url)

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

try:
    engine = create_engine(
        database_url,
        future=True,
        echo=False
    )
except OperationalError as e:
    print("❌ Database connection failed during engine creation:", e)
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
