import os
import json

user_cahce = "./cache/user_cache.json"

if not os.path.exists(user_cahce):
    f = open(user_cahce, "w", encoding="utf-8")
    f.write("{}")

with open(user_cahce, "r", encoding="utf-8") as f:
    user_cache = json.load(f)

ACTIVE_REFRESHING_VIEW = user_cache.get("active_refreshing", False)
ACTIVE_ADVANCED_SEARCH_ENGINE = user_cache.get("active_advanced_search", False)
USER_DATA_DIR = user_cache.get("user-data-dir", None)
CHROME_DRIVER_PATH = user_cache.get("chrome-driver-path", None)
SEARCH_ENGINE_PREFER = user_cache.get("search_engine", 0)

def set_cache(key, value):
    user_cache[key] = value
    with open(user_cahce, "w", encoding="utf-8") as f:
        json.dump(user_cache, f)

    