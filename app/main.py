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
from db.crud.sensors import set_sensor_state
from db.models import Base


def on_moisture_sensor_state_change(channel):
    # sensor detects water when edge is failing so let's reverse it
    state = not GPIO.input(channel)
    set_sensor_state(channel, state)


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


GPIO_EVENTS_MAP = {
    6: on_moisture_sensor_state_change
}
Base.metadata.create_all(bind=engine)
app = get_application()


@app.on_event("startup")
async def initialize_gpio():
    pins = get_gpio_inputs()
    GPIO.setmode(GPIO_MODE)

    for gpio_input in pins:
        if gpio_input not in GPIO_AVAILABLE_PINS:
            logging.error(f"GPIO PIN #{gpio_input.pin} IS INVALID")
            exit(1)
        GPIO.setup(gpio_input.pin, GPIO.IN)
        GPIO.add_event_detect(gpio_input.pin, GPIO.BOTH, bouncetime=300)
        GPIO.add_event_callback(GPIO_EVENTS_MAP[gpio_input.pin], on_moisture_sensor_state_change)


if __name__ == "__main__":
    try:
        uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
    finally:
        GPIO.cleanup()
