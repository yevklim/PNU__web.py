from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = b"su7sinADFC6v4n_!6jVQqZ.YE67DYpP4"
app.config.from_object("config")
login_manager = LoginManager(app);
login_manager.login_view = "login"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "info"

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
with app.app_context():
    db.create_all()

from app import views
