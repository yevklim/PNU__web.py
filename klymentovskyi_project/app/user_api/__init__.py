from flask import Blueprint, jsonify
from flask_restful import Api
from .views import RegisterUserApi, UserApi

user_api2_blueprint = Blueprint("user_api2", __name__, url_prefix="/user")
api = Api(user_api2_blueprint)

api.add_resource(RegisterUserApi, "/")
api.add_resource(UserApi, "/<int:id>")

import marshmallow.exceptions
@user_api2_blueprint.app_errorhandler(marshmallow.exceptions.ValidationError)
def handle_marshmallow_validation_error(e: marshmallow.exceptions.ValidationError):
    return jsonify(message="Invalid JSON payload has been provided.", errors=e.normalized_messages()), 400
