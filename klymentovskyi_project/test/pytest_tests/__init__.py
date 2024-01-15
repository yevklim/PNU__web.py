import pytest
from flask import url_for
from flask_login import current_user
from app import create_app, db
from app.user.models import User
from app.user.forms import LoginForm
from app.post.models import Post, Tag, Category, EnumType

@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='module')
def db_init(client, user, user_2, categories, tags, posts):
    db.session.add_all([user, user_2, *tags, *categories, *posts])
    db.session.commit()
    yield

@pytest.fixture(scope='module')
def user():
    user = User(username='test', email='test@test.com', password='testpass')
    yield user

@pytest.fixture(scope='module')
def user_2():
    user = User(username='test2', email='test2@test.com', password='testpass')
    yield user

@pytest.fixture(scope='function')
def authenticated_user(client, user):
    user_obj: User = user
    form = LoginForm(email='test@test.com', password='testpass')
    response = client.post(url_for('user.login'),
                           data=form.data,
                           follow_redirects=True)
    assert response.status_code == 200
    assert current_user and current_user.is_authenticated

    yield user_obj

    response = client.post(url_for('user.logout'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert not current_user or not current_user.is_authenticated

@pytest.fixture(scope='function')
def authenticated_user_2(client, user_2):
    user_obj: User = user_2
    form = LoginForm(email='test2@test.com', password='testpass')
    response = client.post(url_for('user.login'),
                           data=form.data,
                           follow_redirects=True)
    assert response.status_code == 200
    assert current_user and current_user.is_authenticated

    yield user_obj

    response = client.post(url_for('user.logout'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert not current_user or not current_user.is_authenticated

@pytest.fixture(scope='module')
def categories():
    categories = [
        Category(name='Politics'),
        Category(name='Science'),
        Category(name='Entertainment'),
    ]
    yield categories

@pytest.fixture(scope='module')
def tags():
    tags = [
        Tag(name='Nice'),
        Tag(name='Interesting'),
        Tag(name='Outstanding'),
    ]
    yield tags

@pytest.fixture(scope='module')
def posts(categories, tags, user):
    posts = [
        Post(title='Post #1', text='Lorem ipsum...',
             category=categories[0],
             tags=[tags[0], tags[1]],
             type='other',
             enabled=True,
             user=user),
        Post(title='Post #2', text='Lorem Ipsum...',
             category=categories[1],
             tags=[tags[1], tags[2]],
             type='other',
             enabled=True,
             user=user),
        Post(title='Post #3 (Hidden)', text='lorem ipsum...',
             category=categories[2],
             tags=[tags[0], tags[2]],
             type='publication',
             enabled=False,
             user=user)
    ]
    yield posts
