from __future__ import annotations
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from flask import abort
from flask_login import current_user
import enum
from datetime import datetime
from app import db
from app.user.models import User


class EnumType(enum.Enum):
    news = 1
    publication = 2
    other = 3

    @property
    def label(self):
        match self:
            case EnumType.news:
                return 'News'
            case EnumType.publication:
                return 'Publication'
            case EnumType.other:
                return 'Other'


User.posts = db.relationship('Post', backref='user', lazy=True)


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(48), nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)

post_tag_m2m = db.Table(
    "post_tag",
    Column("post_id", ForeignKey("post.id", name="fk_post_tag_m2m_post_id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", name="fk_post_tag_m2m_tag_id"), primary_key=True),
)

class Tag(db.Model):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(48), nullable=False)
    posts: Mapped[List[Post]] = db.relationship(secondary=post_tag_m2m, back_populates="tags")


class Post(db.Model):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    text = Column(String(1024), nullable=False)
    created = Column(DateTime(True), nullable=False, default=datetime.now)
    type = Column(Enum(EnumType), default='other')
    enabled = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id, name="fk_post_category_id"), nullable=True)
    tags: Mapped[List[Tag]] = db.relationship('Tag', secondary=post_tag_m2m, back_populates="posts")

    def __repr__(self):
        return f"Post('{self.id}', '{self.created}', '{self.title}')"

    def get_visible_post(id: int) -> Post | None:
        post = Post.query.get(id)
        if post is None or post.enabled:
            return post

        if current_user.is_authenticated and current_user.id == post.user_id:
            return post

        return None

    def get_visible_post_or_abort(id: int) -> Post:
        post = Post.query.get(id)

        if post is None:
            abort(404)

        if not post.enabled:

            if not current_user.is_authenticated:
                abort(401)

            if current_user.id != post.user_id:
                abort(403)

        return post

    def visible_posts(page: int, per_page: int = 5):
        try:
            current_user_id = current_user.id
        except:
            current_user_id = None

        if current_user_id:
            query = sa.select(Post).where(
                (Post.enabled == True).__or__(Post.user_id == current_user_id))
            query = Post.query.where((Post.enabled == True).__or__(Post.user_id == current_user_id))
        else:
            query = sa.select(Post).where((Post.enabled == True))
            query = Post.query.where((Post.enabled == True))

        return query.order_by(Post.created.desc()).paginate(page=page, per_page=per_page)

