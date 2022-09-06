from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm, SignUpForm
from .models import db, User, check_password_hash
from . import login_manager


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(password=form.password.data):
                login_user(user, remember=True)
                return redirect(url_for("main_bp.home"))
            else:
                flash("Invalid username/password combination", category="error")
                return redirect(url_for('login.html'))
    return render_template("login.html", form=form, user=current_user)

@auth_bp.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("An account already exists with that email.", category="error")
            else:
                new_user = User(
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                )
                user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("User created")
                return redirect(url_for("main_bp.home"))
    return render_template("signup.html", form=form, user=current_user)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message="You are now logged out.", category="success")
    return redirect(url_for('auth_bp.login'))

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


# @login_manager.unauthorized_handler
# def unauthorized():
#     """Redirect unauthorized users to Login page."""
#     flash('You must be logged in to view that page.')
#     return redirect(url_for('login.html'))

