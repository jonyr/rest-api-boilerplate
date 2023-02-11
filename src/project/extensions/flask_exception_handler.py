import logging
import logging.handlers
import traceback

from werkzeug.exceptions import HTTPException

EXTENSION_NAME = "flask-exception-handler"


class ExceptionHandler(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        handler = logging.handlers.SysLogHandler(address=(app.config.get("SYSLOG_HOST"), app.config.get("SYSLOG_PORT")))
        formatter = logging.Formatter(
            "[%(name)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        self.logger = logging.getLogger("Backend")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)

        app.register_error_handler(HTTPException, self.handle_custom_exceptions)
        app.register_error_handler(Exception, self.try_catch_all)

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

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

        return {
            "error": response,
            "data": None,
            "warning": None,
        }, status_code

    def try_catch_all(self, error):
        response = {"code": error.__class__.__name__, "description": str(error)}
        self.logger.error(self.parse_error(error))
        return {"data": None, "error": response, "warning": None}, 500

    @staticmethod
    def parse_error(error) -> str:
        traceback_list = traceback.extract_tb(error.__traceback__)
        filename, line_number, function_name, code = traceback_list[-1]
        return f"""Error on line {line_number} in file {filename}\n\nMethod: {function_name}\n{code}\n"""
