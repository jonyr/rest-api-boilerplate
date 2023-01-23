import logging
import traceback
from logging import StreamHandler

from werkzeug.exceptions import HTTPException

EXTENSION_NAME = "flask-exception-handler"


class ExceptionHandler(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        handler = StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)

        app.register_error_handler(
            HTTPException,
            self.handle_custom_exceptions,
        )

        app.register_error_handler(
            Exception,
            self.try_catch_all,
        )

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

    def handle_custom_exceptions(self, error):

        status_code = error.status_code if hasattr(error, "status_code") else 400

        response = {
            "code": error.code if hasattr(error, "code") else "UnknownError",
            "message": error.message,
            "fields": error.fields if hasattr(error, "fields") else None,
        }

        return {
            "data": None,
            "error": response,
            "warning": None,
        }, status_code

    def try_catch_all(self, error):
        response = {"code": error.__class__.__name__, "message": str(error)}
        self.logger.error(self.parse_error(error))
        return {"data": None, "error": response, "warning": None}, 500

    @staticmethod
    def parse_error(error) -> str:
        traceback_list = traceback.extract_tb(error.__traceback__)
        filename, line_number, function_name, code = traceback_list[-1]
        return f"""Error on line {line_number} in file {filename}\n\nMethod: {function_name}\n{code}\n"""
