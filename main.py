from auth import register, login
from finance import (
    add_transaction,
    view_transactions,
    search_transaction,
    update_transaction,
    delete_transaction
)


def dashboard(user_id):

    while True:

        print("\n===================================")
        print("         USER DASHBOARD")
        print("===================================")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Search Transaction")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_transaction(user_id)

        elif choice == "2":
            view_transactions(user_id)

        elif choice == "3":
            search_transaction(user_id)

        elif choice == "4":
            update_transaction(user_id)

        elif choice == "5":
            delete_transaction(user_id)

        elif choice == "6":
            print("\n✅ Logged Out Successfully!")
            break

        else:
            print("\n❌ Invalid Choice!")


def main():

    while True:

        print("\n===================================")
        print("   PERSONAL FINANCE MANAGER")
        print("===================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            register()

        elif choice == "2":

            user_id = login()

            if user_id:
                print(f"\n✅ Welcome! User ID: {user_id}")
                dashboard(user_id)

        elif choice == "3":
            print("\n👋 Thank you for using Personal Finance Manager!")
            break

        else:
            print("\n❌ Invalid Choice!")


if __name__ == "__main__":
    main()