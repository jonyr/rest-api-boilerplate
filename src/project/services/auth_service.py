from flask import request
from src.project.helpers.base_service import BaseService
from src.project.repositories import AuthRepository
from src.project.exceptions import CustomException


class AuthService(BaseService):
    """
    Auth services
    """

    repository = AuthRepository

    @classmethod
    def post(cls, payload: dict = None, commit: bool = True, **kwargs):

        payload = payload or request.get_json()

        if cls.exists(payload.get("email", "").lower()):
            raise CustomException("A resource with the email already exist")

        obj = cls.deserialize_using(payload, "RegistrationSchema", unknown="exclude")

        if commit:
            cls.commit()

        return obj

    @classmethod
    def exists(cls, email: str):
        test = cls.repository.exists([("email", "eq", email, "default")])
        return test
