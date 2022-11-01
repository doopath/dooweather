"""
    Dropdown menu for selecting a locale.
"""
from typing import Any, Callable
from kivy.core.window import Window
from kivymd.material_resources import dp
from .. import constants
from .base_dropdown_menu import BaseDropdownMenu


class LocalesDropdownMenu(BaseDropdownMenu):
    def __init__(self, update_locale: Callable, *args, **kwargs):
        super().__init__(*args, {**kwargs, 'update': update_locale})

    def _set_items(self) -> None:
        for locale in constants.LOCALES.keys():
            self.items.append(self._create_item(locale))
