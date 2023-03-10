import logging

EXTENSION_NAME = "flask-logger"


class FlaskLoggger(object):
    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        handler.setFormatter(formatter)

        self.logger = logging.getLogger("RestAPI")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

        @app.teardown_appcontext
        def teardown_response_service(response_or_exc):
            self.reset()
            return response_or_exc

    def reset(self):
        pass

    def log(self, message: str):
        self.logger.error(message)
