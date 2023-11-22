from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from app import db

from . import post_blueprint
from .forms import PostCreationForm, PostUpdateForm, PostDeletionForm
from .models import Post


@post_blueprint.route('/', methods=["GET"])
@post_blueprint.route('/list', methods=["GET"])
def list():
    all_posts = Post.visible_posts().all()
    return render_template("post/list.html", all_posts=all_posts)


@post_blueprint.route('/create', methods=["GET", "POST"])
def create():
    form = PostCreationForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.text.data,
                    type=form.type.data, enabled=form.enabled.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been published", "success")
        return redirect(url_for('.post', id=post.id))
    elif request.method == "POST":
        flash("Your post cannot be published until you resolve the mistakes", "danger")
    return render_template("post/create.html", form=form)


@post_blueprint.route('/<int:id>', methods=["GET"])
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post/post.html", post=post)


@post_blueprint.route('/<int:id>/update', methods=["GET", "POST"])
def update(id):
    form = PostUpdateForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.enabled = form.enabled.data
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for('.post', id=id))
    elif request.method == "POST":
        flash("Your post cannot be updated until you resolve the mistakes", "danger")
    else:
        form.title.data = post.title
        form.text.data = post.text
        form.type.data = post.type
        form.enabled.data = post.enabled
    return render_template("post/create.html", form=form)


@post_blueprint.route('/<int:id>/delete', methods=["GET", "POST"])
def delete(id):
    form = PostDeletionForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted", "info")
        return redirect(url_for('.list'))
    return render_template("post/delete.html", form=form, post=post)

