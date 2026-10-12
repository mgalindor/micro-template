import logging

import structlog
from structlog.processors import CallsiteParameter, CallsiteParameterAdder

from backend.core.config import settings

log = structlog.get_logger()


def configure_logging() -> None:
    logging.basicConfig(level=settings.logging.level, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            CallsiteParameterAdder(
                {CallsiteParameter.MODULE, CallsiteParameter.FUNC_NAME}
            ),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.logging.level)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
