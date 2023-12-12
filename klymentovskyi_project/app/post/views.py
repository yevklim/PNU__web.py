from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db

from . import post_blueprint
from .forms import PostCreationForm, PostUpdateForm, PostDeletionForm, CategoryCreationForm, CategoryUpdateForm, TagCreationForm, TagUpdateForm
from .models import Post, Category, Tag


@post_blueprint.route('/', methods=["GET"])
@post_blueprint.route('/list', methods=["GET"])
def list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)
    all_posts = Post.visible_posts(page, per_page)
    return render_template("post/list.html", all_posts=all_posts)


@post_blueprint.route('/create', methods=["GET", "POST"])
@login_required
def create():
    form = PostCreationForm()
    if form.validate_on_submit():
        category_id = form.category.data
        if category_id == -1:
            category_id = None
        post = Post(title=form.title.data, text=form.text.data, category_id=category_id,
                    tags=[Tag.query.get(id) for id in form.tags.data],
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
@login_required
def update(id):
    form = PostUpdateForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.enabled = form.enabled.data
        category_id = form.category.data
        if category_id == -1:
            category_id = None
        post.category_id = category_id
        post.tags = [Tag.query.get(id) for id in form.tags.data]
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
        form.category.data = post.category_id or -1
        form.tags.data = [tag.id for tag in post.tags]
    return render_template("post/update.html", form=form)


@post_blueprint.route('/<int:id>/delete', methods=["GET", "POST"])
@login_required
def delete(id):
    form = PostDeletionForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted", "info")
        return redirect(url_for('.list'))
    return render_template("post/delete.html", form=form, post=post)

@post_blueprint.route('/category/', methods=["GET", "POST"])
@post_blueprint.route('/category/list', methods=["GET", "POST"])
def category_list():
    form = CategoryCreationForm()

    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash("New category has been added", "success")
        return redirect(url_for('.category_list'))
    elif request.method == "POST":
        flash("New category cannot be created until you resolve the mistake", "danger")

    all_categories = Category.query.all()
    return render_template("post-categories/list.html", all_categories=all_categories, creation_form=form)

@post_blueprint.route('/category/<int:id>/update', methods=["GET", "POST"])
@login_required
def category_update(id):
    category = Category.query.get_or_404(id)
    form = CategoryUpdateForm(category=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("The category has been updated", "success")
        return redirect(url_for('.category_update', id=id))
    elif request.method == "POST":
        flash("The category cannot be updated until you resolve the mistake", "danger")
    else:
        form.name.data = category.name
    return render_template("post-categories/update.html", form=form)

@post_blueprint.route('/category/<int:id>/delete', methods=["POST"])
@login_required
def category_delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash(f"The category \"{category.name}\" has been deleted", "info")
    return redirect(url_for('.category_list'))

@post_blueprint.route('/tag/', methods=["GET", "POST"])
@post_blueprint.route('/tag/list', methods=["GET", "POST"])
def tag_list():
    form = TagCreationForm()

    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash("New tag has been added", "success")
        return redirect(url_for('.tag_list'))
    elif request.method == "POST":
        flash("New tag cannot be created until you resolve the mistake", "danger")

    all_tags = Tag.query.all()
    return render_template("post-tags/list.html", all_tags=all_tags, creation_form=form)

@post_blueprint.route('/tag/<int:id>/update', methods=["GET", "POST"])
@login_required
def tag_update(id):
    tag = Tag.query.get_or_404(id)
    form = TagUpdateForm(tag=tag)
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.commit()
        flash("The tag has been updated", "success")
        return redirect(url_for('.tag_update', id=id))
    elif request.method == "POST":
        flash("The tag cannot be updated until you resolve the mistake", "danger")
    else:
        form.name.data = tag.name
    return render_template("post-tags/update.html", form=form)

@post_blueprint.route('/tag/<int:id>/delete', methods=["POST"])
@login_required
def tag_delete(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"The tag \"{tag.name}\" has been deleted", "info")
    return redirect(url_for('.tag_list'))
