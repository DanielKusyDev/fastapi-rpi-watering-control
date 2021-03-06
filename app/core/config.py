import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
import RPi.GPIO as GPIO
from core.logging import InterceptHandler

API_PREFIX = "/api"
cfg = Config()

# ENVS
DEBUG: bool = cfg("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = cfg("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = cfg("PROJECT_NAME", cast=str, default="Plants control")
ALLOWED_HOSTS: List[str] = cfg(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)
DB_HOST = cfg("DB_HOST", cast=str)
DB_PORT = cfg("DB_PORT", cast=int)
DB_USER = cfg("DB_USER", cast=str, default="")
DB_PASSWORD = cfg("DB_PASSWORD", cast=str, default="")
DB_NAME = cfg("DB_NAME", cast=str)
DB_DRIVER = cfg("DB_DRIVER", cast=str)

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

# Api
DEFAULT_PAGINATION_SIZE = 50

# RPi
GPIO_MODE = GPIO.BCM
GPIO_AVAILABLE_PINS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                       27]
GPIO_CALLBACK_EVENT_MODULE = "app.core.callbacks"
