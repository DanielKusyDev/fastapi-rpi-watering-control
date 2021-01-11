import uvicorn
from fastapi import FastAPI
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from api.errors import validation_error_handler
from api.routes import router
from core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, API_PREFIX
from db import engine
from db.models import Base


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(ValidationError, validation_error_handler)
    application.include_router(router, prefix=API_PREFIX)
    return application


Base.metadata.create_all(bind=engine)
app = get_application()

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
