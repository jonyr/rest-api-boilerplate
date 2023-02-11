from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.project.app import response, schema, validator
from src.project.services import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/auth/registrations")
@validator(
    "json",
    {
        "email": ["required", "max:150"],
        "password": ["required", "min:8", "max:128"],
    },
)
def create_registration():
    registration = AuthService.post()

    registration = schema.dump(
        registration,
        name="User",
    )

    return response.build(registration, 201)


@auth_bp.post("/auth/activations")
@validator(
    "json",
    {
        "email": ["required", "max:150"],
        "code": ["required", "min:6", "max:10"],
    },
)
def activate_registration():
    activation = AuthService.activate_registration()
    return request.json, 201


@auth_bp.post("/auth/tokens")
def create_token():
    tokens = AuthService.login()
    return response.build(tokens)


@auth_bp.put("/auth/tokens")
def refresh_token():
    return request.json, 200


@auth_bp.delete("/auth/tokens")
def delete_token():
    return None, 204


@auth_bp.delete("/auth/passwords")
@validator(
    "json",
    {"email": ["required", "max:150"]},
)
def delete_password():
    return None, 204


@auth_bp.post("/auth/passwords")
def create_password():
    return request.json, 204


@auth_bp.get("/auth/me")
@jwt_required()
def get_my_info():

    identity = get_jwt_identity()
    user = AuthService.me(identity)
    return response.build(user)
