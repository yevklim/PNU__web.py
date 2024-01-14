from flask import Blueprint
todo_api_blueprint = Blueprint("todo", __name__, url_prefix="/todo")

from flask import request, jsonify
from app import db

from app.user.api import token_required

from .models import ToDo

@todo_api_blueprint.route('/ping', methods=["GET", "POST"])
def ping():
    return "pong"

@todo_api_blueprint.route("/", methods=["GET"])
def list():
    todo_list = ToDo.query.all()
    return jsonify([
        todo.as_dict() for todo in todo_list
    ]), 200

@todo_api_blueprint.route("/", methods=["POST"])
@token_required()
def add():
    post: dict | None = request.get_json(silent=True)

    if post is None:
        return jsonify(errorMessage="JSON payload must be provided"), 400

    validation_errors = []

    task: str = post.get("task")
    if not task:
        validation_errors.append({ "field": "task", "error": "Required" })
    elif not isinstance(task, str):
        validation_errors.append({ "field": "task", "error": "Must be a string" })
    elif len(task) > 80:
        validation_errors.append({ "field": "task", "error": "Max length is 80" })

    description: str = post.get("description")
    if description is None:
        description = ""
    elif not isinstance(description, str):
        validation_errors.append({ "field": "description", "error": "Must be a string" })
    elif len(description) > 160:
        validation_errors.append({ "field": "description", "error": "Max length is 160" })

    completed: bool = post.get("completed")
    if completed is None:
        completed = False
    elif not isinstance(completed, bool):
        validation_errors.append({ "field": "completed", "error": "Must be a boolean" })

    if len(validation_errors) > 0:
        return jsonify(errorMessage="Invalid JSON payload has been provided", validationErrors=validation_errors), 400

    todo = ToDo(task=task, completed=completed, description=description)
    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.as_dict()), 200

@todo_api_blueprint.route("/<int:todo_id>", methods=["GET"])
def get(todo_id: int):
    todo: ToDo = ToDo.query.get(todo_id)
    if todo is None:
        return jsonify(errorMessage="Requested todo item has not been found"), 404

    return jsonify(todo.as_dict()), 200

@todo_api_blueprint.route("/<int:todo_id>", methods=["PUT"])
@token_required()
def update(todo_id):
    todo: ToDo = ToDo.query.get(todo_id)
    if todo is None:
        return jsonify(errorMessage="Requested todo item has not been found"), 404
    todo.completed = not todo.completed
    db.session.commit()

    return jsonify(todo.as_dict()), 200

@todo_api_blueprint.route("/<int:todo_id>", methods=["DELETE"])
@token_required()
def delete(todo_id):
    todo: ToDo = ToDo.query.get(todo_id)
    if todo is None:
        return jsonify(errorMessage="Requested todo item has not been found"), 404
    db.session.delete(todo)
    db.session.commit()

    return jsonify(todo.as_dict()), 200
