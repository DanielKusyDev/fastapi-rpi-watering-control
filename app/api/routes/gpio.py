from typing import List

from fastapi import APIRouter


router = APIRouter()

@router.get(path="", )
def get_gpio_pins():
    pass