from cli.user_menu import user_menu
from cli.trip_menu import trip_menu
from cli.activity_menu import activity_menu

def main_menu():
    while True:
        print("\n🌍 Travel Planner CLI 🌍")
        print("1. Manage Users")
        print("2. Manage Trips")
        print("3. Manage Activities")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            user_menu()
        elif choice == "2":
            trip_menu()
        elif choice == "3":
            activity_menu()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
