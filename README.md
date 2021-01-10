# dants-api
FastAPI API for Raspberry Pi plants watering control system.

## Prerequisites
 - Python 3.8
 - pip3
 - MongoDB
 - Docker + Docker compose (optional)

### Getting started
 - Copy `app/core/.env.example` to `app/core/.env` file and fill it with data

#### Run Locally
 - Start MongoDB service
 - Move to `app` directory
 - Run `main.py`

#### Run via Docker
 - Set docker-compose environment variables 
 - Build and run docker-compose container
```
docker-compose build
docker-compose up -d
```