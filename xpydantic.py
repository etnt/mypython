from pydantic import BaseModel, ValidationError, Field, constr

class User(BaseModel):
    id: int
    name: str
    signup_ts: str = None #Optional field


try:
    user = User(id=1, name="John Doe", signup_ts="2024-07-26T12:00:00")
    print(f"User: {user}")
    print(f"JSON: {user.model_dump_json()}") #Serialize to JSON
except ValidationError as e:
    print(e)

print("--- VALIDATION ERRORS ---")

try:
    print("Before validation")
    user = User(id="abc", name=123) #Incorrect types will raise exception
    print(user)
except ValidationError as e:
    print(e)

print("--- NEXT EXAMPLE --- ")

# Create a type alias for the constrained string
ConstrainedName = constr(min_length=3, max_length=50)

class Product(BaseModel):
    name: ConstrainedName # type: ignore
    price: float = Field(..., gt=0)  # ... means required, gt means greater than
    description: str = None

try:
    product = Product(name="Book", price=19.99, description="A great read")
    print(f"Product: {product}")
except ValidationError as e:
    print(e)

print("--- VALIDATION ERRORS ---")

try:
    product = Product(name="A", price=-1)  #Invalid - name too short, price too low.
    print(product)
except ValidationError as e:
    print(e)

