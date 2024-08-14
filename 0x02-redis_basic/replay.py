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

from typing import Callable


def replay(func: Callable) -> None:
    """
    Displays the history of calls of a particular function.

    Args:
        func: The function to replay the calls of.
    """
    # Access the Redis instance from the method's class instance
    redis_client = func.__self__._redis

    # Prepare keys for the inputs and outputs based on the function's qualified name
    inputs_key = f"{func.__qualname__}:inputs"
    outputs_key = f"{func.__qualname__}:outputs"

    # Retrieve all inputs and outputs from Redis
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    # Determine the number of calls
    num_calls = len(inputs)

    print(f"{func.__qualname__} was called {num_calls} times:")

    # Iterate through the inputs and outputs and print them
    for input_data, output_data in zip(inputs, outputs):
        input_str = input_data.decode("utf-8")
        output_str = output_data.decode("utf-8")
        print(f"{func.__qualname__}{input_str} -> {output_str}")
