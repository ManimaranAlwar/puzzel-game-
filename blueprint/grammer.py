from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Our puzzle data
puzzles = [
    {
        "id": 1,
        "question": "Everyone in the class _______ finished the test.",
        "options": ["have", "has", "are"],
        "correct": "has"
    },
    {
        "id": 2,
        "question": "I enjoy _______ mystery books at night.",
        "options": ["to read", "reading", "read"],
        "correct": "reading"
    },
    {
        "id": 3,
        "question": "The team _______ excited about their victory.",
        "options": ["was", "were", "are"],
        "correct": "was"
    }
]

@app.route('/')
def index():
    return render_template('grammer/index.html', puzzles=puzzles)

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    puzzle_id = data.get('id')
    user_answer = data.get('answer')
    
    # Find the puzzle and verify
    puzzle = next((p for p in puzzles if p['id'] == puzzle_id), None)
    is_correct = puzzle['correct'] == user_answer
    
    return jsonify({
        "correct": is_correct,
        "message": "✨ Flawless! ✨" if is_correct else "❌ Not quite a glow-up yet!"
    })

if __name__ == '__main__':
    app.run(debug=True)