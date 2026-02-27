from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Grammar Game Data
puzzles = [
    {"id": 1, "question": "Everyone in the class _______ finished the test.", "options": ["have", "has", "are"], "correct": "has"},
    {"id": 2, "question": "I enjoy _______ mystery books at night.", "options": ["to read", "reading", "read"], "correct": "reading"},
    {"id": 3, "question": "The team _______ excited about their victory.", "options": ["was", "were", "are"], "correct": "was"}
]

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

# API Logic for Grammar Checking
@app.route('/check', methods=['POST'])
def check():
    data = request.json
    puzzle_id = data.get('id')
    user_answer = data.get('answer')
    puzzle = next((p for p in puzzles if p['id'] == puzzle_id), None)
    
    if not puzzle:
        return jsonify({"correct": False, "message": "Puzzle error"}), 404
    
    is_correct = (puzzle['correct'] == user_answer)
    return jsonify({
        "correct": is_correct,
        "message": "✨ Flawless! ✨" if is_correct else "❌ Try again!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)