from src.project.helpers.base_repository import BaseRepository
from src.project.models import ApiKey


class ApiKeyRepository(BaseRepository):

    model = ApiKey
