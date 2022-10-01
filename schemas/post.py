from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    image_url: str
    title: str
    content: str
    user_id: int
    timestamp: Optional[datetime] = datetime.now()


class PostDisplay(BaseModel):
    image_url: str
    title: str
    content: str
    user: User
    timestamp: datetime

    class Config:
        orm_mode = True
