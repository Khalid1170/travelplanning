from models.models import session, Trip

def trip_menu():
    while True:
        print("\n🛫 Trip Management")
        print("1. Create Trip")
        print("2. View All Trips")
        print("3. Delete Trip")
        print("4. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            user_id = input("Enter User ID: ")
            destination = input("Enter Destination: ")
            start_date = input("Enter Start Date: ")
            end_date = input("Enter End Date: ")
            new_trip = Trip(destination=destination, start_date=start_date, end_date=end_date, user_id=user_id)
            session.add(new_trip)
            session.commit()
            print(f"✅ Trip to {destination} on the {start_date} until {end_date} has been created!")

        elif choice == "2":
            trips = session.query(Trip).all()
            for trip in trips:
                print(f"{trip.id}. {trip.destination} ({trip.start_date} - {trip.end_date})")
        elif choice == "3":
            trip_id = input("Enter Trip ID to delete: ")
            trip = session.query(Trip).get(trip_id)
            if trip:
                session.delete(trip)
                session.commit()
                print("✅ Trip deleted!")
            else:
                print("Trip not found.")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")



