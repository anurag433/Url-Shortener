from django.core.cache import cache

def get_from_cache(key):
    return cache.get(key)

def set_to_cache(key, value, timeout=3600):
    cache.set(key, value, timeout)

def delete_from_cache(short_code):
    cache.delete(short_code)