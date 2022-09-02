from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    return render_template("login.html")

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
    
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email is already in use", category="error")
        elif username_exists:
            flash("Username is already in use", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(username) < 2:
            flash("Username is too short", category="error")
        elif len(password1) < 6:
            flash("Passwords is too short", category="error")
        else:
            new_user = User(email=email, username=username, password=password1)
            db.dession.add(new_user)
            db.session.commit()
            flash("User created")
            return redirect(url_for("views.home"))



    return render_template("signup.html")


@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))