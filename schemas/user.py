from datetime import datetime
from typing import List

from pydantic import BaseModel


class Post(BaseModel):
    image_url: str
    title: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str
    posts: List[Post]

    class Config:
        orm_mode = True
