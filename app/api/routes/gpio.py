from fastapi import APIRouter


router = APIRouter()

#
# @router.get(path="/{gpio_pin}", response_model=Gpio)
# async def get_gpio_list(gpio_pin: int):
#     return Gpio(gpio=gpio_pin, is_open=False)
