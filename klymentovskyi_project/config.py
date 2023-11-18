from os import environ as env

class Development():
    DEBUG = True
    SECRET_KEY = env.get("SECRET_KEY", "XbYCy4N@B2QwKgHsGfHDcbJRa_ZfQr.L")
    FLASK_SECRET = SECRET_KEY
    WTF_CSRF_ENABLED = True
    SESSION_PERMANENT = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production():
    DEBUG = False
    SECRET_KEY = env.get("SECRET_KEY", "isDAGa!2vs7k2stx4xGufiM-FwveWY.u")
    FLASK_SECRET = SECRET_KEY
    WTF_CSRF_ENABLED = True
    SESSION_PERMANENT = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

CONFIG = {
    "default": Development,
    "prod": Production,
    "dev": Development,
}
