"""
    Dropdown menu for selecting a colorscheme.
"""
from .. import constants
from .base_dropdown_menu import BaseDropdownMenu


class ThemesDropdownMenu(BaseDropdownMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_items(self) -> None:
        for locale in constants.COLORSCHEMES.keys():
            self.items.append(self._create_item(locale))