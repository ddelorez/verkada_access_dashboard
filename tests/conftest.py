import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Corrected import paths assuming 'tests' is at the project root,
# and 'backend' is a package.
# To make these imports work, ensure your PYTHONPATH is set up correctly
# or run pytest from the project root.
# Example: PYTHONPATH=. pytest
from backend.app.main import app  # The FastAPI application instance
from backend.app.db.session import Base, get_db # Base for tables, get_db to override
from backend.app.db.models import User # To ensure User model is loaded by Base

# Define an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./test.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False}
)
SessionLocal_test = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Fixture to create database tables before tests run and drop them after.
    Applied automatically to all sessions due to autouse=True.
    """
    Base.metadata.create_all(bind=engine_test) # Create tables
    yield
    Base.metadata.drop_all(bind=engine_test)   # Drop tables

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Pytest fixture to provide a database session for a single test function.
    Ensures the session is rolled back after the test to maintain isolation.
    """
    connection = engine_test.connect()
    transaction = connection.begin()
    session = SessionLocal_test(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Pytest fixture to provide a TestClient instance for the FastAPI app.
    Overrides the `get_db` dependency to use the test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close() # Should be handled by db_session fixture's teardown

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clean up dependency override after test
    app.dependency_overrides.pop(get_db, None)