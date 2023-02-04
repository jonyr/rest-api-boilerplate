from flask import make_response, jsonify, request
from flask_sqlalchemy import Pagination

EXTENSION_NAME = "flask-event-manager"


class EventManager(object):
    def __init__(self, app=None):

        self.subscribers = dict()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

        @app.teardown_appcontext
        def teardown_response_service(response_or_exc):
            self.reset()
            return response_or_exc

    def reset(self):
        pass

    def subscribe(self, event_type: str, fn):

        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(fn)

    def post_event(self, event_type: str, data):

        if event_type not in self.subscribers:
            return

        for fn in self.subscribers[event_type]:
            fn(data)
