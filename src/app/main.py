from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.middleware import setup_middleware
from app.core.telemetry import configure_telemetry, instrument_fastapi


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings=settings)
    configure_telemetry(service_name=settings.app_name, service_version=settings.app_version)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    setup_middleware(app=app, settings=settings)
    app.include_router(api_router, prefix=settings.api_prefix)
    instrument_fastapi(app)

    Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
    return app


app = create_app()


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.is_development,
        workers=1 if settings.is_development else settings.server_workers,
    )
