import pytest

import acme.tools.crypto as _crypto


class TestCrypto:
    def test__generate_auth_token(self):
        assert len(_crypto.generate_auth_token()) == \
            _crypto.AUTH_TOKEN_LENGTH
