import importlib

from db.models import Gpio


def get_gpio_callback(gpio: Gpio) -> callable:
    split_callback = gpio.callback.split(".")
    if len(split_callback) == 1:
        module_name = "."
        fn_name = gpio.callback
    else:
        module_name = ".".join(split_callback[:-1])
        fn_name = split_callback[-1]
    callback = importlib.import_module(module_name)
    return getattr(callback, fn_name)
