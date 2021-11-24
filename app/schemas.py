
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from sqlalchemy import orm
from datetime import date, datetime

from starlette.requests import empty_receive

from app.database import Base

from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserDisplay(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserDisplay

    #pydantic's way of converting sqlalchemy object into a dict
    class Config:
        orm_mode = True

class PostVotes(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)