from flask import Flask, render_template, request, redirect, url_for    # flask imports
from flask_sqlalchemy  import SQLAlchemy                                # for database initiation


app = Flask(__name__)                                                   # initiate Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wines.db'            # database config, route to sqlite :///
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)                                                    # launching of database

class Wines(db.Model):                                                  # set up of database table, column names, type of data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))



# wine_list = [['Les Mougeottes Pinot Noir', 'Good wine'], ['Emotivo Pinot Grigio', 'Nice fresh']]



@app.route('/')                                                          # web browser path
# in flask all views are functions -  def
def index():                                                               # define view function
    result = Wines.query.all()                                              # result=get all from database; Wines= name of database

# send to html     read html template   name of template in template folder     variables that will be send from python into html
    return          render_template(    'index.html',                                listing=result)


@app.route('/add')                      # view that allows user to add wines into database
def add():
    return render_template('add.html')


# Function that works inside of "add" view and makes html form connect to database
@app.route('/process', methods=['POST'])    # post allows send record from html to database
def process():
    wine_name = request.form['wine']                    # what user writes in the name field;  html record ('wine') into python ('wine_name')
    wine_description = request.form['description']

    record_saving = Wines(name= wine_name, description= wine_description)    # what is being transfer from python('wine_name' )into database ('name'column)

    db.session.add(record_saving)                                            # preparing record for database saving
    db.session.commit()                                                      # saving into database

    return redirect(url_for('index'))                                        # use always this function  redirect(url_for('xxx'))



@app.route('/delete/<wine_id>', methods=['POST', 'GET'])    # post allows send record from html to database
def delete(wine_id):

    Wines.query.filter_by(id=wine_id).delete()
    db.session.commit()
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)                                                      # this allow to show any errors in the app

