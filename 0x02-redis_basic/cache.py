#!/usr/bin/env python3
"""
This module implements a simple cache class using Redis.

The `Cache` class provides a `store` method to store values in the cache
and a `get` method to retrieve values.
"""

import redis
import uuid

class Cache:
    """
    A simple cache class using Redis.
    """

    def __init__(self) -> None:
        """
        Initializes a Cache object with a connection to the Redis server.
        """
        self.redis_client = redis.Redis()
        self.key_prefix = "cache"

    def store(self, value: str) -> str:
        """
        Stores a value in the cache.

        Args:
            value: The value to store.

        Returns:
            The generated UUID for the stored value.
        """
        key = str(uuid.uuid4())
        self.redis_client.set(f"{self.key_prefix}:{key}", value)

        # Store call information for replay
        func_name = "store"
        redis_client = redis.Redis()
        calls_key = f"{self.__module__}.{func_name}:calls"
        inputs_key = f"{self.__module__}.{func_name}:inputs"
        outputs_key = f"{self.__module__}.{func_name}:outputs"

        num_calls = int(redis_client.get(calls_key).decode("utf-8")) if redis_client.exists(calls_key) else 0
        redis_client.set(calls_key, num_calls + 1)
        redis_client.rpush(inputs_key, str(value))
        redis_client.rpush(outputs_key, key)

        return key

    def get(self, key: str) -> str:
        """
        Retrieves a value from the cache.

        Args:
            key: The key of the value to retrieve.

        Returns:
            The value associated with the key, or None if the key does not exist.
        """
        return self.redis_client.get(f"{self.key_prefix}:{key}").decode("utf-8")
