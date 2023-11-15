import os

# General config
WTF_CSRF_ENABLED = True
SECRET_KEY = b"XbYCy4N@B2QwKgHsGfHDcbJRa_ZfQr.L"
SESSION_PERMANENT = True

# Database
SQLALCHEMY_DATABASE_URI = f"sqlite:///db.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False