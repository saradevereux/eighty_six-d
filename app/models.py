from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship(
        "Post", backref="user_posts", passive_deletes=True, lazy="dynamic"
    )
    comments = db.relationship("Comment", backref="user_comments", passive_deletes=True)
    likes = db.relationship("Like", backref="user_id", passive_deletes=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    post_business = db.Column(
        db.Integer, db.ForeignKey("business.id", ondelete="CASCADE")
    )
    comments = db.relationship(
        "Comment", backref="comments_post", passive_deletes=True, uselist=True
    )
    likes = db.relationship("Like", backref="likes_post", passive_deletes=True)

    def __repr__(self):
        return "<Post {}>".format(self.text)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    post = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"))

    def __repr__(self):
        return "<Comment {}>".format(self.text)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    zip_code = db.Column(db.String(5))
    posts = db.relationship(
        "Post", backref="business_posts", passive_deletes=True, lazy="dynamic"
    )

    def __repr__(self):
        return "<Business {}>".format(self.name)
