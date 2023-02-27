import logging
import logging.handlers
import traceback

from flask import jsonify, make_response, request
from flask_sqlalchemy import Pagination
from werkzeug.exceptions import HTTPException

EXTENSION_NAME = "flask-response-manager"


class ResponseManager(object):
    """
    This class handles responses and exceptions for the framework.
    """

    def __init__(self, app=None):

        self.response = None
        self.status_code = None
        self.errors = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.config["JSON_SORT_KEYS"] = True

        # TODO: parametizar mejor esto
        handler = logging.handlers.SysLogHandler(address=(app.config.get("SYSLOG_HOST"), app.config.get("SYSLOG_PORT")))

        formatter = logging.Formatter(
            "[%(name)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)", datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)

        # TODO: get logger name from config
        self.logger = logging.getLogger("Backend")
        self.logger.addHandler(handler)

        # TODO: Get level from config
        self.logger.setLevel(logging.ERROR)

        app.register_error_handler(HTTPException, self.handle_custom_exceptions)
        app.register_error_handler(Exception, self.try_catch_all)

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

        @app.teardown_appcontext
        def teardown_response_service(response_or_exc):
            self.reset()
            return response_or_exc

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
            "description": error.description if hasattr(error, "description") else "Unknown error",
            "fields": error.fields if hasattr(error, "fields") else None,
        }

        return self.build_error(response, status_code)

    def try_catch_all(self, error):
        response = {"code": error.__class__.__name__, "description": str(error)}
        self.logger.error(self.parse_error(error))

        return self.build_error(response)

    @staticmethod
    def parse_error(error) -> str:
        traceback_list = traceback.extract_tb(error.__traceback__)
        filename, line_number, function_name, code = traceback_list[-1]
        return f"""Error on line {line_number} in file {filename}\n\nMethod: {function_name}\n{code}\n"""

    def build(self, data, meta: dict = None, code: int = None, pagination: Pagination = None):

        _response = {}

        _response["data"] = data
        _response["meta"] = meta
        _response["error"] = None
        _response["warning"] = None

        if pagination:
            _response["pagination"] = self.build_pagination(pagination)

        self.response = make_response(jsonify(_response))

        return self.response, self.set_status_code(code)

    def build_error(self, error, code: int = 500):
        _response = {}
        _response["data"] = None
        _response["meta"] = None
        _response["warning"] = None
        _response["error"] = error
        self.response = make_response(jsonify(_response))
        return self.response, code

    def set_status_code(self, code: int = None):

        http_status_codes = {
            "GET": 200,
            "POST": 201,
            "PUT": 200,
            "PATCH": 200,
            "DELETE": 204,
        }
        return code or http_status_codes.get(request.method, 200)

    def build_pagination(self, pagination):

        if isinstance(pagination, (Pagination,)):

            return {
                "prev_page": pagination.prev_num if pagination.prev_num else False,
                "next_page": pagination.next_num if pagination.next_num else False,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "pages": pagination.pages,
                "total": pagination.total,
            }

    def reset(self):
        self.response = None
        self.status_code = None
        self.errors = None
