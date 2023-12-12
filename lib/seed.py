from faker import Faker
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Restaurant, Review, Customer
import random

engine = create_engine('sqlite:///db.db')
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()

# Comment out to avoid clearing existing data
session.query(Restaurant).delete()
session.query(Review).delete()
session.query(Customer).delete()
session.commit()

# Create restaurants
restaurants = [
    Restaurant(name=faker.name(), price=randint(0, 60))
    for _ in range(50)
]
session.bulk_save_objects(restaurants)
session.commit()

# Create customers
customers = [
    Customer(name=faker.name()) for _ in range(50)
]
session.bulk_save_objects(customers)
session.commit()

# Generate 10 random reviews
desired_star_ratings = [3, 5]
star_rating = random.choice(desired_star_ratings)

for _ in range(10):
    # Choose random restaurant and customer
    restaurant = random.choice(session.query(Restaurant).all())
    customer = random.choice(session.query(Customer).all())

    # Create new review
    review = Review(star_rating=star_rating,
                    restaurant=restaurant,
                    customer=customer)

    # Add review to session
    session.add(review)

# Commit changes to database
session.commit()

print("Sample data successfully added to the database!")