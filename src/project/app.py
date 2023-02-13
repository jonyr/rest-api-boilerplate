import json
import os

from flask import Flask, send_from_directory
from src.config import DefaultConfig
from src.project.extensions import (
    db,
    cors,
    migrate,
    ma,
    jwt,
    schema,
    validator,
    response,
    event,
    aws,
    console,
)
from src.cli import register_cli_commands
from src.project.helpers.utils import make_celery


def create_app() -> "Flask":

    app = Flask(__name__, instance_relative_config=True)

    # Default configuration values
    app.config.from_object(DefaultConfig)
    # Instance configuration value
    app.config.from_pyfile("config.py", silent=True)

    with app.app_context():

        register_extensions(app)

        celery = make_celery(app)
        # https://www.youtube.com/watch?v=2j3em0QQaMg
        celery.set_default()

        register_blueprints(app)
        register_cli_commands(app)
        register_handlers()
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
    from src.project.routes import auth_bp, health_bp

    app.register_blueprint(apidoc_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)


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


def register_handlers():
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
