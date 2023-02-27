from functools import wraps
from flask import request, abort
from src.project.exceptions import CustomException


def requires_api_key(f):
    """
    Checks if a X_API_KEY is present in headers and it has a valid value.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X_API_KEY")
        if not api_key:
            raise CustomException("Api key is missing", code="MissingApiKey", status_code=401)
        if api_key not in ("9aebf6ca-246d-4c8f-ae16-7c1746e79d6d",):
            raise CustomException("Api key is not valid", code="InvalidApiKey", status_code=403)
        return f(*args, **kwargs)

    return decorated
