from pydantic import BaseModel


class Address(BaseModel):
    city: str
    zip_code: str


class User(BaseModel):
    id: int
    name: str
    email: str
    address: Address


user = User(id=1, name="Alice", email="alice@example.com", address=Address(city="New York", zip_code="10001"))
print(user)
print(user.address.city)
print(user.model_dump_json())