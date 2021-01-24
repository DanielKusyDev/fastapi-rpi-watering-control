import RPi.GPIO as GPIO
from db.crud.gpio import set_gpio_pin_state


def moisture_sensor_callback(channel):
    # sensor detects moisture when edge is falling so let's reverse it
    state = not GPIO.input(channel)
    set_gpio_pin_state(channel, state)
