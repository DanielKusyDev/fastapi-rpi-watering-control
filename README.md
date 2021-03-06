# fastapi-rpi-watering-control
FastAPI API for Raspberry Pi plants watering control system.

## Prerequisites
 - Python 3.8
 - pip3
 - MySql

## Getting started

### Locally
 - Set environment variables used in `core/config.py`
 - Migrate db and run server
```
cd app
alembic upgrade head
python main.py
```

### Docker
 - Run docker from provided Dockerfile and entrypoint