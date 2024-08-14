#!/usr/bin/env python3
"""
This module implements a Cache class for storing and retrieving data in Redis,
along with decorators for counting calls and storing call history.
"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Store inputs
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))

        # Execute the function and store the output
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a function is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the counter each time the method is called
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class for storing and retrieving data in Redis."""
    def __init__(self):
        """Initialize the Cache with a Redis client and flush any existing data."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and optionally apply a conversion function.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieve a string from Redis."""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from Redis."""
        return self.get(key, fn=int)
