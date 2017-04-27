import pytest


class TestViewWebView:
    def test__index__get__200(
            self,
            web_app,
    ):
        resp = web_app.get(
            '/',
        )
        assert resp.status_code == 200
