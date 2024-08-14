#!/usr/bin/env python3
"""
This module implements a get_page function to fetch and cache web pages.
It tracks the number of times a URL is accessed and caches the result for 10 seconds.
"""

import redis
import requests
from functools import wraps
from typing import Callable


def cache_and_track(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of a function and track the number of calls.

    Args:
        expiration (int): Cache expiration time in seconds. Defaults to 10.

    Returns:
        Callable: Decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client = redis.Redis()
            cache_key = f"cached:{url}"
            count_key = f"count:{url}"

            # Increment the access count
            redis_client.incr(count_key)

            # Check if the page is cached
            cached_page = redis_client.get(cache_key)
            if cached_page:
                return cached_page.decode('utf-8')

            # If not cached, fetch the page
            page_content = func(url)

            # Cache the result
            redis_client.setex(cache_key, expiration, page_content)

            return page_content
        return wrapper
    return decorator


@cache_and_track()
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Test the function
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    
    print(f"Fetching: {url}")
    
    # First call (should take about 1 second)
    print("First call:")
    print(get_page(url)[:100])  # Print first 100 characters
    
    # Second call (should be instant due to caching)
    print("\nSecond call (should be faster due to caching):")
    print(get_page(url)[:100])  # Print first 100 characters
    
    # Print the count
    redis_client = redis.Redis()
    count = redis_client.get(f"count:{url}")
    print(f"\nURL accessed {count.decode('utf-8')} times.")
