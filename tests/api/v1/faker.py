import random
import string
from faker import Faker

fake = Faker()

def generate_sample_user_data():
    firstname = fake.first_name()
    lastname = fake.last_name()
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email = fake.email()
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=70))

    return {
        "firstname": firstname,
        "lastname": lastname,
        "username": username,
        "email": email,
        "password": password
    }

def generate_sample_project():
    title = fake.name()
    description = fake.text()
    goal_amount = random.randint(7000, 10000)
    deadline = fake.date()

    return {
        "title": title,
        "description": description,
        "goal_amount": float(goal_amount),
        "deadline": str(deadline)
    }