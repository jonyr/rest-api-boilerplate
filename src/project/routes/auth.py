from flask import Blueprint, current_app, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.project.app import api, schema, validator
from src.project.services import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/auth/registrations")
@validator(
    "json",
    {
        "first_name": ["required", "min:2", "max:150"],
        "email": ["required", "max:150"],
        "password": ["required", "min:8", "max:128"],
    },
)
def create_registration():
    """ """
    user = AuthService.post()

    registration = schema.dump(
        user,
        name="User",
        only=(
            "id",
            "email",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
        ),
    )

    meta = None if current_app.config.get("ENV") == "production" else {"code": user.activation_code}

    return api.response(registration, meta)


@auth_bp.post("/auth/activations")
@validator(
    "json",
    {
        "email": ["required", "max:150"],
        "code": ["required", "min:6", "max:10"],
    },
)
def activate_registration():
    """
    Activates a user.
    """
    user = AuthService.activate_registration()
    return api.response(user, code=200)


@auth_bp.post("/auth/tokens")
def create_token():
    """
    Creates an access token for a give pair of credentials.
    """
    tokens = AuthService.login()
    return api.response(tokens)


@auth_bp.put("/auth/tokens")
@jwt_required(refresh=True)
def refresh_token():
    """
    Refreshes an access token.
    """
    tokens = AuthService.refresh()
    return api.response(tokens)


@auth_bp.delete("/auth/tokens")
@jwt_required(verify_type=False)
def delete_token():
    """
    Destroys access token.
    """
    AuthService.logout()
    return api.response(None)


@auth_bp.post("/auth/passwords/reset")
@validator(
    "json",
    {"email": ["required", "max:150"]},
)
def request_password_clean():
    """
    Requests a password reset.
    """
    token = AuthService.request_password_reset()
    meta = None if current_app.config.get("ENV") == "production" else {"token": token}
    return api.response(None, meta)


@auth_bp.post("/auth/passwords")
@validator(
    "json",
    {
        "token": ["required"],
        "password": ["required", "min:8", "max:128"],
    },
)
def update_cleaned_password():
    """
    Updates a password.
    """
    AuthService.password_update()
    return api.response(None)


@auth_bp.get("/auth/me")
@jwt_required()
def get_my_info():
    """
    Gets information about me.
    """
    identity = get_jwt_identity()
    user = AuthService.me(identity)
    return api.response(user)


@auth_bp.get("/users")
def get_users():
    """
    Gets users.
    """
    return render_template("users.html")
