#!/usr/bin/python3
"""
Cache class for storing data
"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    """
    Cache class for storing data in Redis
    """


    def __init__(self):
        """
        Initializing the cache instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()


    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count number of times a method is called
        """
        @wraps(method)
        def wrapped(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapped


    @staticmethod
    def call_history(method: Callable) -> Callable:
        """
        Decorator to store the history of inputs and outputs
        """
        @wraps(method)
        def wrapped(self, *args, **kwargs):
            input_key = "{}:inputs".format(method.__qualname__)
            output_key = "{}:output".format(method.__qualname__)


            self.__redis.rpush(input_key, str(args))


            result = method(self, *args, **kwargs)


            self.__redis.rpush(output_key, result)


            return result
        return wrapped


    def store(self, data: Union[str,bytes, int, float]) -> str:
        """
        Store inpute data in Redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retriving data from Redis
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data


    def replay(method: Callable):
        """
        Displays the history of calls
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:output".format(method.__qualname__)


        inputs = method._redis.lrange(input_key, 0, -1)
        outputs = method._redis.lrange(output_key, 0, -1)


        print("{} was called {} times".format(method.__qualname__, len(inputs)))
        for args, output in zip(inputs, outputs):
            print("{}{} -> {}".format(method.__qualname__, args, output))
