import hashlib
import random

from flask import current_app, request
from itsdangerous import URLSafeTimedSerializer


def strtobool(val: str) -> int:
    """
    Converts a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.
    """
    val = val.lower()

    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError(f"Invalid truth value {val}")


def skip_cache():
    """
    Returns True if skip_cache is in request args, else False.
    """
    return "skip_cache" in request.args


def sign_token(data):
    """
    Signs and creates a token that can be used for things such as resetting
    a password or other tasks that involve a one off token.

    Args:
        Data to serialize

    Return:
        Serialized data
    """
    serializer = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))

    return serializer.dumps(data)


def verify_token(token: str, expiration: int = 3600):
    """
    Obtains a user from de-serializing a signed token.

    Args:
        token: Signed token.
        expiration: Seconds until it expires, defaults to 1 hour.

    Returns:
        data or None.
    """
    serializer = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))

    try:
        return serializer.loads(token, max_age=expiration)
    except Exception:
        return None


def random_num(digits=8):
    lower = 10 ** (digits - 1)
    upper = 10**digits - 1
    return random.randint(lower, upper)


def md5_hash(text: str):
    """Return a hash for a given text string

    Args:
        text: string to be hashed

    Returns:
        md5 hashed string
    """
    return hashlib.md5(text.encode()).hexdigest()
