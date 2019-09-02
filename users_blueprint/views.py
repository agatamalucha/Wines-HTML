from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, AnonymousUserMixin, login_required
from flask import Flask, render_template, request, redirect, url_for
from db import db
from users_blueprint.forms import LoginForm, RegisterForm

from users_blueprint.models import UserModel

users_blueprint = Blueprint ('users_blueprint', __name__ )


########  LOGIN, REGISER ,USER   ######

login_manager = LoginManager()
login_manager.login_view = 'users_blueprint.login'



@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))




class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

login_manager.anonymous_user = Anonymous




# ADD FUNCTIONALITY USER AND LOGIN

@users_blueprint.route('/register_user', methods=['GET', 'POST'])  # view that allows user to register their login
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        if UserModel.query.filter_by(username=form.username.data).first() or UserModel.query.filter_by(email=form.email.data).first() is not None:
            return '<h1>User name or e-mail already exist</h1>'
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = UserModel(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return render_template('user_view.html')

    # user= User.query.filter_by(username=form.username.data).first()
    #   return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('user.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1> Invalid username or password </h1>'

        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

