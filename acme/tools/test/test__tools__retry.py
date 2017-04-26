import pytest
import mock

import requests
import requests_mock

import acme.tools.retry as retry


class TestRetry:
    def test__no_retry(self):
        @retry.retry(Exception, 2)
        def f(v):
            v[0] -= 1
        #
        value = [2]
        f(value)
        # one call without retries
        assert value[0] == 1

    def test__exception_not_match(self):
        @retry.retry(AttributeError, 2)
        def f(v):
            v[0] -= 1
            raise RuntimeError
        #
        with pytest.raises(RuntimeError):
            value = [3]
            f(value)
        # one call without retries
        assert value[0] == 2

    def test__0_attempts(self):
        @retry.retry(Exception, 0)
        def f(v):
            v[0] -= 1
            raise Exception
        #
        with pytest.raises(Exception):
            value = [1]
            f(value)
        # one call - ignore zero
        assert value[0] == 0

    def test__1_attempt(self):
        @retry.retry(Exception, 1)
        def f(v):
            v[0] -= 1
            raise Exception
        #
        with pytest.raises(Exception):
            value = [1]
            f(value)
        # one call
        assert value[0] == 0

    def test__2_attempts(self):
        @retry.retry(Exception, 2)
        def f(v):
            v[0] -= 1
            raise Exception
        #
        with pytest.raises(Exception):
            value = [2]
            f(value)
        # two calls
        assert value[0] == 0

    def test__default_attempts(self):
        @retry.retry(Exception)
        def f(v):
            v[0] -= 1
            raise Exception
        #
        with pytest.raises(Exception):
            value = [3]
            f(value)
        # three calls
        assert value[0] == 0


class TestRetryWrapper:
    def test__args(self):
        def f(i):
            return i
        assert retry.wrapper(
            context={
                'function': f,
                'args': (1,),
            },
        ) == 1

    def test__kwargs(self):
        def f(i):
            return i
        assert retry.wrapper(
            context={
                'function': f,
                'kwargs': {'i': 1},
            },
        ) == 1

    def test__exception_not_match(self):
        def f(v):
            v[0] += 1
            raise AttributeError
        with pytest.raises(AttributeError):
            value = [0]
            retry.wrapper(
                context={
                    'function': f,
                    'args': (value,),
                },
                attempts=10,
                exceptions=RuntimeError,
            )
        assert value[0] == 1

    def test__1_attempts(self):
        def f(v):
            v[0] += 1
            raise AttributeError
        with pytest.raises(AttributeError):
            value = [0]
            retry.wrapper(
                context={
                    'function': f,
                    'args': (value,),
                },
                attempts=1,
                exceptions=AttributeError,
            )
        assert value[0] == 1

    def test__2_attempts(self):
        def f(v):
            v[0] += 1
            raise AttributeError
        with pytest.raises(AttributeError):
            value = [0]
            retry.wrapper(
                context={
                    'function': f,
                    'args': (value,),
                },
                attempts=2,
                exceptions=AttributeError,
            )
        assert value[0] == 2


class TestRequestsRetryWrapper:
    def test__no_raise(self):
        with requests_mock.mock() as m:
            m.get(
                'http://example.com/',
                text='OK',
                status_code=200,
            )
            #
            result = retry.requests_wrapper(
                context={
                    'function': 'get',
                    'args': (
                        'http://example.com/',
                    ),
                },
            )
            assert result.ok
            assert result.text == 'OK'

    def test__raises(self):
        __RETRY_SLEEP = retry.RETRY_SLEEP
        retry.RETRY_SLEEP = 0.0
        with pytest.raises(requests.exceptions.RequestException):
            result = retry.requests_wrapper(
                context={
                    'function': 'get',
                    'args': (
                        'invalid',
                    ),
                },
            )
        retry.RETRY_SLEEP = __RETRY_SLEEP

    def test__not_ok(self, monkeypatch):
        with requests_mock.mock() as m:
            m.get(
                'http://example.com/',
                text='ERROR',
                status_code=404,
            )
            #
            __RETRY_SLEEP = retry.RETRY_SLEEP
            retry.RETRY_SLEEP = 0.0
            result = retry.requests_wrapper(
                context={
                    'function': 'get',
                    'args': (
                        'http://example.com/',
                    ),
                },
            )
            retry.RETRY_SLEEP = __RETRY_SLEEP
            assert not result.ok
            assert result.text == 'ERROR'
