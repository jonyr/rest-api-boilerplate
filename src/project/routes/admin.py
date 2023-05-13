"""Admin routes."""

from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, EmailField
from wtforms.validators import DataRequired, Length
from src.project.services import auth_service

admin_bp = Blueprint("admin", __name__)


class LoginForm(FlaskForm):
    """
    Login form.

    Attributes:
        email (StringField): Email field.
        password (PasswordField): Password field.
    """

    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Email address", "class": "input is-primary"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Password", "class": "input is-primary"},
    )


class SignupForm(FlaskForm):
    """
    Signup form.

    Attributes:
        name (StringField): Name field.
        email (StringField): Email field.
        password (PasswordField): Password field.
        confirm_password (PasswordField): Confirm password field.
        agree_terms (BooleanField): Agree terms field.
    """

    name = StringField(
        "Name",
        validators=[DataRequired()],
        description="Enter your name",
        render_kw={"placeholder": "Name", "class": "input is-primary"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired()],
        description="Enter your email address",
        render_kw={"placeholder": "Email address", "class": "input is-primary"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
        description="Enter your password",
        render_kw={"placeholder": "Password", "class": "input is-primary"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired()],
        description="Confirm your password",
        render_kw={"placeholder": "Confirm password", "class": "input is-primary"},
    )
    agree_terms = BooleanField("I accept the Terms and Conditions", validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    """
    Reset password form.

    Attributes:
        email (StringField): Email field.
    """

    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Email address", "class": "input is-primary"},
    )


@admin_bp.route("/login", methods=["GET", "POST"])
def login_form():
    """
    Get login form.

    Returns:
        str: Rendered template.
    """
    form = LoginForm()

    if request.method == "POST" and form.validate():
        return "Form submitted successfully!"

    # form.email.errors = ["Invalid email or password"]
    # form.password.errors = ["Invalid email or password"]

    return render_template("login.jinja", form=form)


@admin_bp.route("/signup", methods=["GET", "POST"])
def signup_form():
    """
    Get signup form.

    Returns:
        str: Rendered template.
    """
    form = SignupForm()

    if request.method == "POST" and form.validate():
        return "Form submitted successfully!"

    return render_template("signup.jinja", form=form)


@admin_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password_form():
    """
    Get reset password form.

    Returns:
        str: Rendered template.
    """
    form = ResetPasswordForm()

    if request.method == "POST" and form.validate():
        return "Form submitted successfully!"

    return render_template("reset_password.jinja", form=form)


@admin_bp.get("/terms")
def terms():
    return render_template("terms.jinja")
