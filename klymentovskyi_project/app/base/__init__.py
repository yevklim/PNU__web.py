from flask import Blueprint

base_blueprint = Blueprint("base", __name__, template_folder="templates", static_folder="static", url_prefix="/base")

from . import menu
