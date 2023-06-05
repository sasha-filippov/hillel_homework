from collections import OrderedDict
import functools
import requests


def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                # Move the cache key to the end to indicate it was used
                deco._cache.move_to_end(cache_key, last=True)
                # Increment the frequency count of the cache key
                deco._frequency[cache_key] += 1
                return deco._cache[cache_key]
            result = f(*args, **kwargs)
            if len(deco._cache) >= max_limit:
                # Find the cache key with the lowest frequency count
                lfu_key = min(deco._frequency, key=deco._frequency.get)
                # Remove the least frequently used key from the cache and frequency dictionary
                del deco._cache[lfu_key]
                del deco._frequency[lfu_key]
            deco._cache[cache_key] = result
            # Set the frequency count of the new cache key to 1
            deco._frequency[cache_key] = 1
            return result

        deco._cache = OrderedDict()
        deco._frequency = {}
        return deco

    return internal


@cache(max_limit=64)
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content
