from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """ Возвращает читабельную ошибку """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(e) for e in error['loc'])
        message = error['msg']
        errors.append(f"{field}: {message}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": errors}),
    )
