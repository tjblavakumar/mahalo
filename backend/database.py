from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.config import settings

Base = declarative_base()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    from backend.models import jira_models, servicenow_models, splunk_models  # noqa: F401

    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        # Log the error but don't crash if tables already exist
        print(f"Warning during database initialization: {e}")
        # Tables likely already exist, continue anyway
        pass


def get_db():
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
