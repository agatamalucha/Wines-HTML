import os
from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
from werkzeug.utils import secure_filename

from db import db
from wines_blueprint.models import WineModel
from wines_blueprint.utils import allowed_file, upload_file_to_s3


wines_blueprint = Blueprint ('wines_blueprint', __name__ )


# MAIN VIEW


# ADD FUNCTIONALITY

@wines_blueprint.route('/add')  # view that allows user to add wines into database
def add():
    return render_template('add.html')



# Function that works inside of "add" view and makes html form connect to database
@wines_blueprint.route('/process_add_to_db', methods=['POST'])  # post allows send record from html to database
def process_add_to_db():

    wine_name = request.form[
        'wine']  # what user writes in the name field;  html record ('wine') into python ('wine_name')
    wine_description = request.form['description']
    file = request.files["wine_image"]

    #### HANDLING IMAGE UPLOAD  - Different scenarios -checks
    if "wine_image" not in request.files:  # if file not processed by html form
        return "No user_file key in request.files"

    if file and allowed_file(file.filename):  # check if allowed extension
        file.filename = secure_filename(file.filename)  # give file a name in S3
        output = upload_file_to_s3(file, os.environ.get('S3_BUCKET_NAME'))

    if file.filename == "":  # no file choosen
        return "Please select a file"
    ###########################

    # what is being transfer from python('wine_name' )into database ('name'column)
    record_saving = WineModel(name=wine_name,
                          description=wine_description,
                          img_url='https://agatawines.s3-eu-west-1.amazonaws.com/' + file.filename)

    db.session.add(record_saving)  # preparing record for database saving
    db.session.commit()  # saving into database

    return redirect(url_for('index'))  # use always this function  redirect(url_for('xxx'))


# EDIT FUNCTIONALITY

#  RETRIEVE FROM DB to PYTHON --> HTML (edit)
@wines_blueprint.route('/edit/<wine_id>', methods=['POST', 'GET'])  # view that allows user to add wines into database
def edit(wine_id):  # wine_id- you have to put html reference if want to use data that is on the website
    the_edit = WineModel.query.filter_by(
        id=wine_id).first()  # Find correct card from DB by giving database name and finding by PK -ID
    return render_template('edit.html',
                           edited_wine=the_edit)  # To go to new website template and load info of correct ID


#   PROCESS EDITED WINE FROM HTML -> PYTHON ->  DATABASE (process_edit_to_db)
@wines_blueprint.route('/process_edit_to_db/<update_selected_wine>',
           methods=["POST"])  # <-- update_selected_wines comes from html template line 15
def process_edit_to_db(update_selected_wine):
    updated_wine = WineModel.query.filter_by(id=update_selected_wine).first()  # quering from Database by ID

    updated_wine.name = request.form['wine']  # replacing current data in "Name" column in DB with new data
    updated_wine.description = request.form[
        'description']  # replacing current data in "Description" column in DB with new data

    db.session.commit()

    return redirect(url_for("index"))


# DELETE FUNCTIONALITY
@wines_blueprint.route('/delete/<wine_id>', methods=['POST', 'GET'])  # post allows send record from html to database
def delete(wine_id):
    WineModel.query.filter_by(id=wine_id).delete()
    db.session.commit()
    return redirect(url_for('index'))
