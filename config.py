import subprocess

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask config variables."""

    # General Config
    SECRET_KEY = "this is a secret"
    # FLASK_APP = environ["FLASK_APP"]
    # FLASK_ENV = environ["FLASK_ENV"]

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
