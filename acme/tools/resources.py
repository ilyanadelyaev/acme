import resource
import logging


logger = logging.getLogger(__name__)


def limit_memory(limit_mb):
    __limit('RLIMIT_DATA', limit_mb)


def __limit(t, limit_mb):
    logger.info(
        'Current "%s" limit: %s',
        t,
        resource.getrlimit(getattr(resource, t)),
    )
    resource.setrlimit(
        getattr(resource, t),
        (
            limit_mb * 1024 * 1024,
            limit_mb * 1024 * 1024,
        ),
    )
    logger.info(
        'New "%s" limit: %s',
        t,
        resource.getrlimit(getattr(resource, t)),
    )
