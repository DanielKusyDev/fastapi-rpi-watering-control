import uvicorn
from fastapi import FastAPI
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
import RPi.GPIO as GPIO

from api.errors import validation_error_handler
from api.routes import router
from core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, API_PREFIX, GPIO_MODE, GPIO_DIGITAL_OUT
from db import engine, crud
from db.models import Base


def on_sensor_state_change(channel):
    crud.set_sensor_state(channel)


def initialize_GPIO():
    GPIO.setmode(GPIO_MODE)
    GPIO.setup(GPIO_DIGITAL_OUT, GPIO.IN)
    GPIO.add_event_detect(GPIO_DIGITAL_OUT.channel, GPIO.BOTH, bouncetime=300)
    GPIO.add_event_callback(GPIO_DIGITAL_OUT, on_sensor_state_change)


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
initialize_GPIO()

if __name__ == "__main__":
    try:
        uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
    finally:
        GPIO.cleanup()
