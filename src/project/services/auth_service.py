from flask import request
from src.project.helpers.base_service import BaseService
from src.project.repositories import AuthRepository
from src.project.exceptions import CustomException
from src.project.extensions import schema, response, event
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity


class AuthService(BaseService):
    """
    Auth services
    """

    repository = AuthRepository

    @classmethod
    def post(cls, payload: dict = None, commit: bool = True, **kwargs):

        payload = payload or request.get_json()

        if cls.exists(payload.get("email", "missing").lower()):
            raise CustomException("A resource with the email already exist")

        user = cls.deserialize_using(payload, "RegistrationSchema", unknown="exclude")

        if commit:
            cls.commit()

        event.post_event("user_registered", user)

        return user

    @classmethod
    def activate_registration(cls, payload: dict = None):
        payload = payload or request.get_json()

        user = cls.get_model().find_by_email(payload.get("email", "missing").lower())

        if not user:
            raise CustomException("Resource not found", "ResourceNotFound", 404)

        user.validate_activation_code(payload.get("code", ""))

        user.save()

        return {}, 201

    @classmethod
    def reset_password(cls, payload: dict = None):
        payload = payload or request.get_json()

        user = cls.get_model().find_by_email(payload.get("email", "missing").lower())

        if not user:
            raise CustomException("Resource not found", "ResourceNotFound", 404)

        user.validate_activation_code(payload.get("code", ""))

        user.save()

        return {}, 201

    @classmethod
    def exists(cls, email: str):
        return cls.repository.exists([("email", "eq", email, "default")])

    @classmethod
    def login(cls, payload: dict = None):

        payload = payload or request.get_json()

        credentials = schema.load(payload, name="Login")

        user = cls.get_model().find_by_email(credentials["email"])

        event.post_event("user_login", user)

        # invalid credentials
        if not user or not user.authenticated(password=credentials["password"]):
            raise CustomException("Invalid credentials", "InvalidCredentialsError")

        # inactive account or validation code expired
        if not user.is_active:
            if user.activation_code_expired():
                raise CustomException("Activation code has expired", "ExpiredActivationCodeError")
            raise CustomException("Inactive account", "InactiveAccountError")

        claims = dict()

        claims["role"] = "member"

        access_token = create_access_token(
            identity=user.id,
            additional_claims=claims,
            fresh=True,
        )

        refresh_token = create_refresh_token(identity=user.id)

        user.update_activity_tracking()

        return {"access_token": access_token, "refresh_token": refresh_token}

    @classmethod
    def me(cls, identity=None):

        identity = identity or get_jwt_identity()

        user = AuthService.get_model().find_by_id(identity)

        return schema.dump(user, name="User")
