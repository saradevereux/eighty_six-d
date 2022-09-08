from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask config variables."""

    # General Config
    SECRET_KEY = "this is a secret"
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "postgresql://hbpjgcmkcvoadh:5b160d86886437754571992e43b8278433f8cf7f4c6a6535e0c84c38eecf11be@ec2-107-23-76-12.compute-1.amazonaws.com:5432/d1ic5uskf0igb1"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
