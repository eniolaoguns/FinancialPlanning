import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('expenses.db')
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

# Function to add a transaction
def add_transaction(date, description, amount, category, trans_type='expense', source='manual', original_data=None):
   cursor.execute('''
       INSERT INTO transactions (date, description, amount, category, type, source, original_data)
       VALUES (?, ?, ?, ?, ?, ?, ?)
   ''', (date, description, amount, category, trans_type, source, json.dumps(original_data)))
   conn.commit()

print("Transactions database setup complete")

# Function to set a monthly budget
def set_budget(month, year, budget_amount):
   cursor.execute('''
       INSERT INTO budgets (month, year, budget_amount)
       VALUES (?, ?, ?)
   ''', (month, year, budget_amount))
   conn.commit()

print("Budget Database setup complete.")