
from sqlalchemy import Column, ForeignKey, Integer, String

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))