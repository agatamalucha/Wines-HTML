import os
import env
from flask import Flask, render_template, request, redirect, url_for  # flask imports
from flask_sqlalchemy import SQLAlchemy  # for database initiation
from werkzeug.utils import secure_filename
import boto3, botocore

app = Flask(__name__)  # initiate Flask app

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['S3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAME')
app.config["S3_LOCATION"] = 'http://{}.s3.amazonaws.com/'.format(os.environ.get('S3_BUCKET_NAME'))
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['DEBUG'] = True  # this allow to show any errors in the app

db = SQLAlchemy(app)  # launching of database
s3 = boto3.client("s3", aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)


class Wines(db.Model):  # set up of database table, column names, type of data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    img_url = db.Column(db.String(1000))


# MAIN VIEW

@app.route('/')  # web browser path
# in flask all views are functions -  def
def index():  # define view function
    result = Wines.query.all()  # result=get all from database; Wines= name of database

    # send to html     read html template   name of template in template folder     variables that will be send from python into html
    return render_template('index.html', listing=result)


# ADD FUNCTIONALITY

@app.route('/add')  # view that allows user to add wines into database
def add():
    return render_template('add.html')


# Function that works inside of "add" view and makes html form connect to database
@app.route('/process_add_to_db', methods=['POST'])  # post allows send record from html to database
def process_add_to_db():
    wine_name = request.form[
        'wine']  # what user writes in the name field;  html record ('wine') into python ('wine_name')
    wine_description = request.form['description']
    file = request.files["wine_image"]


#### HANDLING IMAGE UPLOAD
    if "wine_image" not in request.files:
        return "No user_file key in request.files"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET_NAME"])

    if file.filename == "":
        return "Please select a file"
###########################

    # what is being transfer from python('wine_name' )into database ('name'column)
    record_saving = Wines(name=wine_name,
                          description=wine_description,
                          img_url='https://agatawines.s3-eu-west-1.amazonaws.com/' + file.filename)

    db.session.add(record_saving)  # preparing record for database saving
    db.session.commit()  # saving into database

    return redirect(url_for('index'))  # use always this function  redirect(url_for('xxx'))


# EDIT FUNCTIONALITY

#  RETRIEVE FROM DB to PYTHON --> HTML (edit)
@app.route('/edit/<wine_id>', methods=['POST', 'GET'])  # view that allows user to add wines into database
def edit(wine_id):  # wine_id- you have to put html reference if want to use data that is on the website
    the_edit = Wines.query.filter_by(
        id=wine_id).first()  # Find correct card from DB by giving database name and finding by PK -ID
    return render_template('edit.html',
                           edited_wine=the_edit)  # To go to new website template and load info of correct ID


#   PROCESS EDITED WINE FROM HTML -> PYTHON ->  DATABASE (process_edit_to_db)
@app.route('/process_edit_to_db/<update_selected_wine>',
           methods=["POST"])  # <-- update_selected_wines comes from html template line 15
def process_edit_to_db(update_selected_wine):
    updated_wine = Wines.query.filter_by(id=update_selected_wine).first()  # quering from Database by ID

    updated_wine.name = request.form['wine']  # replacing current data in "Name" column in DB with new data
    updated_wine.description = request.form[
        'description']  # replacing current data in "Description" column in DB with new data

    db.session.commit()

    return redirect(url_for("index"))


# DELETE FUNCTIONALITY
@app.route('/delete/<wine_id>', methods=['POST', 'GET'])  # post allows send record from html to database
def delete(wine_id):
    Wines.query.filter_by(id=wine_id).delete()
    db.session.commit()
    return redirect(url_for('index'))



# START APP

if __name__ == '__main__':

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run()
