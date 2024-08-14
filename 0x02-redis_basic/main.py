#!/usr/bin/env python3
"""
Main file for testing the Cache class and replay function
"""

from exercise import Cache, replay

if __name__ == "__main__":
    cache = Cache()
    
    data = b"hello"
    key = cache.store(data)
    print(key)
    
    local_redis = cache._redis
    print(local_redis.get(key))
    
    cache.store(b"world")
    cache.store(b"foo")
    cache.store(b"bar")
    
    replay(cache.store)
