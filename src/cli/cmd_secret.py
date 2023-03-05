import secrets
import string
import binascii
import os

import click

from flask.cli import with_appcontext


@click.group()
def secret():
    """
    Function to generate any kind of tokens, secrets, passwords
    """


@secret.command()
@click.argument("num_bytes", default=32)
@with_appcontext
def token(num_bytes: int) -> None:
    """
    Generates a random secret token.

    Args:
        num_bytes (int, Optional): lenth. Default to 32.

    Returns:
        str: A token string
    """
    token = secrets.token_hex(num_bytes)
    click.echo(f"Token generated: {token}")


@secret.command()
@click.option(
    "-l",
    "--length",
    "length",
    default=12,
    help="Password lenght. Defaults to 12 chars",
)
def password(length: int) -> None:
    """
    Generates a random password.

    Args:
        length (int): password length. Defaults to 12 chars

    """
    chars: str = string.ascii_letters + string.digits + string.punctuation
    password: str = "".join(secrets.choice(chars) for _ in range(length))
    click.echo(f"Password generated: {password}")


@secret.command()
@click.argument("num_bytes", default=16)
@with_appcontext
def token_urlsafe(num_bytes: int) -> None:
    """
    Generates a random url safe token.

    Args:
        num_bytes (int, Optional): lenth. Default to 16.

    Returns:
        str: A token string
    """
    token = secrets.token_urlsafe(num_bytes)
    click.echo(f"Token generated: {token}")
