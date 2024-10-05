def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()


import time

def elapsed_time(func):
    def f_wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_elapsed = time.time() - t_start
        print(f"Execution time: {t_elapsed:.4f} seconds")
        return result
    return f_wrapper

@elapsed_time
def slow_function(n):
    time.sleep(n)
    return n * 2

result = slow_function(2)  # Sleeps for 2 seconds
print(f"Result: {result}")




import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_call(func):
    def f_wrapper(*args, **kwargs):
        logging.info(f"Calling function: {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Function {func.__name__} finished. Result: {result}")
        return result
    return f_wrapper


@log_call
def add(a, b):
    return a + b

add(5, 3)

# This is the decorator factory. It takes one argument, num_times, which specifies
# how many times the decorated function should be repeated. Notice that it doesn't
# decorate a function directly; instead, it returns a decorator.
def repeat(num_times):
    # This is the actual decorator. It takes the function to be decorated (func)
    # as input. Its job is to create and return the modified function (wrapper).
    # Think of this as the "decorator-making" part.
    def decorator_repeat(func):
        # This is the modified function. This is what actually gets executed when
        # you call the decorated function (greet in our example). It iterates
        # num_times and calls the original function func each time, collecting
        # its result. Crucially, it only returns the result of the last execution.
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("World")
