import time
import uuid
import random
import zlib
import string


AUTH_TOKEN_LENGTH = 64


def generate_auth_token():
    """
    Generate random string with 64 length
    """
    seq_1 = list(uuid.uuid4().hex)
    seq_2 = list(uuid.uuid4().hex)
    random.shuffle(seq_1)
    random.shuffle(seq_2)
    return ''.join(seq_1 + seq_2)


def generate_hash_ts():
    """
    hash_1-hash_2-timestamp
    """
    return '{}-{}-{}'.format(
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        str(int(time.time())),
    )


def crc_32(data):
    """
    Calculate CRC-32 string
    """
    return str(hex(zlib.crc32(data.encode('utf-8')) % (1 << 32)))[2:]


def generate_password(
        length=None,
        special_characters=None,
):
    if length is None:
        length = 16
    if special_characters is None:
        special_characters = False
    #
    characters = string.ascii_letters + string.digits
    if special_characters:
        characters += string.punctuation
    #
    return ''.join((random.choice(characters) for _ in range(length)))
