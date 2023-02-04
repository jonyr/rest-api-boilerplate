import requests
from flask import current_app


def post_discord_message(message: str):
    """
    Sends a message through Discord Webhooks

    Args:
        message: String to send
    Responses:
        bool: True if success
    """
    payload = {"content": message}

    base_url = current_app.config.get("DISCORD_WEBHOOK_URL")

    if not base_url:
        current_app.logger.error("DISCORD_WEBHOOK_URL is missing in .env")
        return False

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(base_url, headers=headers, json=payload)

    return response.status_code == 204
