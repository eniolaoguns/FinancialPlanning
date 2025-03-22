# import sqlite3

# # Mapping of numeric month to month name
# month_name_map = {
#     '01': 'January', '02': 'February', '03': 'March', '04': 'April',
#     '05': 'May', '06': 'June', '07': 'July', '08': 'August',
#     '09': 'September', '10': 'October', '11': 'November', '12': 'December'
# }

# # Function to view transactions by month, year, and category
# def view_transactions_by_category():
#     try:
#         # Connect to the SQLite database
#         conn = sqlite3.connect('expenses.db')
#         cursor = conn.cursor()

#         # Execute the SQL query to fetch data
#         query = '''
#         SELECT
#             substr(date, 7, 4) AS year,
#             substr(date, 4, 2) AS month,
#             category,
#             SUM(amount) AS total_amount
#         FROM
#             transactions
#         GROUP BY
#             year,
#             month,
#             category
#         ORDER BY
#             year DESC,
#             month DESC,
#             category;
#         '''
#         cursor.execute(query)

#         # Fetch the results
#         results = cursor.fetchall()

#         # Print the results
#         print("Transactions per Category (Month, Year):")
#         for row in results:
#             year, month, category, total_amount = row
#             month_name = month_name_map.get(month, 'Unknown')  # Convert numeric month to month name
#             print(f"Year: {year}, Month: {month_name}, Category: {category}, Total Amount: {total_amount:.2f}")

#         # Close the database connection
#         conn.close()

#     except Exception as e:
#         print(f"Error viewing transactions by category: {e}")
        
        

# # Function to view total income and expenses by month, year
# def view_total_income_expenses():
#     try:
#         # Connect to the SQLite database
#         conn = sqlite3.connect('expenses.db')
#         cursor = conn.cursor()

#         # SQL query to calculate total income and total expenses by month and year
#         query = '''
#         SELECT
#             substr(date, 7, 4) AS year,  -- Extract year from the date
#             substr(date, 4, 2) AS month,  -- Extract month from the date
#             SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
#             SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense
#         FROM
#             transactions
#         GROUP BY
#             year, month
#         ORDER BY
#             year DESC, month DESC;
#         '''
        
#         cursor.execute(query)

#         # Fetch the results
#         results = cursor.fetchall()

#         # Print the results
#         print("Total Income and Expenses per Month and Year:")
#         for row in results:
#             year, month, total_income, total_expense = row
#             month_name = month_name_map.get(month, 'Unknown')  # Convert numeric month to month name
#             print(f"Year: {year}, Month: {month_name}, Total Income: {total_income:.2f}, Total Expense: {total_expense:.2f})

#         # Close the database connection
#         conn.close()

#     except Exception as e:
#         print(f"Error viewing total income and expenses: {e}")




# # Call the function to view transactions
# if __name__ == "__main__":
#     view_transactions_by_category()
#     view_total_income_expenses()



import sqlite3

# Mapping of numeric month to month name
month_name_map = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
}

# Function to view transactions by month, year, category, and net income/expense
def view_transactions_by_category_and_net():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()

        # SQL query to calculate total income, total expense, and net for each month and year
        query = '''
        SELECT
            substr(date, 7, 4) AS year,  -- Extract year from the date
            substr(date, 4, 2) AS month,  -- Extract month from the date
            category,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS total_expense
        FROM
            transactions
        GROUP BY
            year,
            month,
            category
        ORDER BY
            year DESC,
            month DESC,
            category;
        '''
        
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Print the results with net calculation
        print("Transactions per Category (Month, Year):")
        for row in results:
            year, month, category, total_income, total_expense = row
            net = total_income - abs(total_expense)
            month_name = month_name_map.get(month, 'Unknown')  # Convert numeric month to month name
            print(f"Year: {year}, Month: {month_name}, Category: {category}, Total Income: {total_income:.2f}, Total Expense: {total_expense:.2f}, Net: {net:.2f}")

        # Close the database connection
        conn.close()

    except Exception as e:
        print(f"Error viewing transactions by category: {e}")


# Function to view total income, expenses, net cash flow by month, and overall yearly net
def view_total_income_expenses_and_net_cashflow():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()

        # SQL query to calculate total income, total expenses, and net cash flow by month and year
        query = '''
        SELECT
            substr(date, 7, 4) AS year,  -- Extract year from the date
            substr(date, 4, 2) AS month,  -- Extract month from the date
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

        # Fetch the results
        results = cursor.fetchall()

        # Print the results with net cash flow for each month
        print("Total Income, Expenses, and Net Cash Flow per Month and Year:")
        for row in results:
            year, month, total_income, total_expense, net_cashflow = row
            month_name = month_name_map.get(month, 'Unknown')  # Convert numeric month to month name
            print(f"Year: {year}, Month: {month_name}, Total Income: {total_income:.2f}, Total Expense: {total_expense:.2f}, Net Cash Flow: {net_cashflow:.2f}") #curent error there with net cashflow

        # Overall net cash flow for the year
        yearly_net_query = '''
        SELECT
            substr(date, 7, 4) AS year,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) - SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS net_cashflow
        FROM
            transactions
        GROUP BY
            year
        ORDER BY
            year DESC;
        '''

        cursor.execute(yearly_net_query)
        yearly_results = cursor.fetchall()

        # Print the yearly net cash flow
        print("\nYearly Net Cash Flow:")
        for row in yearly_results:
            year, yearly_net_cashflow = row
            print(f"Year: {year}, Net Cash Flow: {yearly_net_cashflow:.2f}")

        # Close the database connection
        conn.close()

    except Exception as e:
        print(f"Error viewing total income, expenses, and net cash flow: {e}")


# Call the function to view transactions and net cash flow
if __name__ == "__main__":
    view_transactions_by_category_and_net()
    view_total_income_expenses_and_net_cashflow()
