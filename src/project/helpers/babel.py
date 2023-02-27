from flask import current_app


def get_locale():
    return current_app.config.get("BABEL_DEFAULT_LOCALE")


def get_timezone():
    return current_app.config.get("BABEL_DEFAULT_TIMEZONE")
