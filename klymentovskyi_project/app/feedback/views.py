from flask import render_template, request, redirect, url_for, flash
from app import db

from . import feedback_blueprint
from .forms import FeedBackForm
from .models import FeedBack

@feedback_blueprint.route('/', methods=["GET", "POST"])
def index():
    form = FeedBackForm()

    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data

        fb = FeedBack(email=email, message=message)
        db.session.add(fb)
        db.session.commit()
        flash("Thank you. We noted your feedback.", "success")
        return redirect(url_for(".index"))
    elif request.method == "POST":
        flash("Please resolve the mistakes and resend the form.", "danger")

    feedbacks_list = FeedBack.query.all()
    return render_template("feedback/index.html", form=form, feedbacks_list=feedbacks_list)
