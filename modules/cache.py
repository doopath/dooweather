"""
    Cache of the application.
    Saves app state.
"""
import os
import json
from typing import Any, Callable
from modules.constants import APP_DIR
from modules.exceptions import CacheSessionIsNotStartedException


def check_if_opened(f: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        if args[0].is_opened:
            return f(*args, **kwargs)
        else:
            raise CacheSessionIsNotStartedException("You didn't start the cache session!")

    return inner


class Cache:
    def __init__(self):
        self._cache_dir = APP_DIR
        self._cache_file = "cache.json"
        self._local_cache = {}
        self.is_opened = False
        self._initialize_cache()
        self._initialize_local_cache()

    @property
    def cache_file_path(self) -> str:
        if self._cache_dir == '':
            self._cache_dir = '.'

        return f"{self._cache_dir}/{self._cache_file}"

    def _initialize_cache(self) -> None:
        if not os.path.exists(self.cache_file_path):
            with open(self.cache_file_path, 'w') as cache_file:
                json.dump(self._local_cache, cache_file)

        self.is_opened = True

    @check_if_opened
    def _get_cache(self) -> object:
        with open(self.cache_file_path, 'r') as cache_file:
            return json.load(cache_file)

    @check_if_opened
    def _initialize_local_cache(self) -> None:
        self._local_cache = self._get_cache()

    @check_if_opened
    def save_session(self) -> None:
        with open(self.cache_file_path, 'w') as cache_file:
            json.dump(self._local_cache, cache_file)

    @check_if_opened
    def close(self) -> None:
        self.is_opened = False

    def open(self) -> None:
        self.is_opened = True

    @check_if_opened
    def get_value(self, key: str) -> Any:
        return self._local_cache[key]

    @check_if_opened
    def get_couples(self, keys: list[Any]) -> dict[Any, Any]:
        res = {}

        for key in keys:
            res[key] = self._local_cache[key]

        return res

    @check_if_opened
    def set_value(self, key: Any, value: Any) -> None:
        self._local_cache[key] = value

    @check_if_opened
    def set_values(self, couples: dict[Any, Any]) -> None:
        for key in couples.keys():
            self._local_cache[key] = couples[key]
