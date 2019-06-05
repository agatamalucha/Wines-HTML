from flask import Flask, render_template, request
from flask_sqlalchemy  import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Wines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))



wine_list = [['Les Mougeottes Pinot Noir', 'Good wine'], ['Emotivo Pinot Grigio', 'Nice fresh']]


@app.route('/')
def index():
    listing = wine_list
    return render_template('index.html', listing=listing)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/process', methods=['post'])
def process():
    wine_name = request.form['wine']
    wine_description = request.form['description']
    return render_template('index.html', wine_name=wine, wine_description=description)


if __name__ == '__main__':
    app.run(debug=True)
