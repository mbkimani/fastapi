from datetime import timezone
from os import terminal_size
from typing import ClassVar
from pydantic.main import BaseModel
from pydantic.tools import T
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import _corresponding_column_or_error
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from .database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published=Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False )

    owner = relationship("User")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable= False, )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
