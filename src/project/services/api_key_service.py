from src.project.exceptions import CustomException
from src.project.helpers.base_service import BaseService
from src.project.repositories import ApiKeyRepository


class ApiKeyService(BaseService):
    """
    ApiKey services
    """

    repository = ApiKeyRepository

    @classmethod
    def get_actives_keys(cls):
        return cls.get_model().query.filter(cls.get_model().is_active.is_(True)).all()
