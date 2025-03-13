from models.models import session, User

def user_menu():
    while True:
        print("\n👤 User Management")
        print("1. Create User")
        print("2. View All Users")
        print("3. Delete User")
        print("4. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            new_user = User(name=name, email=email)
            session.add(new_user)
            session.commit()
            print(f"✅ User {name} created successfully!")
        elif choice == "2":
            users = session.query(User).all()
            for user in users:
                print(f"{user.id}. {user.name} - {user.email}")
        elif choice == "3":
            user_id = input("Enter user ID to delete: ")
            user = session.query(User).get(user_id)
            if user:
                session.delete(user)
                session.commit()
                print("✅ User deleted!")
            else:
                print("User not found.")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
