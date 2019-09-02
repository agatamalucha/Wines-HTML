

from flask_wtf import FlaskForm  # import stuff from  flask  form so we can use flask forms and validators
from wtforms import StringField, PasswordField, BooleanField  # import stuff from  flask  form so we can use flask forms and validators
from wtforms.validators import InputRequired, Email, Length  # import stuff from  flask  form so we can use flask forms and validators
from werkzeug.security import generate_password_hash, check_password_hash  # import function that allow to hash password while inputting it to login or sign in
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for








class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), ])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

