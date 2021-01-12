#!/bin/bash

baseDir="~/Projects/fastapi-rpi-watering-control/app"
source "~/.virtualenvs/plants/bin/activate"

export PYTHONPATH="$baseDir"
cd "$baseDir"

alembic upgrade head
python "$baseDir/main.py"
