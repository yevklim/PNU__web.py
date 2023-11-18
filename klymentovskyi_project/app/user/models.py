from sqlalchemy import Column, Integer, String, DateTime
from app import db, bcrypt, login_manager
from . import user_blueprint

from os import path
from secrets import token_hex
from PIL import Image
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default="default.jpg")
    about_me = Column(String(512), nullable=True, default="")
    last_seen = Column(DateTime(True), nullable=True)
    password_hash = Column(String(128))

    @property
    def image_filename(self):
        return "upload/avatars/" + self.image_file

    def new_image_file(self, form_file):
        random_hex = token_hex(8)
        f_ext = path.splitext(form_file.filename)[1]
        f_name = random_hex + f_ext
        f_path = path.join(user_blueprint.root_path, "static/upload/avatars", f_name)

        img = Image.open(form_file)
        img.thumbnail((200, 200))
        img.save(f_path)

        self.image_file = f_name

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
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        """
        Match a password against the password's hash
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
