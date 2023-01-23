from flask import Blueprint, request
from src.project.services import AuthService
from src.project.app import validator, schema, response

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


@auth_bp.post("/auth/tokens")
def create_token():
    return request.json, 201


@auth_bp.put("/auth/tokens")
def refresh_token():
    return request.json, 200


@auth_bp.delete("/auth/tokens")
def delete_token():
    return None, 204


@auth_bp.delete("/auth/passwords")
def delete_password():
    return None, 204


@auth_bp.post("/auth/passowords")
def create_password():
    return request.json, 204
