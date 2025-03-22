import pandas as pd
import sqlite3
from database import add_transaction

# Function to delete and recreate the transactions table
def delete_and_recreate_transactions_table():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()

        # Drop the transactions table if it exists
        cursor.execute('DROP TABLE IF EXISTS transactions')

        # Recreate the transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            amount REAL,
            category TEXT,
            type TEXT,
            source TEXT,
            original_data TEXT
        )
        ''')

        conn.commit()
        conn.close()
        print("Transactions table deleted and recreated successfully.")

    except Exception as e:
        print(f"Error deleting or recreating transactions table: {e}")

# Function to process the Monzo CSV and add transactions to the database
def process_csv(file_path):
    """Reads Monzo bank statement CSV file and adds transactions to the database."""
    try:
        # Delete and recreate the transactions table before processing
        delete_and_recreate_transactions_table()

        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)

        # Normalize column names to lowercase
        columns = [col.lower().strip() for col in df.columns]
        df.columns = columns

        # Check if the required columns exist
        required_columns = ["date", "name", "category", "amount", "type"]
        if not all(col in columns for col in required_columns):
            raise ValueError(f"CSV must contain required columns: {', '.join(required_columns)}")

        # Process each transaction
        for _, row in df.iterrows():
            date = row["date"]
            name = row["name"]
            amount = row["amount"]
            trans_type = row["type"]

            # Skip transactions with type "Pot transfer"
            if trans_type == "Pot transfer":
                continue  # Skip this transaction

            # Special handling for transactions with specific name or type
            # 1. If the name is "Downing Property Management Ltd", set category as "Bills"
            if name == "Downing Property Management Ltd":
                category = "Bills"
            else:
                category = row["category"]
                

            # 2. If the type is "Faster payment" or "Monzo-to-Monzo", set transaction type to "transfer"
            if trans_type in ["Faster payment", "Monzo-to-Monzo"] and name != "Downing Property Management Ltd":
                if amount > 0:
                    trans_type = "income"
                    category = "Transfers In"  # Set category as "Transfers In" for incoming transfers
                elif amount < 0:
                    trans_type = "expense"
                    category = "Transfers Out"  # Set category as "Transfers Out" for outgoing transfers
            else:
                # Default to "income" or "expense" based on amount
                trans_type = "income" if amount > 0 else "expense"

            # Add the transaction to the database
            add_transaction(date, name, amount, category, trans_type=trans_type, source="csv", original_data=row.to_dict())

        print("CSV uploaded successfully")

    except Exception as e:
        print(f"Error processing CSV: {e}")

# Run the script
if __name__ == "__main__":
    # Specify the path to your Monzo CSV file
    file_path = "Monzo.csv"
    process_csv(file_path)

