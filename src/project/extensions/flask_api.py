""" This file contains the FlaskApi class
which handles responses and exceptions for the framework."""

import logging
import time
import traceback
from logging.handlers import SysLogHandler
from typing import Union
from datetime import datetime

from flask import Flask, jsonify, make_response, request, g, current_app
from flask_sqlalchemy.pagination import Pagination
from werkzeug.exceptions import HTTPException

EXTENSION_NAME = "flask-api"


class Color:
    """
    This class contains color codes for the terminal.
    """

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RESET = "\033[0m"


class FlaskApi:
    """
    This class handles responses, exceptions and logger for the framework.
    """

    def __init__(self, app: Flask = None):
        self.logger = logging.getLogger(__name__)

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        This function initializes the app.

        Args:
            app (Flask): Flask app
        """

        # configure exception handlers
        app.register_error_handler(Exception, self.handle_exception)

        @app.before_request
        def befor_request():
            """This function handles the before request."""
            g.start = time.time()

        @app.after_request
        def after_request(response):
            """This function handles the after request."""

            if self.should_skip_logging_response():
                return response

            method = request.method
            url = request.url
            status_code = response.status_code
            duration = round(time.time() - g.start, 2)
            request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip_address = request.headers.get(
                "X-Forwarded-For", request.remote_addr
            ).split(",")[0]
            json_payload = request.get_json(silent=True)
            error_response = (
                f"ERROR  : {Color.RED}{response.json}{Color.RESET}"
                if status_code > 399
                else ""
            )

            request_color = Color.GREEN if status_code < 400 else Color.RED

            # redact sensitive information
            if json_payload and "password" in json_payload:
                json_payload["password"] = "***REDACTED***"

            json_payload = f"JSON   : {json_payload}" if json_payload else ""

            mensaje = f"""
>>>>>>>>  START REQUEST >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

   METHOD : {method}
   STATUS : {request_color}{status_code}{Color.RESET}
   URL    : {url}
   DATE   : {request_time} DURATION: {duration}s IP: {ip_address}
   {json_payload}
   {error_response}

<<<<<<<<<  END REQUEST  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

"""
            print(mensaje)

            return response

        # configure logging
        log_level = app.config.get("LOG_LEVEL", logging.INFO)
        stream_log_level = app.config.get("STREAM_LOG_LEVEL", logging.INFO)
        syslog_log_level = app.config.get("SYSLOG_LOG_LEVEL", logging.ERROR)

        self.configure_logging(app, log_level, stream_log_level, syslog_log_level)

        app.log = self.log

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

    # LOGGING STUFF BELOW #

    def configure_logging(
        self,
        app: Flask,
        app_log_level: Union[str, int],
        stream_log_level: Union[str, int],
        syslog_log_level: Union[str, int],
    ):
        """
        This function configures the logging for the app.

        Args:
            app (Flask): Flask app
            app_log_level (Union[str, int]): App log level
            stream_log_level (Union[str, int]): Stream log level
            syslog_log_level (Union[str, int]): Syslog log level
        """

        app.logger.setLevel(app_log_level)

        # setup stream handler
        stream_handler = logging.StreamHandler()
        stream_handler_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler.setFormatter(stream_handler_formatter)
        stream_handler.setLevel(stream_log_level)
        self.logger.addHandler(stream_handler)

        # setup syslog handler
        if app.config.get("SYSLOG_ADDRESS") is not None:
            syslog_handler = SysLogHandler(address=app.config.get("SYSLOG_ADDRESS"))
            syslog_handler_formatter = logging.Formatter("[%(levelname)s] %(message)s")
            syslog_handler.setFormatter(syslog_handler_formatter)
            syslog_handler.setLevel(syslog_log_level)
            self.logger.addHandler(syslog_handler)

    def log(self, message: str, level: Union[str, int] = logging.ERROR):
        """
        This function logs the message

        Args:
            message (str): message to log
            level (Union[str, int], optional): log level. Defaults to logging.ERROR.
        """

        self.logger.log(level, message)

    # EXCEPTION HANDLING STUFF BELOW #

    def handle_exception(self, error: Exception):
        """
        This function handles the exception

        Args:
            error (Exception): Exception

        Returns:
            json: response
        """

        # werkzeug.exceptions.HTTPException 4XX
        if isinstance(error, HTTPException):
            response, status_code = self.parse_http_exception(error)
            self.log(self.parse_exception_message(error), logging.ERROR)
            return self.error(response, status_code)

        # Exception 5XX
        response = self.parse_exception(error)
        self.log(self.parse_exception_message(error), logging.ERROR)
        return self.error(response)

    def parse_http_exception(self, error):
        """
        This function parses the http exception

        Args:
            error (HTTPException): HttpException

        Returns:
            json: response
        """

        if isinstance(error.code, int):
            code = error.__class__.__name__
            status_code = error.code

        if isinstance(error.code, str):
            code = error.code
            status_code = error.status_code if hasattr(error, "status_code") else 400

        response = {
            "code": code,
            "description": error.description
            if hasattr(error, "description")
            else "Unknown error",
            "fields": error.fields if hasattr(error, "fields") else None,
        }

        return response, status_code

    def parse_exception(self, error):
        """
        This function parses the exception

        Args:
            error (Exception): Exception

        Returns:
            json: response
        """

        response = {"code": error.__class__.__name__, "description": str(error)}

        # TODO: log error

        return response

    # RESPONSE STUFF BELOW #

    def response(
        self, data, meta: dict = None, code: int = None, pagination: Pagination = None
    ):
        """
        This function builds the response

        Args:
            data (dict): data
            meta (dict, optional): meta. Defaults to None.
            code (int, optional): status code. Defaults to None.
            pagination (Pagination, optional): pagination. Defaults to None.

        Returns:
            json: response
        """

        _response = {}

        _response["data"] = data
        _response["meta"] = meta
        _response["error"] = None
        _response["warning"] = None

        if pagination:
            _response["pagination"] = self.build_pagination(pagination)

        return make_response(jsonify(_response)), self.http_status_code(code)

    def error(self, error, code: int = 500):
        """
        This function builds the error response

        Args:
            error (dict): error
            code (int, optional): status code. Defaults to 500.

        Returns:
            json: response
        """
        _response = {}
        _response["data"] = None
        _response["meta"] = None
        _response["warning"] = None
        _response["error"] = error

        return make_response(jsonify(_response)), code

    def http_status_code(self, code: int = None):
        """
        This function sets the status code

        Args:
            code (int, optional): status code. Defaults to None.

        Returns:
            int: status code
        """
        status_codes = {
            "GET": 200,
            "POST": 201,
            "PUT": 200,
            "PATCH": 200,
            "DELETE": 204,
        }

        return code or status_codes.get(request.method, 200)

    def build_pagination(self, pagination):
        """
        This function builds the pagination

        Args:
            pagination (Pagination): pagination

        Returns:
            dict: pagination
        """

        if isinstance(pagination, (Pagination,)):
            return {
                "prev_page": pagination.prev_num if pagination.prev_num else False,
                "next_page": pagination.next_num if pagination.next_num else False,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "pages": pagination.pages,
                "total": pagination.total,
            }

    def handle_custom_exceptions(self, error):
        """
        This function handles custom http exceptions

        Args:
            error (HTTPException): Custom HttpException

        Returns:
            json: response
        """

        if isinstance(error.code, int):
            code = error.__class__.__name__
            status_code = error.code

        if isinstance(error.code, str):
            code = error.code
            status_code = error.status_code if hasattr(error, "status_code") else 400

        response = {
            "code": code,
            "description": error.description
            if hasattr(error, "description")
            else "Unknown error",
            "fields": error.fields if hasattr(error, "fields") else None,
        }

        return self.error(response, status_code)

    def parse_exception_message(self, error) -> str:
        """
        This function parses the exception to a string

        Args:
            error (Exception): Exception

        Returns:
            str: error
        """

        traceback_list = traceback.extract_tb(error.__traceback__)
        filename, line_number, function_name, code = traceback_list[-1]
        return f"""Error on line {line_number} in file {filename}\n\nMethod: {function_name}\n{code}\n"""

    def color_from_status_code(self, status_code: int):
        """
        This function returns a color based on the status code

        Args:
            status_code (int): status code

        Returns:
            str: color
        """
        if status_code >= 500:
            return Color.RED

        if status_code >= 400:
            return Color.YELLOW

        if status_code >= 300:
            return Color.BLUE

        if status_code >= 200:
            return Color.GREEN

        return Color.RESET

    def should_skip_logging_response(self):
        """
        This function checks if the status code should be logged

        Args:
            status_code (int): status code

        Returns:
            bool: skip logging
        """

        if request.path.startswith("/static"):
            return True

        if request.path.startswith("/favicon.ico"):
            return True

        if current_app.config.get("ENV") == "production":
            return True

        if request.method == "OPTIONS":
            return True

        if request.method in ("POST", "PUT", "PATCH") and not request.is_json:
            return True

        if not current_app.config.get("REQUEST_LOGGER", False):
            return True

        return False
