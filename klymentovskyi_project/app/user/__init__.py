from flask import Blueprint

user_blueprint = Blueprint("user", __name__, template_folder="templates", static_folder="static", url_prefix="/user")

from . import views
