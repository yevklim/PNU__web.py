from app import db, bcrypt
import sqlalchemy as sa

class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(20), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    image_file = sa.Column(sa.String(20), nullable=False, default="default.jpg")
    password_hash = sa.Column(sa.String(128))

    @property
    def password(self):
        """
        Password cannot be accessed
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Store the password's hash
        """
        # TODO:
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        """
        Match a password against the password's hash
        """
        # TODO:
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
class ToDo(db.Model):
    __tablename__ = "todo"
    id = sa.Column(sa.Integer, primary_key=True)
    task = sa.Column(sa.String(80), nullable=False)
    description = sa.Column(sa.String(160), nullable=True)
    completed = sa.Column(sa.Boolean(), nullable=True)

class FeedBack(db.Model):
    __tablename__ = "feedback"
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(256), nullable=False)
    message = sa.Column(sa.String(768), nullable=True)
