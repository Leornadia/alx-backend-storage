#!/usr/bin/env python3
"""
Main module for testing the Cache class and replay function.
"""

from exercise import Cache
from replay import replay

if __name__ == "__main__":
    cache = Cache()
    
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    
    replay(cache.store)
