# coding: utf8
from __future__ import unicode_literals

import uuid

import pytest

import acme.tools.simple_auth as simple_auth


@pytest.fixture
def password():
    return str(uuid.uuid4())


class Test_Tools_SimpleAuth:
    def test__passphrase(self, password):
        hashed, salt = simple_auth.hash_passphrase(password)
        #
        assert len(hashed) == simple_auth.HASHED_LENGTH
        assert len(salt) == simple_auth.SALT_LENGTH
        #
        assert simple_auth.validate_passphrase(
            password, hashed, salt)

    def test__passphrase__empty(self):
        password = ''
        #
        hashed, salt = simple_auth.hash_passphrase(password)
        #
        assert len(hashed) == simple_auth.HASHED_LENGTH
        assert len(salt) == simple_auth.SALT_LENGTH
        #
        assert simple_auth.validate_passphrase(
            password, hashed, salt)

    def test__passphrase__short(self):
        password = 'qwer'
        #
        hashed, salt = simple_auth.hash_passphrase(password)
        #
        assert len(hashed) == simple_auth.HASHED_LENGTH
        assert len(salt) == simple_auth.SALT_LENGTH
        #
        assert simple_auth.validate_passphrase(
            password, hashed, salt)

    def test__passphrase__long(self, password):
        password *= 8
        #
        hashed, salt = simple_auth.hash_passphrase(password)
        #
        assert len(hashed) == simple_auth.HASHED_LENGTH
        assert len(salt) == simple_auth.SALT_LENGTH
        #
        assert simple_auth.validate_passphrase(
            password, hashed, salt)

    def test__passphrase__non_ascii(self):
        password = 'йцукен'
        #
        hashed, salt = simple_auth.hash_passphrase(password)
        #
        assert len(hashed) == simple_auth.HASHED_LENGTH
        assert len(salt) == simple_auth.SALT_LENGTH
        #
        assert simple_auth.validate_passphrase(
            password, hashed, salt)
