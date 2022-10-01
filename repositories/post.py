import logging
from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.response import CustomResponse
from models.post import Post
from schemas.post import PostBase


# noinspection PyShadowingBuiltins
class PostRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    # Create
    def add(self, item: PostBase) -> CustomResponse:
        with self.session_factory() as session:
            try:
                post = Post(**item.dict())
                session.add(post)
                session.commit()
                session.refresh(post)
                return CustomResponse(post)
            except IntegrityError:
                logging.info("Duplicated Error")
                session.rollback()
                return CustomResponse({}, False, f"Duplicated Error {item.json()}")

    # Read
    def get(self, id: int) -> CustomResponse:
        with self.session_factory() as session:
            post = session.query(Post).get(id)
            if not post:
                return CustomResponse({}, False, f"Post with id {id} not found")
            else:
                return CustomResponse(post)

    def get_all(self) -> Iterator[Post]:
        with self.session_factory() as session:
            return session.query(Post).all()

    # Update
    def update(self, id: int, item: PostBase) -> CustomResponse:
        with self.session_factory() as session:
            post_query = session.query(Post).filter(Post.id == id)
            if not post_query.first():
                return CustomResponse({}, False, f"Post with id {id} not found")
            post_query.update(item.dict())
            session.commit()
            session.refresh(post_query.first())
            return CustomResponse(post_query.first())

    # Delete
    def delete(self, id: int) -> CustomResponse:
        with self.session_factory() as session:
            post = session.query(Post).get(id)
            if not post:
                return CustomResponse({}, False, f"Post with id {id} not found")
            session.delete(post)
            session.commit()
            return CustomResponse()
