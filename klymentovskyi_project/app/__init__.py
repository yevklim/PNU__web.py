from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = b"su7sinADFC6v4n_!6jVQqZ.YE67DYpP4"
app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
with app.app_context():
    db.create_all()

from app import views
