# The @dataclasses.dataclass decorator simplifies the creation of classes in Python,
# automatically generating common methods like __init__, __repr__, and others.

import dataclasses

# The simplest way to use it is to decorate a class definition
# Below we create a Point class with two fields, x and y, both of type int. 
# The @dataclasses.dataclass decorator automatically generates:
#
# __init__(self, x: int, y: int): A constructor that takes x and y as arguments
#                                 and initializes the object's attributes.
#
# __repr__(self): A method that returns a string representation of the object,
#                 useful for debugging and printing. It'll look something like
#                 Point(x=10, y=20).
#
# __eq__(self, other): A method for comparing equality between two Point objects.
#
# __hash__(self): A method for creating a hash value, allowing Point objects to
#                 be used as keys in dictionaries and sets.
#
@dataclasses.dataclass
class Point:
    x: int
    y: int

# You can customize the generated methods or add your own
@dataclasses.dataclass
class Circle:
    radius: float

    # The area method is a property, allowing access to the calculated area
    # like an attribute (circle.area).
    @property
    def area(self):
        return 3.14159 * self.radius**2

    # This special method is called after the __init__ method.
    # It's useful for performing validation or additional initialization steps.
    # Here, it checks for a negative radius.
    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("Radius cannot be negative")


# You can specify default values for fields
@dataclasses.dataclass
class Person:
    name: str
    age: int = 30  # Default age is 30


# The @dataclasses.dataclass decorator accepts optional arguments:
#
# init=True (default): Controls whether __init__ is generated.
#                      Set to False to prevent automatic constructor generation.
#
# repr=True (default): Controls whether __repr__ is generated. Set to False to
#                      prevent automatic representation generation.
#
# eq=True (default): Controls whether __eq__ is generated.
#
# order=False (default): If set to True, generates methods for ordering
#                        comparisons (__lt__, __le__, __gt__, __ge__).
#                        Requires fields to be comparable.
#
# frozen=False (default): If set to True, makes the class immutable after initialization.
#                         Fields cannot be changed after object creation.
#
# unsafe_hash=False (default): Usually you shouldn't change this.
#                              Only set to True if you understand the implications
#                              for hashing mutable objects.
#
@dataclasses.dataclass(frozen=True, order=True)
class ImmutablePoint:
    x: int
    y: int
