from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.secret_key = b"su7sinADFC6v4n_!6jVQqZ.YE67DYpP4"
app.config.from_object("config")
login_manager = LoginManager(app);
login_manager.login_view = "login"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "info"

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    from .base import base_blueprint, menu
    app.register_blueprint(base_blueprint)

    from .todo import todo_blueprint
    app.register_blueprint(todo_blueprint)

    from .feedback import feedback_blueprint
    app.register_blueprint(feedback_blueprint)

    from .user import user_blueprint
    app.register_blueprint(user_blueprint)

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
        menu.MenuItem("Info", "cookies.index", lambda : (current_user and current_user.is_authenticated)),
        menu.separator(),
        menu.MenuItem("ToDo List", "todo.list"),
        menu.separator(),
        menu.MenuItem("Feedback", "feedback.index"),
        menu.separator(),
        menu.MenuItem("Users", "user.list"),
        menu.MenuItem("Account", "user.account", lambda : (current_user and current_user.is_authenticated)),
        menu.MenuItem("Sign Out", "user.logout", lambda : (current_user and current_user.is_authenticated)),
        menu.MenuItem("Sign In", "user.login", lambda : (not current_user or not current_user.is_authenticated)),
        menu.MenuItem("Sign Up", "user.register", lambda : (not current_user or not current_user.is_authenticated)),
    )

