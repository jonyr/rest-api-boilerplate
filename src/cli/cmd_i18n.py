import os

import click
from babel.messages.frontend import CommandLineInterface
from flask.cli import with_appcontext

basedir = os.path.abspath(os.path.dirname(__file__))


@click.group()
def i18n():
    """
    Babel translation tools.
    """


@i18n.command()
@with_appcontext
def extract():
    """
    Extract all the translations labels from files.
    """

    CommandLineInterface().run(
        [
            "pybabel",
            "extract",
            "-F",
            "babel.cfg",
            "-k",
            "lazy_gettext",
            "-o",
            "translations/messages.pot",
            "--project=Arzion Backend",
            "--copyright-holder=Arzion",
            "--version=1.0.0",
            ".",
        ]
    )


@i18n.command()
def update():
    """
    Update translations files.
    """
    CommandLineInterface().run(
        [
            "pybabel",
            "update",
            "-i",
            "messages.pot",
            "-d",
            "translations",
        ]
    )


@i18n.command()
def compile_locales():
    """
    Compile translations.
    """
    CommandLineInterface().run(
        [
            "pybabel",
            "compile",
            "-d",
            "translations",
        ]
    )


@i18n.command()
@click.argument("locale")
def add_locale(locale: str):
    """Add a new locale"""
    CommandLineInterface().run(
        [
            "pybabel",
            "init",
            "-i",
            "messages.pot",
            "-d",
            "translations",
            "-l",
            locale,
        ]
    )
