from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

#########################
# All Schemas for Users #
#########################

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

########################
# All schemas for Auth #
########################

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

########################
# All schemas for post #
########################

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse 

    # This converts the SQLAlchemy ORM model into a python dict
    # so that it can be read by pydantic
    class Config:
        orm_mode = True

class PostResponseVotes(BaseModel):
    Post: PostResponse
    votes: int

    # This converts the SQLAlchemy ORM model into a python dict
    # so that it can be read by pydantic
    class Config:
        orm_mode = True

########################
# All schemas for vote #
########################
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)
