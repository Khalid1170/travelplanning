from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from config import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)  # Ensures unique usernames

    trips = relationship("Trip", back_populates="user")

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    destination = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="trips")
    activities = relationship("Activity", back_populates="trip")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"))

    trip = relationship("Trip", back_populates="activities")

    @property
    def user(self):
        """Returns the user who owns the trip."""
        return self.trip.user if self.trip else None

# Create tables
Base.metadata.create_all(engine)
