import pytest


class TestViewWebView:
    def test__ping__get__200(
            self,
            web_app,
    ):
        resp = web_app.get(
            '/v1/ping/',
        )
        assert resp.status_code == 200
        assert resp.json['version'] == '0'
