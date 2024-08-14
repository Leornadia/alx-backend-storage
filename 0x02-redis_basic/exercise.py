#!/usr/bin/env python3
import redis  # Import the Redis client library
import uuid  # Import uuid for generating random keys
from functools import wraps  # Import wraps for preserving metadata in decorators
from typing import Union, Callable, Optional  # Import type hints

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.
    Stores inputs and outputs in Redis using lists.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Store the function's input arguments in a Redis list
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        
        # Execute the original function and store its output in a Redis list
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(output))
        
        # Return the function's output
        return output

    return wrapper

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a function is called.
    Stores the count in Redis using the INCR command.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the call count for this function in Redis
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper

class Cache:
    """Cache class for storing and retrieving data in Redis."""
    
    def __init__(self):
        """Initialize the Cache with a Redis client and flush any existing data."""
        self._redis = redis.Redis()  # Create a Redis client instance
        self._redis.flushdb()  # Clear any existing data in Redis

    @call_history  # Apply the call_history decorator
    @count_calls  # Apply the count_calls decorator
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a generated key.
        Generates a unique key for the data and stores it in Redis.
        """
        key = str(uuid.uuid4())  # Generate a unique key
        self._redis.set(key, data)  # Store the data in Redis with the generated key
        return key  # Return the generated key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and optionally apply a conversion function.
        If a conversion function is provided, it is applied to the retrieved data.
        """
        data = self._redis.get(key)  # Retrieve the data from Redis
        if fn:
            return fn(data)  # Apply the conversion function if provided
        return data  # Return the raw data if no conversion function is provided

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from Redis.
        Automatically decodes the retrieved data as UTF-8.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis.
        Automatically converts the retrieved data to an integer.
        """
        return self.get(key, fn=int)

def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    Shows how many times the function was called, along with the inputs and outputs.
    """
    redis_instance = method.__self__._redis  # Access the Redis instance from the method
    method_name = method.__qualname__  # Get the qualified name of the method

    # Keys for inputs and outputs in Redis
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    # Retrieve inputs and outputs from Redis
    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    # Print the number of times the function was called
    print(f"{method_name} was called {len(inputs)} times:")

    # Iterate through inputs and outputs and print them
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")

