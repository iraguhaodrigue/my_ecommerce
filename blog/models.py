from sqlalchemy import Integer, Column, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))   # FIXED here ✅
    Creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)  # add index is good practice
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    blogs = relationship("Blog", back_populates="Creator")
