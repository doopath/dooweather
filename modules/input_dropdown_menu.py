"""
    Dropdown menu for an input field.
"""
from typing import Any, Callable
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from modules.cache import Cache


class InputDropdownMenu(MDDropdownMenu):
    def __init__(self, update_location: Callable, cache: Cache, **kwargs):
        super().__init__(**kwargs)
        self._cache = cache
        self._remove_all_button_text = "Remove All"
        self._update_weather = update_location
        self.items = []
        self.position = 'center'
        self.width_mult = 4
        self.max_height = Window.size[1] / 3 // 50 * 50

    def _get_cached_cities(self) -> list[str]:
        try:
            return self._cache.get_value('CITIES')
        except KeyError:
            self._cache.set_value('CITIES', [])
            return []

    def _create_item(self, city: str) -> Any:
        return {
            'text': city,
            'viewclass': 'OneLineListItem',
            'on_release': lambda: self._on_release(city)
        }

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
            self._update_weather(city)

        self.dismiss()

    def open(self) -> None:
        self._set_items()
        super().open()
