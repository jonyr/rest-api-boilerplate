from datetime import timedelta

from flask import request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, get_jti
from itsdangerous.exc import BadSignature, BadTimeSignature

from src.project.exceptions import CustomException
from src.project.extensions import event, rediscache, response, schema, console
from src.project.helpers.base_service import BaseService
from src.project.helpers import encode_object, decode_string
from src.project.models import Role
from src.project.repositories import AuthRepository


class AuthService(BaseService):
    """
    Auth services
    """

    repository = AuthRepository

    @classmethod
    def post(cls, payload: dict = None, commit: bool = True, **kwargs):

        payload = payload or request.get_json()

        if cls.exists(payload.get("email", "missing").lower()):
            raise CustomException("User already exists")

        user = cls.deserialize_using(payload, "RegistrationSchema", unknown="exclude")

        # sets default role to user
        role = Role.get_default_role()
        user.role_id = role.id

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

        if user.is_active:
            raise CustomException("The account was already active", "AlreadyActive", 400)

        user.validate_activation_code(payload.get("code", ""))

        user.save()

        event.post_event("user_activated", user)

        return schema.dump(
            user,
            name="User",
            only=(
                "first_name",
                "last_name",
                "id",
                "email",
                "updated_at",
            ),
        )

    # @classmethod
    # def reset_password(cls, payload: dict = None):
    #     payload = payload or request.get_json()

    #     user = cls.get_model().find_by_email(payload.get("email", "missing").lower())

    #     if not user:
    #         raise CustomException("Resource not found", "ResourceNotFound", 404)

    #     user.validate_activation_code(payload.get("code", ""))

    #     user.save()

    #     return {}, 201

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

        refresh_token = create_refresh_token(identity=user.id)

        claims = dict()
        claims["role"] = "member"
        claims["rjti"] = get_jti(refresh_token)

        access_token = create_access_token(
            identity=user.id,
            fresh=True,
            additional_claims=claims,
        )

        user.update_activity_tracking()

        return {"access_token": access_token, "refresh_token": refresh_token}

    @classmethod
    def me(cls, identity=None):

        identity = identity or get_jwt_identity()

        user = cls.get_model().find_by_id(identity)

        return schema.dump(user, name="User")

    @classmethod
    def get_by_id(cls, identity=None):
        identity = identity or get_jwt_identity()

        user = cls.get_model().find_by_id(identity)

    @classmethod
    def refresh(cls, identity=None):
        identity = identity or get_jwt_identity()

        user = cls.get_model().find_by_id(identity)

        access_token = create_access_token(
            identity=user.id,
            fresh=False,
        )

        return {"access_token": access_token}

    @classmethod
    def logout(cls):
        """
        Gets the unique identifier of an encoded JWT,
        and sets it in a rediscache service.
        """

        token = get_jwt()
        jti = token.get("jti")
        rjti = token.get("rjti")

        rediscache.set(jti, "", timeout=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"))
        rediscache.set(rjti, "", timeout=current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES"))

    @classmethod
    def request_password_reset(cls, payload: dict = None):
        payload = payload or request.get_json()
        user = cls.get_model().find_by_email(payload["email"].lower())

        if user and user.is_active:
            event.post_event("password_reset", user)
            return user.encode()

    @classmethod
    def password_update(cls, payload: dict = None):

        payload = payload or request.get_json()

        decoded_info = decode_string(
            payload.get("token"),
            expiration=60 * 60 * 24,
        )

        if decoded_info:
            user = cls.get_model().find_by_id(decoded_info["id"])
            user.password = user.encrypt_password(payload.get("password"))
            user.save()

            return True
