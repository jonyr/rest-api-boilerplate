import importlib
import os


def register_cli_commands(app: "Flask" = None) -> None:
    """Register 0 or more Flask CLI commands (mutates the app passed in).

    Args:
        app (Flask, optional): Flask application instance. Defaults to None.

    """
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and filename.startswith("cmd_"):
            module = importlib.import_module(f"src.cli.{filename[:-3]}")
            cmd = getattr(module, filename[4:-3])
            app.cli.add_command(cmd)
