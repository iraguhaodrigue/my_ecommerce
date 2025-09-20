from pydantic import BaseModel
from typing import List


# -------- Blog --------
class BlogBase(BaseModel):
    title: str
    body: str


class BlogCreate(BlogBase):
    pass


class ShowBlog(BlogBase):
    class Config:
        orm_mode = True


# -------- User --------
class UserBase(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[ShowBlog] = []   # Show user with blogs

    class Config:
        orm_mode = True
