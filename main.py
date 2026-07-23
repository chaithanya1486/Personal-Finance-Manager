from auth import register, login


def main():

    while True:

        print("\n===================================")
        print(" Personal Finance Manager ")
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

                print(f"\nWelcome! Your User ID is {user_id}")

                # Dashboard will come here later.
                break

        elif choice == "3":

            print("Thank you for using our application!")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()