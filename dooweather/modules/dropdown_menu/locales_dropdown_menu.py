"""
    Dropdown menu for selecting a locale.
"""
from typing import Callable
from .. import constants
from .base_dropdown_menu import BaseDropdownMenu


class LocalesDropdownMenu(BaseDropdownMenu):
    def __init__(self, update: Callable, *args, **kwargs):
        super().__init__(update=update, *args, **kwargs)

    def _set_items(self) -> None:
        for locale in constants.LOCALES.keys():
            self.items.append(self._create_item(locale))
