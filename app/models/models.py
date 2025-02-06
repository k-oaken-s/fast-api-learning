from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

# 画像とタグの中間テーブル
image_tags = Table(
    'image_tags',
    Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# お気に入り中間テーブル
user_favorites = Table(
    'user_favorites',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship("Image", back_populates="user")
    favorite_images = relationship("Image", secondary=user_favorites, back_populates="favorited_by")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    source_url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    format = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="pending")

    # AI生成されたメタデータ
    ai_description = Column(String, nullable=True)
    ai_score = Column(Float, nullable=True)
    safe_search_adult = Column(String, nullable=True)
    safe_search_violence = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="images")
    tags = relationship("Tag", secondary=image_tags, back_populates="images")
    favorited_by = relationship("User", secondary=user_favorites, back_populates="favorite_images")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
    count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship("Image", secondary=image_tags, back_populates="tags")