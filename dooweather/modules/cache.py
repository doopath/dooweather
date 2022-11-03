"""
    Cache of the application.
    Saves app state.
"""
import os
import json
from typing import Any, Callable
from .constants import APP_DIR
from .exceptions import CacheSessionIsNotStartedException, CacheSessionIsAlreadyStartedException


def check_if_opened(f: Callable) -> Callable:
    """
    A decorator that checks if the given context's (self)
    parameter "is_opened" is True. Otherwise, it raises the CacheSessionIsNotStartedException.
    Is not intended for using by other modules.

    Parameters
    ----------
    f - a function to be decorated.

    Returns
    -------
    Decorated "f" function.
    """
    """
        Is not intended for using by other modules.
    """
    def inner(self, *args, **kwargs) -> Any:
        if self.is_opened:
            return f(self, *args, **kwargs)
        else:
            raise CacheSessionIsNotStartedException(
                "You didn't start the cache session!")

    return inner


def check_if_closed(f: Callable) -> Callable:
    """
    A decorator that checks if the given context's (self)
    parameter "is_opened" is False. Otherwise,
        it raises the CacheSessionIsAlreadyStartedException.
    Is not intended for using by other modules.

    Parameters
    ----------
    f - a function to be decorated.

    Returns
    -------
    Decorated "f" function.
    """
    def inner(self, *args, **kwargs) -> Any:
        if not self.is_opened:
            return f(self, *args, **kwargs)
        else:
            raise CacheSessionIsAlreadyStartedException(
                "You didn't start the cache session!")

    return inner


class Cache:
    """
        Class provides methods for caching key-value couples and
        saving them on a local disk.
        Attention! If you don't call save_session method the changes
        made in this session (after creating an instance) will not be saved!
    """
    def __init__(self):
        self._cache_dir = APP_DIR
        self._cache_file = "dooweather-cache.json"
        self._local_cache = {}
        self.is_opened = False
        self._initialize_cache()
        self._initialize_local_cache()
        ...

    @property
    def cache_file_path(self) -> str:
        """
        Get-only property.
        Returns
        -------
        Full path to the cache file as a string
        """
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
            return json.loads(cache_file.read())

    @check_if_opened
    def _initialize_local_cache(self) -> None:
        self._local_cache = self._get_cache()

    @check_if_opened
    def save_session(self) -> None:
        """
            Save all changes on a local disk.
        """
        with open(self.cache_file_path, 'w') as cache_file:
            json.dump(self._local_cache, cache_file)

    @check_if_opened
    def close(self) -> None:
        """
            Closes the cache.
            None will be able to change the cache until you open it.
        """
        self.is_opened = False

    def open(self) -> None:
        """
            Opens the cache.
            You can make changes util the cache is opened
            (call the 'close' method to close it).
        """
        self.is_opened = True

    @check_if_opened
    def get_value(self, key: str) -> Any:
        """
        Get a value from the cache.

        Parameters
        ----------
        key - a key to match with cache.

        Returns
        -------
        A value matched to the 'key' as a string.
        """
        return self._local_cache[key]

    @check_if_opened
    def get_couples(self, keys: list[Any]) -> dict[Any, Any]:
        """
        Parameters
        ----------
        keys - a list of keys to match with cache.

        Returns
        -------
        A dict containing key-value pairs.
        """
        res = {}

        for key in keys:
            res[key] = self.get_value(key)

        return res

    @check_if_opened
    def set_value(self, key: Any, value: Any) -> None:
        """
        Parameters
        ----------
        key: key in cache
        value: value for the key in cache
        """
        self._local_cache[key] = value

    @check_if_opened
    def set_values(self, couples: dict[Any, Any]) -> None:
        """
        Parameters
        ----------
        couples - pairs of keys and values
        """
        for key in couples.keys():
            self._local_cache[key] = couples[key]

