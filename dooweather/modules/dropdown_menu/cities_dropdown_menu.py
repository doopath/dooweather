"""
    Dropdown menu for selecting a city.
"""
from typing import Callable
from ..cache import Cache
from .. import constants
from .base_dropdown_menu import BaseDropdownMenu


class CitiesDropdownMenu(BaseDropdownMenu):
    def __init__(self, update: Callable, cache: Cache, *args, **kwargs):
        super().__init__(update=update, *args, **kwargs)

        self._cache = cache
        self._remove_all_button_text = constants.LOCALE['REMOVE_ALL']

    def _get_cached_cities(self) -> list[str]:
        try:
            return self._cache.get_value('CITIES')
        except KeyError:
            self._cache.set_value('CITIES', [])
            return []

    def _clear_all_items(self) -> None:
        self._cache.set_value('CITIES', [])
        self.items = []

    def _add_remove_all_button(self) -> None:
        self.items.append(self._create_item(self._remove_all_button_text))

    def _set_items(self) -> None:
        cities = self._get_cached_cities()
        self.items = [self._create_item(city) for city in cities]

        if len(self.items) > 0:
            self._add_remove_all_button()

    def _on_release(self, city: str) -> None:
        if city == self._remove_all_button_text:
            self._clear_all_items()
        else:
            self.dismiss()
            self._update(city)
