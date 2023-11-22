from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
import enum
from datetime import datetime
from app import db
from app.user.models import User

class EnumType(enum.Enum):
    news = 1
    publication = 2
    other = 3

User.posts = db.relationship('Post', backref='person', lazy=True)
class Post(db.Model):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    text = Column(String(1024), nullable=False)
    created = Column(DateTime(True), nullable=False, default=datetime.now())
    type = Column(Enum(EnumType), default='other')
    enabled = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.created}', '{self.title}')"
