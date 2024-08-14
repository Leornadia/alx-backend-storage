#!/usr/bin/env python3
"""
This module provides a Cache class for storing and retrieving data in Redis,
and decorators for counting calls and tracking call history.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    
    :param method: The method to wrap.
    :return: The wrapped method that increments the call count and returns the original result.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a particular function.
    
    :param method: The method to wrap.
    :return: The wrapped method that logs inputs and outputs in Redis and returns the original result.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Define Redis keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments in the input list
        self._redis.rpush(input_key, str(args))

        # Execute the original method and get the output
        result = method(self, *args, **kwargs)

        # Store the output in the output list
        self._redis.rpush(output_key, str(result))

        return result
    
    return wrapper

class Cache:
    """
    Cache class that interacts with Redis to store and retrieve data with random keys.
    """

    def __init__(self):
        """
        Initialize the Cache with a Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        :param data: The data to store, which can be of type str, bytes, int, or float.
        :return: The randomly generated key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve the data from Redis using the given key, with an optional conversion function.

        :param key: The key to retrieve data for.
        :param fn: Optional callable to convert the data to the desired format.
        :return: The retrieved data, optionally converted, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data from Redis and decode it as a UTF-8 string.

        :param key: The key to retrieve data for.
        :return: The retrieved data decoded as a UTF-8 string, or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data from Redis and convert it to an integer.

        :param key: The key to retrieve data for.
        :return: The retrieved data converted to an integer, or None if the key does not exist.
        """
        return self.get(key, fn=int)

