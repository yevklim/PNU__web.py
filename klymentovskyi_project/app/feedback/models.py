from sqlalchemy import Column, Integer, String
from app import db

class FeedBack(db.Model):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False)
    message = Column(String(768), nullable=True)
