from src.api.v1 import deposit_routes
import uvicorn
from fastapi import FastAPI
from core.utils import validation_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(deposit_routes.router, prefix="/api/v1", tags=['calculate'])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
