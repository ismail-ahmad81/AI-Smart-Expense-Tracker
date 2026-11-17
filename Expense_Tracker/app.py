from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pymysql 
from ai_features import predict_category, check_budget_status

app = Flask(__name__)


app.secret_key = 'super_secret_expense_tracker_key'


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'issana@123', 
    'database': 'expense_tracker'
}



@app.route('/')
def home():
    
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', user_name=session.get('user_name'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login_page'))

@app.route('/api/predict-category', methods=['POST'])
def predict():
    data = request.json
    description = data.get('description', '')
    category = predict_category(description)
    return jsonify({"category": category})


@app.route('/api/budget-check', methods=['POST'])
def budget_check():
    data = request.json
    monthly_budget = data.get('monthly_budget', 10000)
    total_spent = data.get('total_spent', 0)
    current_day = data.get('current_day', 1)
    
    result = check_budget_status(monthly_budget, total_spent, current_day)
    return jsonify(result)




@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"message": "Registration successful!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/login', methods=['POST'])
def user_login_api():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if user:
            
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            return jsonify({"message": "Login successful", "redirect": "/"}), 200
        else:
            return jsonify({"error": "Invalid Email or Password!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/add_transaction', methods=['POST'])
def add_transaction():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        category_id = data.get('category_id')
        amount = data.get('amount')
        trans_type = data.get('type')
        description = data.get('description')
        trans_date = data.get('transaction_date')

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        query = "INSERT INTO transactions (user_id, category_id, amount, type, description, transaction_date) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (current_user_id, category_id, amount, trans_type, description, trans_date))
        conn.commit()
        
        cursor.close()
        conn.close()

        return jsonify({"message": "Transaction added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        query = "SELECT transaction_date, category_id, description, amount, type FROM transactions WHERE user_id = %s"
        cursor.execute(query, (current_user_id,))
        transactions = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)