"""Database models and engine setup for the register/login system.

A single SQLAlchemy engine and sessionmaker are created here and reused by the
application. The connection string can be overridden with the DATABASE_URL
environment variable; it defaults to a local SQLite file (userDB.db).
"""

import os

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

# Connection string. Defaults to a local SQLite file. Override with DATABASE_URL
# (for example: postgresql+psycopg://user:pass@host:5432/db).
CONN = os.environ.get("DATABASE_URL", "sqlite:///userDB.db")

engine = create_engine(CONN)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Person(Base):
    __tablename__ = "Person"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    # Unique so the same username cannot be registered twice.
    user = Column(String(20), unique=True, nullable=False)
    # Stores a salted PBKDF2 hash, not the plaintext password. Widened from the
    # original String(10) because hashes are long.
    passwd = Column(String(255), nullable=False)


class Tokens(Base):
    __tablename__ = "Tokens"
    id = Column(Integer, primary_key=True)
    id_person = Column(Integer, ForeignKey("Person.id"))
    token = Column(String(100))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    """Create all tables. Idempotent."""
    Base.metadata.create_all(engine)


init_db()
