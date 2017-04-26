import pytest

import flask_webtest


@pytest.fixture(scope='session')
# pylint: disable=W0621
def application():
    """
    Application
    """
    from acme.neuro.api.application import Application
    return Application()


@pytest.fixture
def web_app(application):
    wt = flask_webtest.TestApp(application.flask_app)
    wt.cookiejar.clear()
    return wt
