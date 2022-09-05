from cgitb import text
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignUpForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm", message="Passwords must match"), Length(min=7, message="Passowrd must be at least 8 charecters")])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Passowrd", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CreatePostForm(FlaskForm):
    business = StringField("Who do you want to Blast:", validators=[DataRequired()])
    text = TextAreaField("And why: ", validators=[DataRequired()])
    submit = SubmitField("Post")