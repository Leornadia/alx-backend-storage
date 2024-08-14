#!/usr/bin/env python3
"""
This script demonstrates how to use the RedisClient and replay modules.
"""

from redis_client import RedisClient
from replay import replay
from cache import Cache # Assuming you have a 'cache.py' file with the Cache class

def main():
    """
    Main function to demonstrate the use of RedisClient and replay.
    """
    # Initialize a RedisClient
    client = RedisClient()

    # Create a Cache instance
    cache = Cache()

    # Use the cache
    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    # Replay the history of calls to cache.store
    replay(cache.store)


if __name__ == "__main__":
    main()
