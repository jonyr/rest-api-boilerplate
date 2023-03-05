import os
from typing import Any

from flask import Flask, send_from_directory

from src.cli import register_cli_commands
from src.config import DefaultConfig
from src.project.extensions import (
    aws,
    console,
    cors,
    db,
    event,
    filecache,
    jwt,
    ma,
    migrate,
    rediscache,
    response,
    schema,
    validator,
    i18n,
    memcachedcache,
)
from src.project.helpers.utils import make_celery
from src.project.helpers.babel import get_locale, get_timezone
from src.project.helpers.jwt import register_jwt_handlers


def create_app() -> "Flask":

    app = Flask(__name__, instance_relative_config=True)

    # Default configuration values
    app.config.from_object(DefaultConfig)

    # Instance configuration value.
    app.config.from_pyfile("config.py", silent=True)

    with app.app_context():

        register_extensions(app)

        celery = make_celery(app)
        celery.set_default()  # https://www.youtube.com/watch?v=2j3em0QQaMg

        register_blueprints(app)
        register_cli_commands(app)
        register_event_handlers()
        register_jwt_handlers()
        shell_context(app)

        @app.get("/favicon.ico")
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, "static"),
                "favicon.ico",
                mimetype="image/vnd.microsoft.icon",
            )

        return app, celery


def register_blueprints(app):

    from src.project.apidoc import apidoc_bp
    from src.project.routes import atlas_bp, auth_bp, health_bp, toolbox_bp

    app.register_blueprint(apidoc_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(atlas_bp)
    app.register_blueprint(toolbox_bp)


def register_extensions(app):
    """
    Registers app extensions.
    """

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    schema.init_app(app)
    validator.init_app(app)
    response.init_app(app)
    event.init_app(app)
    aws.init_app(app)
    console.init_app(app)
    i18n.init_app(app, timezone_selector=get_timezone, locale_selector=get_locale)
    filecache.init_app(
        app,
        config={
            "CACHE_TYPE": "FileSystemCache",
            "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24 * 30,
            "CACHE_IGNORE_ERRORS": False,
        },
    )
    rediscache.init_app(
        app,
        config={
            "CACHE_TYPE": "RedisCache",
            "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24 * 30,
            "CACHE_KEY_PREFIX": "RESTAPI_",
        },
    )
    memcachedcache.init_app(
        app,
        config={
            "CACHE_TYPE": "MemcachedCache",
            "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 12,
            "CACHE_KEY_PREFIX": "RESTAPI_",
        },
    )


def register_event_handlers():
    from src.project.services.discord_listener import setup_discord_event_handlers
    from src.project.services.email_listener import setup_email_event_handlers
    from src.project.services.log_listener import setup_log_event_handlers

    setup_discord_event_handlers()
    setup_email_event_handlers()
    setup_log_event_handlers()


def shell_context(app):
    @app.shell_context_processor
    def shell():
        return {
            "db": db,
        }
