

class MyClass:

    def __init__(self):
        self.initial_attribute = 10

    # The method allows you to add or change an attribute of an object using
    # strings to specify the attribute's name. This is often used for dynamic
    # attribute creation, where you don't know the attribute name beforehand.
    def _set_attr(self, name, value):
        self.__dict__[name] = value

    # This is a common pattern in Python. It allows you to dynamically create
    # attributes on an object at runtime. This is useful when you don't know the
    # attribute name beforehand, or when you want to create attributes dynamically
    # based on user input or other external factors.
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name in ['one','two']:
            self._set_attr(name, 1 if name == 'one' else 2)
            return self.__dict__[name]
        raise AttributeError(f"Attribute '{name}' not found") 


obj = MyClass()
print(obj.__dict__) # Output: {'initial_attribute': 10}

obj._set_attr("new_attribute", 25)
print(obj.__dict__) # Output: {'initial_attribute': 10, 'new_attribute': 25}

obj._set_attr("initial_attribute", 50) #updates existing attribute
print(obj.__dict__) # Output: {'initial_attribute': 50, 'new_attribute': 25}

print(obj.new_attribute) # Output: 25

print(f"One = {obj.one}") # Output: One = 1
print(f"Two = {obj.two}") # Output: Two = 2
try:
    print(f"Three = {obj.three}") # AttributeError: Attribute 'three' not found
except AttributeError as e:
    print(e)



