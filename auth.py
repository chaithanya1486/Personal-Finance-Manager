import sqlite3
import hashlib


def connect_db():
    return sqlite3.connect("finance.db")


def hash_password(password):
    """
    Converts a password into a secure hash.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    conn = connect_db()
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        print("\n✅ Registration Successful!")

    except sqlite3.IntegrityError:
        print("\n❌ Username already exists!")

    conn.close()


def login():
    conn = connect_db()
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed_password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        print("\n✅ Login Successful!")
        return user[0]   # Returns the user's ID
    else:
        print("\n❌ Invalid Username or Password")
        return None


if __name__ == "__main__":
    while True:
        print("\n===== Authentication =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            register()

        elif choice == "2":
            login()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")