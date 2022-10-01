import logging
from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.response import CustomResponse
from models.user import User
from schemas.user import UserBase


# noinspection PyShadowingBuiltins
class UserRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    # Create
    def add(self, item: UserBase) -> CustomResponse:
        with self.session_factory() as session:
            try:
                user = User(**item.dict())
                session.add(user)
                session.commit()
                session.refresh(user)
                return CustomResponse(user)
            except IntegrityError:
                logging.info("Duplicated Error")
                session.rollback()
                return CustomResponse({}, False, f"Duplicated Error {item.json()}")

    # Read
    def get(self, id: int) -> CustomResponse:
        with self.session_factory() as session:
            user = session.query(User).get(id)
            if not user:
                return CustomResponse({}, False, f"User with id {id} not found")
            else:
                return CustomResponse(user)

    def get_by_username(self, username: str) -> CustomResponse:
        with self.session_factory() as session:
            user = session.query(User).filter(User.username.like(username)).first()
            if not user:
                return CustomResponse({}, False, f"User with name {username} not found")
            else:
                return CustomResponse(user)

    # Update
    def update(self, id: int, item: UserBase) -> CustomResponse:
        with self.session_factory() as session:
            user_query = session.query(User).filter(User.id == id)
            if not user_query.first():
                return CustomResponse({}, False, f"User with id {id} not found")
            user_query.update(item.dict())
            session.commit()
            session.refresh(user_query.first())
            return CustomResponse(user_query.first())

    # Delete
    def delete(self, id: int) -> CustomResponse:
        with self.session_factory() as session:
            user = session.query(User).get(id)
            if not user:
                return CustomResponse({}, False, f"User with id {id} not found")
            session.delete(user)
            session.commit()
            return CustomResponse()
