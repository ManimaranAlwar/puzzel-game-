from flask import Flask, render_template, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

app = Flask(__name__)

# Initialize the Gemini Model via LangChain
# Note: Ensure GOOGLE_API_KEY is set in your environment
api_key = os.environ.get("GOOGLE_API_KEY") or "YOUR_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# Mock Database
transactions = [
    {"id": 1, "title": "Freelance Gig", "amount": 500, "type": "income"},
    {"id": 2, "title": "Canteen Lunch", "amount": -50, "type": "expense"}
]

def get_financial_advice(user_transactions):
    template = """
    You are a professional Student Financial Advisor. Analyze these recent transactions: {user_data}
    
    Categorize each transaction (e.g., Food, Academics, Entertainment, Utilities).
    Analyze spending patterns and identify where money is being wasted.
    Provide exactly three 'Actionable Tips' specifically for a college student (e.g., suggesting student discounts or meal prepping).
    Estimate how much can be saved by next month if tips are followed.
    
    Keep the tone encouraging, witty, and concise.
    Return a JSON object with:
    1. "category_breakdown": A summary of spending by category.
    2. "warnings": Any red flags (e.g., too much spent on snacks).
    3. "savings_tips": An array of three specific actionable tips.
    4. "potential_savings": An estimated dollar amount.
    5. "health_score": A score from 1-100.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | JsonOutputParser()
    
    try:
        response = chain.invoke({"user_data": str(user_transactions)})
        return response
    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "category_breakdown": {"Error": "AI Analysis Failed"},
            "warnings": ["Check your API key or network connection."],
            "savings_tips": ["Save more", "Spend less", "Keep tracking"],
            "potential_savings": 0,
            "health_score": 0
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transactions', methods=['GET', 'POST'])
def handle_transactions():
    if request.method == 'POST':
        data = request.json
        new_tx = {
            "id": len(transactions) + 1,
            "title": data['title'],
            "amount": float(data['amount']),
            "type": "income" if float(data['amount']) > 0 else "expense"
        }
        transactions.append(new_tx)
        return jsonify(new_tx), 201
    
    return jsonify(transactions)

@app.route('/api/advice', methods=['GET'])
def get_advice():
    advice = get_financial_advice(transactions)
    return jsonify(advice)

@app.route('/api/chat', methods=['POST'])
def mentor_chat():
    data = request.json
    user_query = data.get('query')
    
    template = """
    You are a professional Student Financial Advisor (Mentor). 
    User Question: {query}
    Context (Recent Transactions): {user_data}
    
    Provide a witty, concise, and helpful response. If they want to buy something expensive, compare it to their current spending/rent.
    Keep it encouraging.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"query": user_query, "user_data": str(transactions)})
        return jsonify({"response": response.content})
    except Exception as e:
        return jsonify({"response": "Sorry, I'm a bit busy calculating decimals right now. Try again later!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    