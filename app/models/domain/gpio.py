from pydantic import BaseModel


class GpioManager(BaseModel):
    gpio: int
    is_open: bool = False

    def init(self):
        GPIO.setup(self.gpio, GPIO.OUT)
        return self

    def open(self):
        GPIO.output(self.gpio, GPIO.HIGH)
        self.is_open = True

    def close(self):
        GPIO.output(self.gpio, GPIO.LOW)
        self.is_open = False
