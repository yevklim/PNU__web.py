from sqlalchemy import Column, Integer, String, Boolean
from app import db

class ToDo(db.Model):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    task = Column(String(80), nullable=False)
    description = Column(String(160), nullable=True)
    completed = Column(Boolean(), nullable=True)
