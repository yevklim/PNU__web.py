from flask import Flask

app = Flask(__name__)
app.secret_key = b"su7sinADFC6v4n_!6jVQqZ.YE67DYpP4"

from app import views
