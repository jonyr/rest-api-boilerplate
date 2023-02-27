from src.project.libs.email import send_email
from src.project.app import event
from src.project.helpers import generate_url


def handle_user_register_event(user):
    # TODO: sends the email using Amazon SES
    send_email(user.first_name, user.email, "Welcome", "Your password is PEPE")


def handle_user_login_event(user):
    # TODO: sends the email using Amazon SES
    send_email(user.first_name, user.email, "Login Data", f"Login Counts {user.sign_in_count}")


def handle_user_password_reset(user):
    send_email(
        user.first_name,
        user.email,
        "Password Reset",
        f"{user.encode()}",
    )


def setup_email_event_handlers():
    event.subscribe("user_registered", handle_user_register_event)
    event.subscribe("user_login", handle_user_login_event)
    event.subscribe("password_reset", handle_user_password_reset)
