import os
import env
from flask import Flask, render_template, request, redirect, url_for  # flask imports
from flask_login import  LoginManager, current_user, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy  # for database initiation

import boto3, botocore
from flask_bootstrap import Bootstrap
from db import db

from users_blueprint.views import users_blueprint, login_manager
from wines_blueprint.views import wines_blueprint






app = Flask(__name__)  # initiate Flask app
Bootstrap(app)  # initiate Bootstrap in order to use WTF flask forms

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # system configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['S3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAME')
app.config["S3_LOCATION"] = 'http://{}.s3.amazonaws.com/'.format(os.environ.get('S3_BUCKET_NAME'))
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['DEBUG'] = True  # this allow to show any errors in the app




s3 = boto3.client("s3", aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),  # system configurations
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

app.register_blueprint(users_blueprint)
app.register_blueprint(wines_blueprint)

login_manager.init_app(app)


class Wines(db.Model):  # set up of database table, column names, type of data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    img_url = db.Column(db.String(1000))  # image stored in AWS , URL to that image stored in Database in " string "type of data




@app.route('/')  # web browser path
# in flask all views are functions -  def
def index():  # define view function

    result = Wines.query.all()  # result=get all from database; Wines= name of database
    # username=
    # send to html     read html template   name of template in template folder     variables that will be send from python into html
    return render_template('index.html', listing=result)






# START APP  and CREATE DATABASE ,IF ONE DOESN'T EXIST

if __name__ == '__main__':

    if app.config['DEBUG']:
        from db import db
        db.init_app(app)
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run()
