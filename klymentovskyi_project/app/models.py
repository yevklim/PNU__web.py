from app import db
import sqlalchemy as sa

class ToDo(db.Model):
    __tablename__ = "todo"
    id = sa.Column(sa.Integer, primary_key=True)
    task = sa.Column(sa.String(80), nullable=False)
    description = sa.Column(sa.String(160), nullable=True)
    completed = sa.Column(sa.Boolean(), nullable=True)
