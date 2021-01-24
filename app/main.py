import logging

import uvicorn
from fastapi import FastAPI
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

import RPi.GPIO as GPIO
from api.errors import validation_error_handler
from api.routes import router
from core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, API_PREFIX, GPIO_MODE, GPIO_AVAILABLE_PINS
from db import engine
from db.crud.gpio import get_gpio_pins
from db.models import Base
from helpers.gpio import get_gpio_callback


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(ValidationError, validation_error_handler)
    application.include_router(router, prefix=API_PREFIX)
    return application

Base.metadata.create_all(bind=engine)
app = get_application()


@app.on_event("startup")
async def initialize_gpio():
    pins = get_gpio_pins()
    GPIO.setmode(GPIO_MODE)
    for gpio in pins:
        if gpio.channel not in GPIO_AVAILABLE_PINS:
            logging.error(f"GPIO PIN #{gpio.channel} IS INVALID")
            exit(1)
        if gpio.callback:
            callback = get_gpio_callback(gpio)
            GPIO.setup(gpio.channel, GPIO.IN)
            GPIO.add_event_detect(gpio.channel, GPIO.BOTH, bouncetime=300)
            GPIO.add_event_callback(gpio.channel, callback)


if __name__ == "__main__":
    try:
        uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
    finally:
        GPIO.cleanup()
