from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name = "default"):
    from config import CONFIG
    if not config_name in CONFIG:
        config_name = "default"

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(CONFIG[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    login_manager.login_message = "You must sign in to access this page."
    login_manager.login_message_category = "info"

    with app.app_context():
        from .base import base_blueprint, menu
        app.register_blueprint(base_blueprint)

        from .todo import todo_blueprint
        app.register_blueprint(todo_blueprint)

        from .feedback import feedback_blueprint
        app.register_blueprint(feedback_blueprint)

        from .user import user_blueprint
        app.register_blueprint(user_blueprint)

        from .post import post_blueprint
        app.register_blueprint(post_blueprint)

        from .cookies import cookies_blueprint
        app.register_blueprint(cookies_blueprint)

        from .portfolio import portfolio_blueprint, views as portfolio_views
        app.register_blueprint(portfolio_blueprint)
        app.route("/")(portfolio_views.main)

        menu.add_items(
            menu.MenuItem("Main", "portfolio.main"),
            menu.MenuItem("Skills", "portfolio.skills"),
            menu.MenuItem("Projects", "portfolio.projects"),
            menu.MenuItem("About me", "portfolio.about"),
            menu.separator(),
            menu.MenuItem("Cookies", "cookies.index", lambda : (current_user and current_user.is_authenticated)),
            menu.separator(),
            menu.MenuItem("ToDo List", "todo.list"),
            menu.separator(),
            menu.MenuItem("Feedback", "feedback.index"),
            menu.separator(),
            menu.MenuItem("Posts", "post.list"),
            menu.MenuItem("Post", "post.create", lambda : (current_user and current_user.is_authenticated)),
            menu.MenuItem("Categories", "post.category_list"),
            menu.MenuItem("Tags", "post.tag_list"),
            menu.separator(),
            menu.MenuItem("Users", "user.list"),
            menu.MenuItem("Account", "user.account", lambda : (current_user and current_user.is_authenticated)),
            menu.MenuItem("Sign Out", "user.logout", lambda : (current_user and current_user.is_authenticated)),
            menu.MenuItem("Sign In", "user.login", lambda : (not current_user or not current_user.is_authenticated)),
            menu.MenuItem("Sign Up", "user.register", lambda : (not current_user or not current_user.is_authenticated)),
        )

    return app

