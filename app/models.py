from .database import Base
from sqlalchemy import Column, String, Integer

class Repository(Base):
    __tablename__="repositories"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    github_url=Column(String)
    description=Column(String)
    owner_id = Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)