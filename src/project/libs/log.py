from datetime import datetime


def log_message(msg: str):
    print(f"{datetime.now()} - {msg}")
