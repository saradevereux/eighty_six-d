from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from db import db
from forms import CreatePostForm
from models import Post, User, Comment, Like


views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("./index.html", user=current_user, posts=posts)


@views.route("/create-post", methods=["GET", "POST"])
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
            return redirect(url_for("views.home"))
    return render_template("create_post.html", form=form, user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.id:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", category="success")

    return redirect(url_for("views.home"))


@views.route("/posts/<user_id>")
@login_required
def posts(user_id):
    user = User.query.filter_by(id=user_id).first()
    first_name = User.first_name
    if not User:
        flash("User does not exists.", category="error")
        return redirect(url_for("views.home"))
    posts = user.post

    return render_template(
        "posts.html", user=current_user, posts=posts, first_name=first_name
    )


@views.route("create-comment/<post_id>", methods=["POST"])
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
    return redirect(url_for("views.home"))


@views.route("delete-comment/<comment_id>")
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

    return redirect(url_for("views.home"))


@views.route("/like-post/<post_id>", methods=["POST"])
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

@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@views.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 404