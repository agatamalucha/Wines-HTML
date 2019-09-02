
from db import db



class WineModel(db.Model):  # set up of database table, column names, type of data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    img_url = db.Column(db.String(1000))  # image stored in AWS , URL to that image stored in Database in " string "type of data