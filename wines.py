from flask import Flask, render_template, request, redirect, url_for
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
    result = Wines.query.all()
    return render_template('index.html', listing=result)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/process', methods=['POST'])
def process():
    wine_name = request.form['wine']
    wine_description = request.form['description']

    record_saving = Wines(name= wine_name, description= wine_description)

    db.session.add(record_saving)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
