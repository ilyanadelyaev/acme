import time
import functools

import requests


RETRY_SLEEP = 3.0  # seconds


def retry(exc_cls, tries=3, logger=None):
    """
    Retry decorator
    :exc_cls: class to follow
    :tries: number of tries
    """
    def decoy(f):
        @functools.wraps(f)
        def functor(*args, **kwargs):
            t = tries  # copy
            # last one without catching
            while t > 1:
                try:
                    return f(*args, **kwargs)
                except exc_cls as ex:
                    if logger:
                        msg = 'Retry for "{}" / attempts: {}'.format(
                            f.__name__, (t - 1))
                        logger.error(msg)
                        logger.exception('retry error')
                    t -= 1
            return f(*args, **kwargs)
        return functor
    return decoy


def wrapper(
        context,
        exceptions=None,
        attempts=None,
):
    """
    result = retry.wrapper(
        context={
            'function': requests.get,
            'args': ('http://example.com/'),
            'kwargs': {
                'auth': AUTH_DATA,
            },
        },
        exceptions=(requests.exceptions.RequestException),
        attempts=30,
    )
    """
    #
    DEFAULT_EXCEPTIONS = (Exception,)
    DEFAULT_RETRY_ATTEMPTS = 3
    #
    if exceptions is None:
        exceptions = DEFAULT_EXCEPTIONS
    if attempts is None:
        attempts = DEFAULT_RETRY_ATTEMPTS
    #
    if not context.get('args'):
        context['args'] = []
    if not context.get('kwargs'):
        context['kwargs'] = {}
    #
    for attempt in xrange(attempts):
        try:
            result = context['function'](
                *context['args'], **context['kwargs'])
            break
        except exceptions as ex:
            if attempt >= (attempts - 1):
                raise
            time.sleep(attempt * RETRY_SLEEP)
            continue
    return result


def requests_wrapper(
        context,
        attempts=None,
        sessions=False,
):
    """
    response = retry.requests_wrapper(
        context={
            'function': 'get',
            'args': ('http://example.com/'),
            'kwargs': {
                'auth': AUTH_DATA,
            },
        },
        attempts=30,
    )
    """
    DEFAULT_RETRY_ATTEMPTS = 3
    #
    if attempts is None:
        attempts = DEFAULT_RETRY_ATTEMPTS
    #
    if not context.get('args'):
        context['args'] = []
    if not context.get('kwargs'):
        context['kwargs'] = {}
    #
    if sessions:
        session = requests.session()
        func = getattr(session, context['function'].lower())
    else:
        func = getattr(requests, context['function'].lower())
    #
    for attempt in xrange(attempts):
        try:
            response = func(
                *context['args'], **context['kwargs'])
            if response.ok:
                break
            if response.status_code < 500:
                break
            if attempt >= (attempts - 1):
                break
            try:
                r_data = response.json()
            except ValueError:
                pass
            time.sleep(attempt * RETRY_SLEEP)
            continue
        except requests.exceptions.RequestException:
            if attempt >= (attempts - 1):
                raise
            time.sleep(attempt * RETRY_SLEEP)
            continue
    return response
