from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Relationship: A user can have many trips
    trips = relationship('Trip', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship: A trip belongs to a user
    user = relationship('User', back_populates='trips')
    activities = relationship('Activity', back_populates='trip', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Trip(id={self.id}, destination={self.destination}, start_date={self.start_date}, end_date={self.end_date})>"

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    trip_id = Column(Integer, ForeignKey('trips.id'))

    # Relationship: An activity belongs to a trip
    trip = relationship('Trip', back_populates='activities')

    def __repr__(self):
        return f"<Activity(id={self.id}, name={self.name}, trip_id={self.trip_id})>"

# Database setup
DATABASE_URL = "sqlite:///travel_planner.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
