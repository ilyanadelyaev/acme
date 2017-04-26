# coding: utf8
from __future__ import unicode_literals

import uuid
import hashlib


HASHED_LENGTH = 128
SALT_LENGTH = 32


def hash_passphrase(passphrase):
    """
    Generates salt and return hashed value for passphrase
    """
    salt = uuid.uuid4().hex
    return (hashlib.sha512(
        passphrase.encode('utf8') + str(salt).encode('utf8')
    ).hexdigest(), salt)


def validate_passphrase(passphrase, hashed, salt):
    """
    Validate user passphrase with stored hashed value and salt
    """
    return hashlib.sha512(
        passphrase.encode('utf8') + str(salt).encode('utf8')
    ).hexdigest() == hashed
