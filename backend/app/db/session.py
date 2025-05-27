from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the SQLite database URL.
# The database file will be created in the 'backend' directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///../dashboard.db"  # Relative to the 'app' directory

# Create the SQLAlchemy engine.
# connect_args is needed for SQLite to allow multithreaded access.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class, which will be used to create database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions.
Base = declarative_base()

def init_db():
    """
    Initializes the database by creating all tables defined in the models.
    This should be called once at application startup.
    """
    # Import all modules here that define models so that
    # they are registered properly on the metadata. Otherwise
    # you will have to import them first before calling init_db()
    from .models import User # noqa
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency to get a database session.
    Ensures the database session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()