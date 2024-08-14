#!/usr/bin/env python3
"""
This module implements a get_page function to fetch and cache web pages.
It tracks the number of times a URL is accessed and caches the result for 10 seconds.
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def cache_page(expiration: int = 10) -> Callable:
    """
    Decorator to cache the page content and track access count.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Increment the count for how many times this URL is accessed
            redis_client.incr(count_key)

            # Check if the content is already cached
            cached_content = redis_client.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')

            # Fetch the content if not cached
            content = func(url)

            # Cache the new content with expiration
            redis_client.setex(cache_key, expiration, content)
            return content

        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of the specified URL and cache it.
    """
    response = requests.get(url)
    return response.text



