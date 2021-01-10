from models.domain import Model


class GpioField(int):
    AVAILABLE_GPIO_PINS = [17, 27, 22, 23, 24, 25]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v not in cls.AVAILABLE_GPIO_PINS:
            raise ValueError("Not a valid GPIO pin")
        return v


class Gpio(Model):
    gpio: GpioField
    is_open: bool = False

    def init(self):
        # GPIO.setup(self.gpio, GPIO.OUT)
        return self

    def open(self):
        # GPIO.output(self.gpio, GPIO.HIGH)
        self.is_open = True

    def close(self):
        # GPIO.output(self.gpio, GPIO.LOW)
        self.is_open = False
