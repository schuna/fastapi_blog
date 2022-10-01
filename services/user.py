from common.response import CustomResponse
from models.user import User
from schemas.user import UserBase
from repositories.user import UserRepository


# noinspection PyShadowingBuiltins
class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, item: UserBase) -> CustomResponse:
        return self.user_repository.add(item)

    def get_user(self, id: int) -> CustomResponse:
        return self.user_repository.get(id)

    def get_user_by_name(self, username: str) -> CustomResponse:
        return self.user_repository.get_by_username(username)

    def update_user(self, id: int, item: UserBase) -> CustomResponse:
        return self.user_repository.update(id, item)

    def delete_user(self, id: int) -> CustomResponse:
        return self.user_repository.delete(id)
