import json
from os import uname, path
from time import time, ctime
from flask import request, render_template, redirect, url_for, session, make_response, flash, get_flashed_messages

from app.data import skills_list, projects_list
system_info = f"{uname().sysname} {uname().release} {uname().machine}"

from app import app, db, forms, models, credentials

def _save_user_session(username, remember):
    print(f"remember {remember}")
    session["username"] = username
    if remember:
        session["expires"] = time() + 60 * 60 * 24 * 92 # 3 months (92 days)
    else:
        session["expires"] = time() + 60 * 15 # 15 minutes

@app.before_request
def check_for_expired_session():
    now = time()
    if session.get("expires", now) < now:
        session.clear()
        flash("Your session expired. Please sign in again.", "warning")

@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    return render_template("home.html", system_info=system_info, user_agent=request.user_agent, now=ctime(time()))

@app.route('/projects', methods=["GET"])
def projects():
    return render_template("projects.html", projects_list=projects_list)

@app.route('/skills/', methods=["GET"])
@app.route('/skills/<int:idx>', methods=["GET"])
def skills(idx=None):
    if idx is not None:
        return render_template("skill.html", skills_list=skills_list, idx=idx)
    else:
        return render_template("skills.html", skills_list=skills_list)

@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        user = credentials.get_user_credentials(username)
        username_match = user["username"] == username
        password_match = user["password"] == password
        if username_match and password_match:
            response = redirect(url_for("info"))
            _save_user_session(username, remember)
            flash("Successfully signed in", "success")
            return response
        else:
            flash("Incorrect username or password", "danger")

    return render_template("login.html", form=form)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    response = redirect(url_for("login"))
    session.clear()
    return response

@app.route('/info', methods=["GET", "POST"])
def info():
    change_password_form = forms.ChangePasswordForm()
    if not "username" in session or not session["username"]:
        return redirect(url_for("login"))

    if request.args.get("action", "") == "change_password":
        success = change_password(change_password_form)
        if success:
            return redirect(url_for("info"))

    return render_template("info.html", change_password_form=change_password_form)

def change_password(form):
    if not form.validate_on_submit():
        return

    current_password = form.current_password.data
    new_password = form.new_password.data

    username = session["username"]
    user = credentials.get_user_credentials(username)
    if user is None:
        flash(f"User \"{username}\" doesn't exist anymore", "danger")
    elif current_password == user["password"]:
        if credentials.change_user_password(user, new_password):
            flash("Successfully changed password", "success")
            return True
        flash("Failed to change password", "danger")
    else:
        flash("Incorrect password was provided", "danger")

    return False

@app.route('/setcookie', methods=["POST"])
def setcookie():
    response = redirect(url_for("info"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        value = request.form.get("value", "")
        max_age = request.form.get("max_age", 0, type=int)
        response.set_cookie(key, value, max_age)
        flash(f"Set cookie \"{key}\" to \"{value}\" with max-age \"{max_age}\"", "success")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@app.route('/deletecookie', methods=["POST"])
def deletecookie():
    response = redirect(url_for("info"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        response.delete_cookie(key)
        flash(f"Deleted cookie \"{key}\"", "success")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@app.route('/clearcookies', methods=["POST"])
def clearcookies():
    response = redirect(url_for("info"))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    flash("Deleted all cookies", "success")
    return response

@app.route('/todos', methods=["GET"])
def todos():
    form = forms.ToDoForm()
    todo_list = models.ToDo.query.all()
    return render_template("todos.html", form=form, todo_list=todo_list)

@app.route('/todo-add', methods=["POST"])
def todo_add():
    form = forms.ToDoForm()

    if form.validate_on_submit():
        task = form.task.data
        description = form.description.data
        todo = models.ToDo(task=task, completed=False, description=description)
        db.session.add(todo)
        db.session.commit()
        flash(f"Added \"{task}\" to the ToDo list", "success")
    else:
        flash("Invalid input for a ToDo item", "danger")

    return redirect(url_for("todos"))

@app.route('/todo-update/<int:todo_id>')
def todo_update(todo_id):
    todo = models.ToDo.query.get_or_404(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    flash(f"Updated \"{todo.task}\"", "success")
    return redirect(url_for("todos"))

@app.route('/todo-delete/<int:todo_id>')
def todo_delete(todo_id):
    todo = models.ToDo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash(f"Deleted \"{todo.task}\"", "success")
    return redirect(url_for("todos"))

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    form = forms.FeedBackForm()

    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data

        fb = models.FeedBack(email=email, message=message)
        db.session.add(fb)
        db.session.commit()
        flash("Thank you. We noted your feedback.", "success")
    elif request.method == "POST":
        flash("Please resolve the mistakes and resend the form.", "danger")

    feedbacks_list = models.FeedBack.query.all()
    return render_template("feedback.html", form=form, feedbacks_list=feedbacks_list)
