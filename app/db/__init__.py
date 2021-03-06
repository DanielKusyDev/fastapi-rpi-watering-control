from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_DRIVER

SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
