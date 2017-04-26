import os
import logging


def setup_logging(
        level,
        handler_type=None,
        path=None,
        filename=None,
        root_logger=None,
):
    """
    Setup components logs
    """

    handler = __logging_handler(
        level=level,
        handler_type=handler_type,
        path=path,
        filename=filename,
    )

    __setup_logger(
        level,
        handler,
        name='acme',
        root_logger=root_logger,
    )

    return handler


def __logging_handler(
        level,
        handler_type=None,
        path=None,
        filename=None,
):
    """
    Rotating file handler for logger redirection
    Rotate every midnight
    or
    Stream handler
    """
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'
    )
    #
    if handler_type == 'file':
        # ensure dirs
        if not os.path.exists(path):
            os.makedirs(path)
        #
        handler = logging.FileHandler(
            filename=os.path.join(
                path,
                filename,
            ),
        )
    else:
        handler = logging.StreamHandler()  # pylint: disable=R0204
    #
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def __setup_logger(
        level,
        handler,
        name=None,
        root_logger=None,
):
    """
    Write specified messages for log class :name:
    to handler :handler: with :level:
    """
    if root_logger:
        logger = root_logger
    else:
        logger = logging.getLogger(name)
    #
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
