from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from contextlib import contextmanager

# Load environment variables from .env file
load_dotenv()

# Access database file path
database_path = os.getenv(
    "DB_PATH", "finance.db"
)  # Default to provided path if not set

# SQLite connection string
connection_str = f"sqlite:///{database_path}"

# Create engine
engine = create_engine(
    connection_str, echo=True
)  # `echo=True` for logging queries during development

# Session factory
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_db_session():
    """
    Provides a session instance to interact with the database.
    Usage: with get_db_session() as session:
               # perform database operations
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
