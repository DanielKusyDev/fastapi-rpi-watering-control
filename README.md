# fastapi-rpi-watering-control
FastAPI API for Raspberry Pi plants watering control system.

## Prerequisites
 - Python 3.8
 - pip3
 - MySql

### Getting started
 - Copy `app/core/.env.example` to `app/core/.env` file and fill it with data
 - Start MySql
 - Migrate db and run server
```
cd app
alembic upgrade head
python main.py
```
