import sqlite3


def add_transaction(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    print("\n========== Add Transaction ==========")

    transaction_type = input("Enter Transaction Type (Income/Expense): ")
    category = input("Enter Category: ")
    amount = float(input("Enter Amount: "))

    cursor.execute("""
        INSERT INTO transactions (user_id, type, category, amount)
        VALUES (?, ?, ?, ?)
    """, (user_id, transaction_type, category, amount))

    conn.commit()
    conn.close()

    print("\n✅ Transaction Added Successfully!")


def view_transactions(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, type, category, amount
        FROM transactions
        WHERE user_id = ?
    """, (user_id,))

    transactions = cursor.fetchall()

    conn.close()

    print("\n========== Your Transactions ==========")

    if len(transactions) == 0:
        print("No Transactions Found.")

    else:
        print("-" * 55)
        print(f"{'ID':<5}{'TYPE':<12}{'CATEGORY':<18}{'AMOUNT':<10}")
        print("-" * 55)

        for transaction in transactions:
            print(f"{transaction[0]:<5}{transaction[1]:<12}{transaction[2]:<18}{transaction[3]:<10}")

        print("-" * 55)

def search_transaction(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    keyword = input("\nEnter Category to Search: ")

    cursor.execute("""
        SELECT id, type, category, amount
        FROM transactions
        WHERE user_id=? AND category LIKE ?
    """, (user_id, f"%{keyword}%"))

    data = cursor.fetchall()

    conn.close()

    if not data:
        print("\nNo Transaction Found!")
        return

    print("\n========== Search Results ==========")
    print(f"{'ID':<5}{'TYPE':<12}{'CATEGORY':<18}{'AMOUNT'}")

    for row in data:
        print(f"{row[0]:<5}{row[1]:<12}{row[2]:<18}{row[3]}")
def update_transaction(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    transaction_id = input("\nEnter Transaction ID to Update: ")

    cursor.execute("""
        SELECT * FROM transactions
        WHERE id=? AND user_id=?
    """, (transaction_id, user_id))

    record = cursor.fetchone()

    if not record:
        print("Transaction not found.")
        conn.close()
        return

    new_category = input("New Category: ")
    new_amount = float(input("New Amount: "))

    cursor.execute("""
        UPDATE transactions
        SET category=?, amount=?
        WHERE id=?
    """, (new_category, new_amount, transaction_id))

    conn.commit()
    conn.close()

    print("\nTransaction Updated Successfully!")

def delete_transaction(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    transaction_id = input("\nEnter Transaction ID to Delete: ")

    cursor.execute("""
        SELECT * FROM transactions
        WHERE id=? AND user_id=?
    """, (transaction_id, user_id))

    record = cursor.fetchone()

    if not record:
        print("Transaction not found.")
        conn.close()
        return

    cursor.execute("""
        DELETE FROM transactions
        WHERE id=?
    """, (transaction_id,))

    conn.commit()
    conn.close()

    print("\nTransaction Deleted Successfully!")
    