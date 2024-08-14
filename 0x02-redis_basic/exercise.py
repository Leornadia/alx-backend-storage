#!/usr/bin/env python3
"""
This module implements a replay function to display the history of calls of a particular function.

The `replay` function takes a function and displays the history of its calls, 
including the arguments and the corresponding return values.

Example:
    ```python
    from cache import Cache
    from replay import replay

    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    replay(cache.store)
    ```
    Output:
    ```
    Cache.store was called 3 times:
    Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
    Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
    Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
    ```
"""

import redis
from typing import Callable

def replay(func: Callable) -> None:
    """
    Displays the history of calls of a particular function.

    Args:
        func: The function to replay the calls of.
    """
    redis_client = redis.Redis()
    key = f"{func.__module__}.{func.__name__}:calls"
    inputs_key = f"{func.__module__}.{func.__name__}:inputs"
    outputs_key = f"{func.__module__}.{func.__name__}:outputs"

    num_calls = int(redis_client.get(key).decode("utf-8"))
    inputs = redis_client.lrange(inputs_key, 0, num_calls - 1)
    outputs = redis_client.lrange(outputs_key, 0, num_calls - 1)

    print(f"{func.__qualname__} was called {num_calls} times:")
    for i, (input, output) in enumerate(zip(inputs, outputs)):
        input_str = str(tuple(input.decode("utf-8").split("|")))
        output_str = output.decode("utf-8")
        print(f"{func.__qualname__}*{input_str} -> {output_str}")
