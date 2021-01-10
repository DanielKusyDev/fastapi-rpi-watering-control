import json

from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


async def validation_error_handler(_: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(json.loads(exc.json()), status_code=400)
