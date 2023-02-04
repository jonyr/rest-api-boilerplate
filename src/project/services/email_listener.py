from src.project.libs.email import send_email
from src.project.app import event


def handle_user_register_event(user):
    send_email(user.name, user.email, "Welcome", "Your password is PEPE")


def handle_user_login_event(user):
    send_email(user.name, user.email, "Login Data", f"Login Counts {user.sign_in_count}")


def setup_email_event_handlers():
    event.subscribe("user_registered", handle_user_register_event)
    event.subscribe("user_login", handle_user_login_event)
