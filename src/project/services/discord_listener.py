from src.project.libs.discord import post_discord_message
from src.project.app import event


def handle_user_register_event(user):
    post_discord_message(f"{user.first_name} has registered with email address {user.email} ({user.activation_code})")


def handle_user_activation_event(user):
    post_discord_message(f"{user.email} activated his account")


def handle_user_login_event(user):
    post_discord_message(f"{user.email} has login")


def setup_discord_event_handlers():
    event.subscribe("user_registered", handle_user_register_event)
    event.subscribe("user_activated", handle_user_activation_event)
