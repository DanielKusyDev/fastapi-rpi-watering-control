import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from core.logging import InterceptHandler

API_PREFIX = "/api"

# ENVS
cfg = Config("./core/.env")
DEBUG: bool = cfg("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = cfg("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = cfg("PROJECT_NAME", cast=str)
ALLOWED_HOSTS: List[str] = cfg(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

# Database
MONGODB_CONFIG = {
    "url": cfg("MONGODB_URL", cast=str),
    "port": cfg("MONGODB_PORT", cast=int),
    "user": cfg("MONGODB_USER", cast=str, default=""),
    "password": cfg("MONGODB_PASSWORD", cast=str, default=""),
    "db": cfg("MONGODB_DB", cast=str)
}
