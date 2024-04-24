import logging

import uvicorn
from fastapi import FastAPI

from src.api.v1 import deposit_routes
from src.core.logger import LOGGING

app = FastAPI(
    title="Read-only API для расчета депозитов",
    description="Расчитываем депозиты клиентов",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    log_config=LOGGING,
    log_level=logging.DEBUG
)

app.include_router(deposit_routes.router, prefix="/api/v1", tags=['calculate'])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
