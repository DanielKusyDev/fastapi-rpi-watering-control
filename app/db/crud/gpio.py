from typing import List

from db import models
from db.crud import Connection


def get_gpio_inputs() -> List[models.Gpio]:
    db = Connection.all(models.Gpio)
    result = db.all()
    return result
