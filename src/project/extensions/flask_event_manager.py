# -*- coding: utf-8 -*-
"""Event Manager flask extension."""

EXTENSION_NAME = "event-manager"


class EventManager(object):
    """Event Manager."""

    def __init__(self, app=None):
        self.subscribers = dict()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the app."""
        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

    def subscribe(self, event_type: str, func):
        """Subscribe to an event."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(func)

    def post_event(self, event_type: str, data):
        """Post an event."""
        if event_type not in self.subscribers:
            return

        for func in self.subscribers[event_type]:
            func(data)
