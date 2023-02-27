from src.project.libs.log import log_message
from src.project.app import event


def handle_user_register_event(user):
    log_message(f"{user.first_name} has registered with email address {user.email}")


def handle_user_login_event(user):
    log_message(f"{user.first_name} has login")


def setup_log_event_handlers():
    event.subscribe("user_registered", handle_user_login_event)
    event.subscribe("user_login", handle_user_login_event)
