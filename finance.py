import sqlite3
def add_transaction():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    transaction_type = input("Enter transaction type (Income/Expense): ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))

    cursor.execute("INSERT INTO transactions (type, category, amount) VALUES (?, ?, ?)", (transaction_type, category, amount))
    conn.commit()
    conn.close()
    print("\n✅ Transaction added successfully!")