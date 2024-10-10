import os
import json

CACHE_FILE = "response_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_cached_response(prompt):
    cache = load_cache()
    return cache.get(prompt)

def cache_response(prompt, response):
    cache = load_cache()
    cache[prompt] = response
    save_cache(cache)
