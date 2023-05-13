from faker import Faker

fake = Faker()
usernames = [fake.user_name() for _ in range(100)]
print(usernames)
