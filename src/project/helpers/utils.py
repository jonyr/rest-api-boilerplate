import hashlib
import random
import re

from celery import Celery
from flask import current_app, request, url_for
from itsdangerous import Signer, URLSafeTimedSerializer

from itsdangerous.exc import BadSignature, BadTimeSignature
from src.project.exceptions import CustomException


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


def encode_object(data):
    """
    Signs and creates a token that can be used for things such as resetting
    a password or other tasks that involve a one off token.

    Args:
        Data to serialize

    Return:
        Serialized data
    """
    serializer = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"), current_app.config.get("SECRET_KEY_SALT"))

    return serializer.dumps(data)


def decode_string(data: str, expiration: int = 3600):
    """
    Obtains an object from de-serializing a signed token.

    Args:
        data (str): signed token
        expiration (int, optional): Seconds until it expires, defaults to 1 hour.

    Raises:
        CustomException: TokenError

    Returns:
        _type_: _description_
    """
    serializer = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"), current_app.config.get("SECRET_KEY_SALT"))

    try:
        return serializer.loads(data, max_age=expiration)
    except (BadSignature, BadTimeSignature) as error:
        raise CustomException(f"Expired or modified token ({error.__class__.__name__})", "TokenError")


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


def get_ip_address(localhost: str = "54.232.165.254"):
    """
    Gets the real ip address.

    > Se more details [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)
    """
    if "X-Forwarded-For" in request.headers:
        proxy_data = request.headers["X-Forwarded-For"]
        ip_list = proxy_data.split(",")
        return ip_list[0]  # first address in list is User IP
    else:
        if request.remote_addr == "127.0.0.1":
            return localhost
        return request.remote_addr  # For local development


def is_ip_private(ipv4: str):
    """
    Verifies if it is a private ip.

    > See more details [here](https://en.wikipedia.org/wiki/Private_network)
    """
    priv_lo = re.compile(r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    priv_24 = re.compile(r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    priv_20 = re.compile(r"^192\.168\.\d{1,3}.\d{1,3}$")
    priv_16 = re.compile(r"^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$")

    res = priv_lo.match(ipv4) or priv_24.match(ipv4) or priv_20.match(ipv4) or priv_16.match(ipv4)

    if res:
        return True

    return False


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def sign_str(text: str) -> str:
    """Attach a signature to a specific string
    :param text: A string to be signed
    :returns: A signed string.
    """
    return Signer(current_app.config.get("SECRET_KEY"), current_app.config.get("SECRET_KEY_SALT")).sign(text)


def unsign_str(self, signed_text: str) -> str:
    """
    Validate a signed string.
    :param signed_text: A signed string.
    :exception: TokenError: When signature does not match
    :returns: a string
    """
    try:
        return Signer(current_app.config.get("SECRET_KEY"), current_app.config.get("SECRET_KEY_SALT")).unsign(
            signed_text
        )
    except (BadSignature) as error:
        raise CustomException(f"Signature does not match ({error.__class__.__name__})", "TokenError")


def generate_url(endpoint: str, token: str) -> str:
    return url_for(endpoint, token=token, _external=True)


def get_default_email_template_params():
    """
    Gets default email templates parameters.

    Returns:
        dict: dictionary
    """
    return {
        "APP_NAME": current_app.config.get("APP_NAME"),
        "APP_URL": current_app.config.get("APP_URL"),
        "APP_LOGO_URL": current_app.config.get("APP_LOGO_URL"),
        "APP_BANNER_URL": current_app.config.get("APP_BANNER_URL"),
        "PRIMARY_COLOR": current_app.config.get("APP_PRIMARY_COLOR"),
        "FOOTER": current_app.config.get("APP_NAME"),
    }
