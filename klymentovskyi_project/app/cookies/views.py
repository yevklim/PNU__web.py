from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required

from . import cookies_blueprint

@cookies_blueprint.route('/', methods=["GET", "POST"])
@login_required
def index():
    return render_template("cookies/index.html")

@cookies_blueprint.route('/setcookie', methods=["POST"])
def setcookie():
    response = redirect(url_for(".index"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        value = request.form.get("value", "")
        max_age = request.form.get("max_age", 0, type=int)
        response.set_cookie(key, value, max_age)
        flash(f"Set cookie \"{key}\" to \"{value}\" with max-age \"{max_age}\"", "success")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@cookies_blueprint.route('/deletecookie', methods=["POST"])
def deletecookie():
    response = redirect(url_for(".index"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        response.delete_cookie(key)
        flash(f"Deleted cookie \"{key}\"", "success")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@cookies_blueprint.route('/clearcookies', methods=["POST"])
def clearcookies():
    response = redirect(url_for(".index"))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    flash("Deleted all cookies", "success")
    return response

