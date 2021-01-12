from typing import List

from fastapi import APIRouter

from db import crud
from schemas.gpio import GpioSchema

router = APIRouter()


@router.get(path="", response_model=List[GpioSchema])
def get_gpio_pins():
    inputs = crud.get_gpio_inputs()
    result = [GpioSchema(pin=gpio.pin, state=gpio.state) for gpio in inputs]
    return result
