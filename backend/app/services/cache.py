from functools import wraps
from typing import Any, Callable
import hashlib
import json
from datetime import datetime, timedelta

class MemoryCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str) -> Any:
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.now() < expiry:
                return value
            del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300):
        expiry = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = (value, expiry)

memory_cache = MemoryCache()

def cached(ttl: int = 300):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Key based on function name and args
            key_data = f"{func.__name__}:{args}:{kwargs}"
            key = hashlib.md5(key_data.encode()).hexdigest()
            
            cached_result = memory_cache.get(key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            memory_cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator
