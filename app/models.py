from .database import Base
from sqlalchemy import Column, String, Integer

class Repository(Base):
    __tablename__="repositories"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    github_url=Column(String)
    description=Column(String)
    