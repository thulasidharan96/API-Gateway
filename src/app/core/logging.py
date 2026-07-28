from __future__ import annotations

import logging
import sys

import structlog

from app.core.config import Settings


def configure_logging(*, settings: Settings) -> None:
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        timestamper,
    ]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    log_level = logging.DEBUG if settings.is_development else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s", stream=sys.stdout)
