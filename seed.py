from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Trip, Activity  # Ensure models.py is correctly structured
from config import engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data (optional, for a fresh start)
session.query(Activity).delete()
session.query(Trip).delete()
session.query(User).delete()
session.commit()

# Default Users (REMOVED 'email' field to match models.py)
users = [
    User(name="Alice Johnson"),
    User(name="Bob Smith"),
    User(name="Charlie Brown")
]

session.add_all(users)
session.commit()

# Default Trips
trips = [
    Trip(destination="Paris, France", user_id=users[0].id),
    Trip(destination="Tokyo, Japan", user_id=users[1].id),
    Trip(destination="New York, USA", user_id=users[2].id),
    Trip(destination="Rome, Italy", user_id=users[0].id)
]

session.add_all(trips)
session.commit()

# Default Activities (REMOVED 'location' field to match models.py)
activities = [
    Activity(name="Eiffel Tower Tour", trip_id=trips[0].id),
    Activity(name="Louvre Museum Visit", trip_id=trips[0].id),
    Activity(name="Sushi Tasting", trip_id=trips[1].id),
    Activity(name="Shibuya Crossing Walk", trip_id=trips[1].id),
    Activity(name="Statue of Liberty Visit", trip_id=trips[2].id),
    Activity(name="Broadway Show", trip_id=trips[2].id),
    Activity(name="Colosseum Tour", trip_id=trips[3].id),
    Activity(name="Vatican Museum", trip_id=trips[3].id)
]

session.add_all(activities)
session.commit()

print("✅ Database seeded successfully with default data!")
