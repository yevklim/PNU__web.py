from flask import render_template, redirect, url_for, flash
from app import db

from . import todo_blueprint
from .forms import ToDoForm
from .models import ToDo

@todo_blueprint.route("/list", methods=["GET"])
def list():
    form = ToDoForm()
    todo_list = ToDo.query.all()
    return render_template("todo/list.html", form=form, todo_list=todo_list)

@todo_blueprint.route("/add", methods=["POST"])
def add():
    form = ToDoForm()

    if form.validate_on_submit():
        task = form.task.data
        description = form.description.data
        todo = ToDo(task=task, completed=False, description=description)
        db.session.add(todo)
        db.session.commit()
        flash(f"Added \"{task}\" to the ToDo list", "success")
    else:
        flash("Invalid input for a ToDo item", "danger")

    return redirect(url_for(".list"))

@todo_blueprint.route("/update/<int:todo_id>")
def update(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    flash(f"Updated \"{todo.task}\"", "success")
    return redirect(url_for(".list"))

@todo_blueprint.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"Deleted \"{todo.task}\"", "success")
    return redirect(url_for(".list"))
