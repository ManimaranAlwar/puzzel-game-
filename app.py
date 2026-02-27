from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grammer')
def grammer_game():
    return render_template('grammer.html')

@app.route('/plant_growth')
def plant_growth():
    return render_template('plant_growth.html')

@app.route('/sequence')
def sequence():
    return render_template('sequence.html')