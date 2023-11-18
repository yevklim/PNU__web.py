from flask import Blueprint

cookies_blueprint = Blueprint("cookies", __name__, template_folder="templates", url_prefix="/cookies")

from . import views
