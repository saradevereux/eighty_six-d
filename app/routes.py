
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.forms import SignUpForm, LoginForm, UpdateProfileForm, CreatePostForm
from .models import Post, User, Comment, Like

from flask import current_app as app

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route("/update-profile/<user_id>", methods=["GET", "PATCH"])
@login_required
def update_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateProfileForm()
    if request.method == "PATCH":
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.email = request.form["email"]

        db.session.commit()
        login_user(user, remember=True)
        flash("Profile has been updated")
        return redirect(url_for("main_bp.home"))
    
    return render_template("update-profile.html", form=form, user=current_user)
    
@main_bp.route("/")
@main_bp.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("./index.html", user=current_user, posts=posts)


@main_bp.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == "POST":
        text = form.text.data
        if not text:
            flash("Post cannot be empty", category="error")
        else:
            post = Post(text=text, author=current_user.id, business= form.business.data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("main_bp.home"))
    return render_template("create_post.html", form=form, user=current_user)


@main_bp.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", category="success")

    return redirect(url_for("main_bp.home"))


@main_bp.route("/posts/<user_id>")
@login_required
def posts(user_id):
    user = User.query.filter_by(id=user_id).first()
    first_name = User.first_name
    if not User:
        flash("User does not exists.", category="error")
        return redirect(url_for("main_bp.home"))
    posts = user.post

    return render_template(
        "posts.html", user=current_user, posts=posts, first_name=first_name
    )


@main_bp.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")

    if not text:
        flash("Comment cannot be empty.", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist.", category="error")
    return redirect(url_for("main_bp.home"))


@main_bp.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash("Comment does not exist.", category="error")
    elif current_user.id != comment.author or current_user.id != comment.author:
        flash("You do no have permission to delete this comment.", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("main_bp.home"))


@main_bp.route("/like-post/<post_id>", methods=["GET", "PATCH"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({"error": "Post does not exist."}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return jsonify(
        {
            "likes": len(post.likes),
            "liked": current_user.id in map(lambda x: x.author, post.likes),
        }, 200
    )

# @main_bp.errorhandler(404)
# def page_not_found(e):
#     return make_response(render_template("404.html"), 404)

# @main_bp.errorhandler(500)
# def internal_server_error():
#     return make_response(render_template("500.html"), 404)

