from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List, Optional
from datetime import datetime

class TagBase(BaseModel):
    name: str
    category: Optional[str] = None

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    count: int
    created_at: datetime

    class Config:
        from_attributes = True

class ImageBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ImageCreate(ImageBase):
    url: HttpUrl
    tags: Optional[List[str]] = []

class Image(ImageBase):
    id: int
    url: HttpUrl
    source_url: Optional[HttpUrl]
    width: Optional[int]
    height: Optional[int]
    format: Optional[str]
    created_at: datetime
    updated_at: datetime
    tags: List[Tag]
    ai_description: Optional[str]
    ai_score: Optional[float]

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None