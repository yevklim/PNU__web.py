from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from app import db

from . import user_blueprint
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from .models import User

@user_blueprint.after_request
def user_last_seen_update(response):
    if current_user and current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()
    return response

@user_blueprint.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".account"))

    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(username=form.username.data,
                           email=form.email.data,
                           password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}", "success")
        return redirect(url_for(".login"))
    
    return render_template("user/register.html", form=form)

@user_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".account"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user, remember)
            flash("Successfully signed in", "success")
            return redirect(url_for(".account"))
        else:
            flash("Incorrect e-mail or password", "danger")

    return render_template("user/login.html", form=form)

@user_blueprint.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    flash("You have signed out", "info")
    return redirect(url_for(".login"))

@user_blueprint.route('/account', methods=["GET", "POST"])
@login_required
def account():
    action = request.args.get("action", "")
    form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()
    if action == "update_profile" and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if form.picture.data:
            current_user.new_image_file(form.picture.data)
        db.session.commit()
        flash("Your account has been updated.", "success")
        return redirect(url_for(".account"))
    elif action == "change_password" and change_password_form.validate_on_submit():
        current_user.password = change_password_form.new_password.data
        db.session.commit()
        flash("Successfully changed password", "success")
        return redirect(url_for(".account"))
    if action != "update_profile" or request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template("user/account.html", form=form, change_password_form=change_password_form)

@user_blueprint.route('/list')
def list():
    all_users = User.query.all()
    return render_template("user/list.html", all_users=all_users)
