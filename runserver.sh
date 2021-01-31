#!/bin/bash

baseDir="./app"
source "$VENV_PATH"

export PYTHONPATH="$baseDir"
cd "$baseDir"

alembic upgrade head
python "$baseDir/main.py"
