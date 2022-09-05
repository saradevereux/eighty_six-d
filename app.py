from flask import Flask
from flask_login import LoginManager
from os import path

from auth import auth
from create_db import db, DB_NAME
from models import User, Post, Comment, Like
from views import views


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)