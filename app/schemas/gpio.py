from schemas import Schema


class GpioSchema(Schema):
    pin: int
    state: bool
