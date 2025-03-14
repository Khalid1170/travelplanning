from models import User, Trip, Activity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database connection
DATABASE_URL = "sqlite:///travel_planning.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def main_menu():
    """
    Displays the main menu and handles user input for different options.
    The user can view, add, or delete users, trips, and activities.
    """
    while True:
        print("\n📌 Travel Planning CLI")
        print("1. View Users")
        print("2. Add a User")
        print("3. Delete a User")
        print("4. View Trips")
        print("5. Add a Trip")
        print("6. Delete a Trip")
        print("7. View Activities")
        print("8. Add an Activity")
        print("9. Delete an Activity")
        print("10. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            view_trips()
        elif choice == "5":
            add_trip()
        elif choice == "6":
            delete_trip()
        elif choice == "7":
            view_activities()
        elif choice == "8":
            add_activity()
        elif choice == "9":
            delete_activity()
        elif choice == "10":
            print("Goodbye! 👋")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

def return_to_menu():
    """
    Prompts the user to press 'm' to return to the main menu.
    This ensures smooth navigation.
    """
    while True:
        choice = input("\nPress 'm' to return to the main menu: ").strip().lower()
        if choice == "m":
            return
        else:
            print("Invalid input. Please press 'm'.")

# ----------------- User Management ----------------- #

def view_users():
    """
    Displays a list of all users in the system.
    """
    users = session.query(User).all()
    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"{user.id}: {user.name}")
    
    return_to_menu()

def add_user():
    """
    Adds a new user after checking if the user already exists.
    """
    name = input("Enter user name: ").strip().title()

    existing_user = session.query(User).filter_by(name=name).first()
    if existing_user:
        print("⚠️ User already exists!")
        return_to_menu()
        return

    new_user = User(name=name)
    session.add(new_user)
    session.commit()
    print("✅ User added successfully!")
    return_to_menu()

def delete_user():
    """
    Deletes a user along with their trips and activities.
    """
    users = session.query(User).all()
    if not users:
        print("No users found.")
        return_to_menu()
        return

    print("\n📌 Available Users:")
    for user in users:
        print(f"{user.id}: {user.name}")

    user_id = input("Enter User ID to delete or 'm' to return: ").strip().lower()

    if user_id == "m":
        return

    if user_id.isdigit():
        user = session.query(User).filter_by(id=int(user_id)).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"✅ User '{user.name}' and their associated trips and activities have been deleted!")
        else:
            print("⚠️ User not found!")
    else:
        print("⚠️ Invalid input. Enter a valid User ID or 'm' to return.")

    return_to_menu()


# ----------------- Trip Management ----------------- #

def view_trips():
    """
    Displays a list of all trips along with their associated users.
    Only shows trips where the user exists.
    """
    trips = session.query(Trip).join(User).all()  # Ensure only valid trips are shown

    if not trips:
        print("⚠️ No trips found.")
    else:
        for trip in trips:
            print(f"{trip.id}: {trip.destination} (by {trip.user.name})")  # User guaranteed to exist

    return_to_menu()


def add_trip():
    """
    Allows a user to add a new trip. The user must exist in the system.
    """
    destination = input("Enter trip destination: ").strip().title()

    print("\n📌 Available Users:")
    users = session.query(User).all()
    if not users:
        print("⚠️ No users found! Please add a user first.")
        return_to_menu()
        return

    for user in users:
        print(f"- {user.name}")

    user_name = input("Enter user name: ").strip().title()
    user = session.query(User).filter_by(name=user_name).first()

    if not user:
        print("⚠️ User does not exist! Please add the user first.")
        return_to_menu()
        return

    new_trip = Trip(destination=destination, user_id=user.id)
    session.add(new_trip)
    session.commit()
    print(f"✅ Trip to {destination} added successfully for {user_name}!")
    return_to_menu()

def delete_trip():
    """
    Allows a user to delete a trip by entering the trip ID.
    """
    trips = session.query(Trip).join(User).all()
    if not trips:
        print("No trips found.")
        return_to_menu()
        return

    print("\n📌 Available Trips:")
    for trip in trips:
        print(f"{trip.id}: {trip.destination} (by {trip.user.name})")

    trip_id = input("Enter Trip ID to delete or 'm' to return: ").strip().lower()

    if trip_id == "m":
        return

    if trip_id.isdigit():
        trip = session.query(Trip).filter_by(id=int(trip_id)).first()
        if trip:
            session.delete(trip)
            session.commit()
            print(f"✅ Trip '{trip.destination}' deleted successfully!")
        else:
            print("⚠️ Trip not found!")
    else:
        print("⚠️ Invalid input. Enter a valid Trip ID or 'm' to return.")

    return_to_menu()

# ----------------- Activity Management ----------------- #

def view_activities():
    """
    Displays a list of all activities along with their associated trips and users.
    Only shows activities where the trip has a valid user.
    """
    activities = session.query(Activity).join(Trip).join(User).all()  # Ensure valid user-trips

    if not activities:
        print("⚠️ No activities found.")
    else:
        for activity in activities:
            trip = activity.trip
            user = trip.user  # Ensured valid by join condition
            
            print(f"{activity.id}: {activity.name} (Trip: {trip.destination}, User: {user.name})")
    
    return_to_menu()
 

def add_activity():
    """
    Adds a new activity to a selected trip.
    Only displays trips that have a valid associated user.
    """
    activity_name = input("Enter activity name: ").strip()

    trips = session.query(Trip).join(User).all()  # Only fetch trips with valid users

    if not trips:
        print("⚠️ No available trips found! Please add a user and trip first.")
        return_to_menu()
        return

    print("\n📌 Available Trips:")
    for trip in trips:
        print(f"{trip.id}: {trip.destination} (by {trip.user.name})")

    try:
        trip_id = int(input("Enter the Trip ID to associate this activity with: ").strip())
    except ValueError:
        print("❌ Invalid input. Please enter a numeric Trip ID.")
        return_to_menu()
        return

    selected_trip = session.query(Trip).filter_by(id=trip_id).first()

    if not selected_trip or not selected_trip.user:
        print("❌ Trip ID not found or the trip has no associated user.")
        return_to_menu()
        return

    new_activity = Activity(name=activity_name, trip_id=selected_trip.id)
    session.add(new_activity)
    session.commit()
    print(f"✅ Activity '{activity_name}' added to {selected_trip.destination}!")
    return_to_menu()

if __name__ == "__main__":
    main_menu()
