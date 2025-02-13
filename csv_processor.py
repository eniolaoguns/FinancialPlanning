import pandas as pd
from database import add_transaction
from categorys import categorise_expense

def process_csv(file_path):
    """Reads a bank statement CSV file and adds transactions to the database."""
    try:
        df = pd.read_csv(file_path)
        # Normalise column names
        columns = [col.lower() for col in df.columns]
        if 'date' in columns and 'description' in columns and 'amount' in columns:
            df.columns = columns
        else:
            raise ValueError("CSV must contain Date, Description, and Amount columns.")
        # Process each transaction
        for _, row in df.iterrows():
            date = row['date']
            description = row['description']
            amount = row['amount']
            category = categorise_expense(description)
            # Determine transaction type
            transaction_type = 'income' if amount > 0 else 'expense'
            # Add transaction with inputs and output fields
            add_transaction(date, description, amount, category, trans_type=transaction_type, source='csv', original_data=row.to_dict())
        print("CSV uploaded successfully")
    except Exception as e:
        print(f"Error processing CSV: {e}")