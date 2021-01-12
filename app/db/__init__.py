from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST, MYSQL_PORT, MYSQL_USER

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
