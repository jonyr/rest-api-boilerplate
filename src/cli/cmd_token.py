import binascii
import os

import click

from flask.cli import with_appcontext


@click.command()
@click.argument("num_bytes", default=32)
@with_appcontext
def token(num_bytes: int):
    """
    Generates a random secret token.

    Args:
        num_bytes (int, Optional): lenth. Default to 32.

    Returns:
        A token string
    """

    return click.echo(binascii.b2a_hex(os.urandom(num_bytes)))
