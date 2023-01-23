from src.project.helpers.base_repository import BaseRepository
from src.project.models import User


class AuthRepository(BaseRepository):

    model = User
