import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_DATABASE_URL = "sqlite:////app/sql_app.db"
SQLALCHEMY_DATABASE_URL = os.environ.get("DB_URL", DEFAULT_DATABASE_URL)


logger.info(f"DB_URL: {SQLALCHEMY_DATABASE_URL}")
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DbManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
