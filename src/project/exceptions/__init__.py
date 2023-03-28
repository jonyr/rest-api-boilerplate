# -*- coding: utf-8 -*-
"""Exceptions module."""
from werkzeug.exceptions import HTTPException


class CustomException(HTTPException):
    """Custom exception class."""

    def __init__(
        self,
        description: str = "Bad request",
        code: str = "BadRequestError",
        status_code: int = 400,
    ):
        """Initialize custom exception."""
        super().__init__()

        self.code = code
        self.description = description
        self.status_code = status_code
