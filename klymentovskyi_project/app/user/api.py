from flask import Blueprint
user_api_blueprint = Blueprint("user", __name__, url_prefix="/user")

from flask import request, jsonify, current_app, has_request_context
from datetime import datetime, timedelta
from werkzeug.local import LocalProxy
from functools import wraps
import jwt

from .models import User

def _get_token():
    if has_request_context():
        token = request.headers.get("Authorization")

        return token

    return None

jwt_token = LocalProxy(_get_token)

def _get_payload_and_error():
    cache = dict(
        token = None,
        payload = None,
        error = None
    )

    def get(cache: dict, prop: str):
        if not jwt_token:
            return None
        if jwt_token != cache["token"]:
            cache["token"] = _get_token()
            cache["payload"], cache["error"] = parse_token(cache["token"])
        return cache[prop]

    return LocalProxy(lambda: get(cache, "payload")), LocalProxy(lambda: get(cache, "error"))

jwt_payload, jwt_error = _get_payload_and_error()

def generate_token(sub: str | int):
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "sub": sub
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token

def parse_token(token: str):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Expired token"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

def token_required(use_jsonify = True):
    def inner(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not jwt_token:
                response = {
                    "errorMessage": "Token is missing",
                }
                code = 401
                if use_jsonify:
                    return jsonify(response), code
                else:
                    return response, code

            if jwt_error:
                response = {
                    "errorMessage": jwt_error._get_current_object()
                }
                code = 401
                if use_jsonify:
                    return jsonify(response), code
                else:
                    return response, code

            return f(*args, **kwargs)

        return decorated
    return inner

@user_api_blueprint.route('/ping', methods=["GET", "POST"])
@token_required()
def ping():
    return "pong"

@user_api_blueprint.route('/login', methods=["POST"])
def login():
    post: dict | None = request.get_json(silent=True)

    if post is None:
        return jsonify(errorMessage="JSON payload must be provided"), 400

    validation_errors = []

    email: str = post.get("email")
    if not email:
        validation_errors.append({ "field": "email", "error": "Required" })
    elif not isinstance(email, str):
        validation_errors.append({ "field": "email", "error": "Must be a string" })
    elif len(email) > 120:
        validation_errors.append({ "field": "email", "error": "Max length is 120" })

    password: str = post.get("password")
    if not password:
        validation_errors.append({ "field": "password", "error": "Required" })
    elif not isinstance(password, str):
        validation_errors.append({ "field": "password", "error": "Must be a string" })

    if len(validation_errors) > 0:
        return jsonify(errorMessage="Invalid JSON payload has been provided", validationErrors=validation_errors), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.verify_password(password):
        return jsonify(errorMessage="Incorrect email or password"), 401

    return generate_token(email), 200
