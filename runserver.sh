#!/bin/bash

baseDir="/home/pi/Projects/fastapi-rpi-watering-control"
source ~/.virtualenvs/plants/bin/activate

export PYTHONPATH="$baseDir"
cd "$baseDir/app"

alembic upgrade head
python "$baseDir/app/main.py"
