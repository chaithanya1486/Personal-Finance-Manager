import sqlite3


def add_transaction(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    print("\n========== Add Transaction ==========")

    # Transaction Type Validation
    while True:
        transaction_type = input("Enter Transaction Type (Income/Expense): ").strip().lower()

        if transaction_type in ["income", "expense"]:
            break
        else:
            print("❌ Invalid Transaction Type! Please enter 'Income' or 'Expense'.")

    # Category Validation
    while True:
        category = input("Enter Category: ").strip()

        if category:
            break
        else:
            print("❌ Category cannot be empty!")

    # Amount Validation
    while True:
        try:
            amount = float(input("Enter Amount: "))

            if amount <= 0:
                print("❌ Amount must be greater than 0.")
                continue

            break

        except ValueError:
            print("❌ Invalid Amount! Please enter a valid number.")

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
        ORDER BY id DESC
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
            print(f"{transaction[0]:<5}{transaction[1]:<12}{transaction[2]:<18}{transaction[3]:<10.2f}")
        print("-" * 55)

def search_transaction(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    keyword = input("\nEnter Category to Search: ")

    cursor.execute("""
        SELECT id, type, category, amount
        FROM transactions
        WHERE user_id=? AND category LIKE ?
        ORDER BY id DESC
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
        print("\n❌ Transaction not found.")
        conn.close()
        return

    # Category Validation
    while True:
        new_category = input("New Category: ").strip()

        if new_category:
            break
        else:
            print("❌ Category cannot be empty!")

    # Amount Validation
    while True:
        try:
            new_amount = float(input("New Amount: "))

            if new_amount <= 0:
                print("❌ Amount must be greater than 0.")
                continue

            break

        except ValueError:
            print("❌ Invalid Amount! Please enter a valid number.")

    cursor.execute("""
        UPDATE transactions
        SET category=?, amount=?
        WHERE id=?
    """, (new_category, new_amount, transaction_id))

    conn.commit()
    conn.close()

    print("\n✅ Transaction Updated Successfully!")

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
        print("\n❌ Transaction not found.")
        conn.close()
        return

    confirm = input("Are you sure you want to delete this transaction? (y/n): ").strip().lower()

    if confirm != "y":
        print("\n❌ Deletion Cancelled.")
        conn.close()
        return

    cursor.execute("""
        DELETE FROM transactions
        WHERE id=?
    """, (transaction_id,))

    conn.commit()
    conn.close()

    print("\n✅ Transaction Deleted Successfully!")

def balance_summary(user_id):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    # Total Income
    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = ? AND type = ?
        """,
        (user_id, "income")
    )

    total_income = cursor.fetchone()[0]

    # Total Expense
    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = ? AND type = ?
        """,
        (user_id, "expense")
    )

    total_expense = cursor.fetchone()[0]

    # Handle None values
    if total_income is None:
        total_income = 0

    if total_expense is None:
        total_expense = 0

    balance = total_income - total_expense

    print("\n========== Balance Summary ==========")
    print(f"Total Income  : £{total_income:.2f}")
    print(f"Total Expense : £{total_expense:.2f}")
    print(f"Net Balance   : £{balance:.2f}")

    conn.close()

def expense_report(user_id):

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id=? AND type=?
        GROUP BY category
    """, (user_id, "expense"))

    data = cursor.fetchall()

    conn.close()

    print("\n========== Expense Report ==========")

    if not data:
        print("No expense transactions found.")
        return

    print("-" * 35)
    print(f"{'Category':<20}{'Total'}")
    print("-" * 35)

    for row in data:
        print(f"{row[0]:<20}£{row[1]:.2f}")
        
    print("-" * 35)