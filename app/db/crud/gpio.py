from typing import List

from loguru import logger

from db import models
from db.crud import Connection


def get_gpio_pins() -> List[models.Gpio]:
    db = Connection.all(models.Gpio)
    result = db.all()
    return result


def set_gpio_pin_state(channel: int, state: bool):
    with Connection.session_scope() as db:
        try:
            gpio_input: models.Gpio = db.query(models.Gpio).filter_by(channel=channel).one()
        except BaseException as e:
            logger.error(str(e))
            raise e
        else:
            gpio_input.state = state
            db.commit()
