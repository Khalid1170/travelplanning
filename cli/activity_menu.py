from models.models import session, Activity

def activity_menu():
    while True:
        print("\n🎢 Activity Management")
        print("1. Add Activity")
        print("2. View Activities by Trip")
        print("3. Delete Activity")
        print("4. Back to Main Menu")
        choice = input("Select an option: ")

if choice == "1":
    trip_id = ("Enter Trip ID: ")
    name = input ("Enter Activity Name: ")
    description = input("Enter Activity Description: ")
    