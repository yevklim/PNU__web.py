from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
import sqlalchemy as sa
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


class Post(db.Model):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    text = Column(String(1024), nullable=False)
    created = Column(DateTime(True), nullable=False, default=datetime.now)
    type = Column(Enum(EnumType), default='other')
    enabled = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.created}', '{self.title}')"

    def visible_posts():
        try:
            current_user_id = current_user.id
        except:
            current_user_id = None

        if current_user_id:
            query = sa.select(Post).where((Post.enabled == True).__or__(Post.user_id == current_user_id))
        else:
            query = sa.select(Post).where((Post.enabled == True))

        return db.session.execute(query).scalars()
