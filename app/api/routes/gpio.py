from typing import List

from fastapi import APIRouter

from db import crud
from schemas.gpio import GpioSchema

router = APIRouter()


@router.get(path="", response_model=List[GpioSchema])
def get_gpio_pins():
    gpio = crud.get_gpio_inputs()
    return gpio
