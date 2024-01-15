import pytest
from flask import url_for
from app.post.models import Category, Post, Tag
from app.post.forms import PostCreationForm, PostUpdateForm

from . import client, db_init, user, user_2, authenticated_user, authenticated_user_2, posts, categories, tags

def test_post_list_view_guest(client, db_init):
    response = client.get(url_for('post.list'))
    assert response.status_code == 200
    assert 'Posts' in response.text
    assert 'post/1' in response.text
    assert 'post/2' in response.text
    assert 'post/3' not in response.text

def test_post_list_view(client, db_init, authenticated_user):
    response = client.get(url_for('post.list'))
    assert response.status_code == 200
    assert 'Posts' in response.text
    assert 'post/1' in response.text
    assert 'post/2' in response.text
    assert 'post/3' in response.text

def test_create_post_view_guest(client, db_init):
    response = client.get(url_for('post.create'), follow_redirects=True)
    assert response.status_code == 200
    assert "E-mail" in response.text
    assert "Password" in response.text
    assert "Remember Me" in response.text
    assert "Sign In" in response.text

def test_create_post_view(client, db_init, authenticated_user):
    response = client.get(url_for('post.create'))
    assert response.status_code == 200
    assert "Title" in response.text
    assert "Content" in response.text
    assert "Category" in response.text
    assert "Type" in response.text
    assert "Tags" in response.text
    assert "Enabled" in response.text
    assert "Publish" in response.text

def test_create_post_submit_successful(client, db_init, authenticated_user, tags, categories):
    form = PostCreationForm(title='Post #4',
                            text='Dolor sit amet...',
                            category=categories[2].id,
                            tags=[tag.id for tag in (tags[0], tags[1], tags[2])],
                            type='other',
                            enabled=True)
    response = client.post(url_for('post.create'),
                           data=form.data,
                           follow_redirects=True)
    assert response.status_code == 200
    assert "Your post has been published" in response.text
    assert form.title.data in response.text
    assert form.text.data in response.text
    assert "Visible for everyone" in response.text
    assert "Edit" in response.text
    assert "Delete" in response.text

def test_create_post_submit_failed(client, db_init, authenticated_user):
    form = PostCreationForm(title='',
                            text='',
                            enabled=False)
    response = client.post(url_for('post.create'))
    assert response.status_code == 200
    assert "Your post cannot be published until you resolve the mistakes" in response.text
    assert form.title.data in response.text
    assert form.text.data in response.text
    assert "Title" in response.text
    assert "Content" in response.text
    assert "Category" in response.text
    assert "Type" in response.text
    assert "Tags" in response.text
    assert "Enabled" in response.text
    assert "Publish" in response.text

def test_post_view_guest(client, db_init, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.post', id=post.id))
    assert response.status_code == 200
    assert post.title in response.text
    assert post.text in response.text
    assert "Visible for everyone" not in response.text
    assert "Edit" not in response.text
    assert "Delete" not in response.text

def test_post_view(client, db_init, authenticated_user, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.post', id=post.id))
    assert response.status_code == 200
    assert post.title in response.text
    assert post.text in response.text
    assert "Visible for everyone" in response.text
    assert "Edit" in response.text
    assert "Delete" in response.text

def test_hidden_post_view_guest(client, db_init, posts):
    post = posts[2]
    assert post is not None
    response = client.get(url_for('post.post', id=post.id))
    assert response.status_code == 401

def test_hidden_post_view(client, db_init, authenticated_user, posts):
    post = posts[2]
    assert post is not None
    response = client.get(url_for('post.post', id=post.id))
    assert response.status_code == 200
    assert post.title in response.text
    assert post.text in response.text
    assert "Hidden from others" in response.text
    assert "Edit" in response.text
    assert "Delete" in response.text

def test_update_post_view_guest(client, db_init, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.update', id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert "E-mail" in response.text
    assert "Password" in response.text
    assert "Remember Me" in response.text
    assert "Sign In" in response.text

def test_update_post_view_forbidden(client, db_init, authenticated_user_2, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.update', id=post.id),
                          follow_redirects=True)
    assert response.status_code == 403

def test_update_post_view(client, db_init, authenticated_user, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.update', id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert post.title in response.text
    assert post.text in response.text
    assert "Title" in response.text
    assert "Content" in response.text
    assert "Category" in response.text
    assert "Type" in response.text
    assert "Tags" in response.text
    assert "Enabled" in response.text
    assert "Update" in response.text

def test_update_post_submit_guest(client, db_init, posts):
    post = posts[0]
    assert post is not None
    response = client.post(url_for('post.update', id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert "E-mail" in response.text
    assert "Password" in response.text
    assert "Remember Me" in response.text
    assert "Sign In" in response.text

def test_update_post_submit_forbidden(client, db_init, authenticated_user_2, posts):
    post = posts[0]
    assert post is not None
    response = client.post(url_for('post.update', id=post.id))
    assert response.status_code == 403

def test_update_post_submit_successful(client, db_init, authenticated_user, posts, tags, categories):
    post = posts[0]
    assert post is not None
    form = PostUpdateForm(title='Post #2 (Updated)',
                          text='Dolor Sit Amet Mani...',
                          category=categories[0].id,
                          tags=[tag.id for tag in (tags[0], tags[1], tags[2])],
                          type='publication',
                          enabled=True)
    response = client.post(url_for('post.update', id=post.id),
                           data=form.data,
                           follow_redirects=True)
    assert response.status_code == 200
    assert "Your post has been updated" in response.text
    assert form.title.data in response.text
    assert form.text.data in response.text
    assert "Visible for everyone" in response.text
    assert "Edit" in response.text
    assert "Delete" in response.text

def test_update_post_submit_failed(client, db_init, authenticated_user, posts):
    post = posts[0]
    assert post is not None

    form = PostUpdateForm()
    form.title.data = ''
    form.text.data = ''
    form.type.data = post.type
    form.enabled.data = post.enabled
    form.category.data = post.category_id or -1
    form.tags.data = [tag.id for tag in post.tags]

    response = client.post(url_for('post.update', id=post.id),
                           data=form.data,
                           follow_redirects=True)
    assert response.status_code == 200
    assert "Your post cannot be updated until you resolve the mistakes" in response.text
    assert form.title.data in response.text
    assert form.text.data in response.text
    assert "Title" in response.text
    assert "Content" in response.text
    assert "Category" in response.text
    assert "Type" in response.text
    assert "Tags" in response.text
    assert "Enabled" in response.text
    assert "Update" in response.text

def test_delete_post_view_guest(client, db_init, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.delete', id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert "E-mail" in response.text
    assert "Password" in response.text
    assert "Remember Me" in response.text
    assert "Sign In" in response.text

def test_delete_post_view_forbidden(client, db_init, authenticated_user_2, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.delete', id=post.id))
    assert response.status_code == 403

def test_delete_post_view(client, db_init, authenticated_user, posts):
    post = posts[0]
    assert post is not None
    response = client.get(url_for('post.delete', id=post.id))
    assert response.status_code == 200
    assert "Delete Post" in response.text
    assert "Confirm Deletion" in response.text

def test_delete_post_submit_guest(client, db_init, posts):
    post = posts[0]
    assert post is not None
    response = client.post(url_for('post.delete', id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert "E-mail" in response.text
    assert "Password" in response.text
    assert "Remember Me" in response.text
    assert "Sign In" in response.text

def test_delete_post_submit_forbidden(client, db_init, authenticated_user_2, posts):
    post = posts[0]
    assert post is not None
    response = client.post(url_for('post.delete', id=post.id))
    assert response.status_code == 403

def test_delete_post_submit_successful(client, db_init, authenticated_user, posts):
    post = posts[0]
    assert post is not None
    response = client.post(url_for('post.delete', id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert "Your post has been deleted" in response.text
