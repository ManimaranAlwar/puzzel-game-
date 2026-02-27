from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# 1. Main Dashboard (Connecting all games)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Grammar Game Route
@app.route('/grammer')
def grammer_game():
    return render_template('grammer.html', puzzles=puzzles)

# 3. Plant Growth Game Route
@app.route('/plant_growth')
def plant_growth():
    return render_template('plant_growth.html')

# 4. Sequence Game Route
@app.route('/sequence')
def sequence():
    return render_template('sequence.html')
if __name__ == '__main__':
    app.run(debug=True, port=5001)