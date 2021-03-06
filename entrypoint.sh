#!/bin/bash

echo "Running migrations"
alembic upgrade head

echo "Starting server"
python main.py
