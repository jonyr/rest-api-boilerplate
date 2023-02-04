import boto3

EXTENSION_NAME = "flask-aws-manager"


class AWSManager(object):
    def __init__(self, app=None):

        self.subscribers = dict()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        self.region_name = self.app.config.get("AWS_DEFAULT_REGION")
        self.aws_access_key_id = self.app.config.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = self.app.config.get("AWS_SECRET_ACCESS_KEY")

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

        @app.teardown_appcontext
        def teardown_response_service(response_or_exc):
            self.reset()
            return response_or_exc

    def reset(self):
        pass

    def get_client(self, client_name):

        return boto3.client(
            client_name,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
