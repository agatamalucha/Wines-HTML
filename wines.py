from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/process', methods=['post'])
def process():
    wine_name = request.form['wine']
    wine_description=request.form['description']
    return render_template('index.html', wine_name=wine, wine_description=wine)

if __name__ == '__main__':
    app.run(debug=True)

