#!/bin/bash

baseDir="/home/pi/Projects/fastapi-rpi-watering-control/app"
source "/home/pi/.virtualenvs/plants/bin/activate"

export PYTHONPATH="$baseDir"
cd "$baseDir"

alembic upgrade head
python "$baseDir/main.py"
