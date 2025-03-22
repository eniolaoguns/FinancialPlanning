from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

DB_FILE = "expenses.db"

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create Transactions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       date TEXT,
       description TEXT,
       amount REAL,
       category TEXT,
       type TEXT,  -- 'income' or 'expense'
       source TEXT, -- 'manual' or 'csv'
       original_data TEXT -- JSON string of the original row data
    )
    ''')

    # Create Budget Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       month TEXT,
       year INTEGER,
       budget_amount REAL
    )
    ''')

    conn.commit()
    conn.close()

init_db()  # Initialize the database on startup

@app.route("/")
def home():
    return "Financial Data Analysis API is running!"



@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        data = request.json  # Get data from request
        date = data["date"]
        description = data["description"]
        amount = float(data["amount"])
        category = data["category"]
        trans_type = data["type"]
        source = data.get("source", "manual")
        original_data = json.dumps(data.get("original_data", {}))

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (date, description, amount, category, type, source, original_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, description, amount, category, trans_type, source, original_data))
        conn.commit()
        conn.close()

        return jsonify({"message": "Transaction added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    
    transactions_list = [
        {"id": row[0], "date": row[1], "description": row[2], "amount": row[3], "category": row[4], "type": row[5]}
        for row in transactions
    ]
    
    return jsonify(transactions_list)


@app.route('/summary', methods=['GET'])
def get_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = '''
        SELECT
            substr(date, 7, 4) AS year,
            substr(date, 4, 2) AS month,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) - SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS net_cashflow
        FROM
            transactions
        GROUP BY
            year, month
        ORDER BY
            year DESC, month DESC;
    '''

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    summary_list = [
        {"year": row[0], "month": row[1], "total_income": row[2], "total_expense": row[3], "net_cashflow": row[4]}
        for row in results
    ]

    return jsonify(summary_list)



@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        df = pd.read_csv(file)

        # Process transactions from CSV
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        for _, row in df.iterrows():
            date = row["date"]
            name = row["name"]
            amount = row["amount"]
            trans_type = row["type"]

            if trans_type == "Pot transfer":
                continue  

            if name == "Downing Property Management Ltd":
                category = "Bills"
            else:
                category = row["category"]

            if trans_type in ["Faster payment", "Monzo-to-Monzo"] and name != "Downing Property Management Ltd":
                if amount > 0:
                    trans_type = "income"
                    category = "Transfers In"
                elif amount < 0:
                    trans_type = "expense"
                    category = "Transfers Out"
            else:
                trans_type = "income" if amount > 0 else "expense"

            cursor.execute('''
                INSERT INTO transactions (date, description, amount, category, type, source, original_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (date, name, amount, category, trans_type, "csv", json.dumps(row.to_dict())))

        conn.commit()
        conn.close()

        return jsonify({"message": "CSV uploaded successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
