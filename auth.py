from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from forms import SignUpForm, LoginForm
from models import User


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            password = form.password.data
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for("views.home"))
                else:
                    flash("Password is incorrect", category="error")
            else:
                flash("Email does not exist", category="error")
    return render_template("login.html", form=form, user=current_user)

@auth.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("Email is already in use", category="error")
            else:
                new_user = User(
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=generate_password_hash(form.password.data, method="sha256"),
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("User created")
                return redirect(url_for("views.home"))
    return render_template("signup.html", form=form, user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
