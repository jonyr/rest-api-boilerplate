EXTENSION_NAME = "event-manager"


class EventManager(object):
    def __init__(self, app=None):

        self.subscribers = dict()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

    def subscribe(self, event_type: str, fn):

        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(fn)

    def post_event(self, event_type: str, data):

        if event_type not in self.subscribers:
            return

        for fn in self.subscribers[event_type]:
            fn(data)
