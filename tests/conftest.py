"""
Test configuration — uses a separate in-memory database so tests
never touch the main mahalo.db.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base
from backend.utils.reset_data import reset_demo_data

# Override the database engine for tests — use in-memory SQLite
_test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(monkeypatch_session):
    """Create a fresh in-memory DB for tests, seed it, then tear down."""
    import backend.database as db_module

    # Patch the module-level engine and session so all code uses the test DB
    monkeypatch_session.setattr(db_module, "engine", _test_engine)
    monkeypatch_session.setattr(db_module, "SessionLocal", _TestSession)

    # Create all tables in the test DB
    Base.metadata.create_all(bind=_test_engine)

    # Seed with demo data
    reset_demo_data()
    yield

    # Cleanup
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture(scope="session")
def monkeypatch_session():
    """Session-scoped monkeypatch (pytest's built-in is function-scoped)."""
    from _pytest.monkeypatch import MonkeyPatch
    mp = MonkeyPatch()
    yield mp
    mp.undo()
