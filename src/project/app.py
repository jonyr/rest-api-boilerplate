import json

from flask import Flask
from src.config import Config
from src.project.extensions import db, cors, migrate, ma, jwt, schema, validator, catcher, response
from src.cli import register_cli_commands


def create_app() -> "Flask":

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_file("../../instance/config.json", load=json.load)

    with app.app_context():

        register_extensions(app)
        register_blueprints(app)
        register_cli_commands(app)

        return app


def register_blueprints(app):

    from src.project.apidoc import apidoc_bp
    from src.project.routes import auth_bp

    app.register_blueprint(apidoc_bp)
    app.register_blueprint(auth_bp)


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
    catcher.init_app(app)
    response.init_app(app)
