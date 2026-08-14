from faker import Faker


fake = Faker()

user_data = {
    "name": fake.name(),
    "email": fake.email(),
    "address": fake.address()
}

print(user_data)
