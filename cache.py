import os
import hashlib

CACHE_DIR = "cache"

os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(url):
    file_name = hashlib.md5(url.encode()).hexdigest() + ".mp4"
    return os.path.join(CACHE_DIR, file_name)

def is_cached(url):
    return os.path.exists(get_cache_path(url))
