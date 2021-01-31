#!/bin/bash

source "$VENV_PATH"
cd app
export PYTHONPATH="$PWD"
alembic upgrade head && python main.py
