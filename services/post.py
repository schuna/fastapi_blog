from typing import Iterator

from common.response import CustomResponse
from models.post import Post
from repositories.post import PostRepository
from schemas.post import PostBase


# noinspection PyShadowingBuiltins
class PostService:
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    def create_post(self, item: PostBase) -> CustomResponse:
        return self.post_repository.add(item)

    def get_post(self, id: int) -> CustomResponse:
        return self.post_repository.get(id)

    def get_posts(self) -> Iterator[Post]:
        return self.post_repository.get_all()

    def update_post(self, id: int, item: PostBase) -> CustomResponse:
        return self.post_repository.update(id, item)

    def delete_post(self, id: int) -> CustomResponse:
        return self.post_repository.delete(id)
